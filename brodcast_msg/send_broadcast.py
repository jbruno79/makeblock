#!/usr/bin/env python3
# send_broadcast.py
import argparse
import socket
import json
import ipaddress
import sys

PORT = 37020
MY_ID = "PC-Sender"  # ID lógico de este emisor (también default de --name)

def is_ipv4(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Enviar JSON por UDP (broadcast/unicast)")
    parser.add_argument("--to", default="all",
                        help="IPv4 destino o 'all' para broadcast (por defecto: all)")
    parser.add_argument("--message", default="",
                        help="Campo 'message' (por defecto: cadena vacía)")
    parser.add_argument("--value", default="0",
                        help="Campo 'value' (str) (por defecto: 0)")
    parser.add_argument("--type", dest="ptype", default="cmd",
                        help='Campo "type" (por defecto: cmd)')
    parser.add_argument("--name", default=MY_ID,
                        help='Campo "from" (por defecto: MY_ID)')
    args = parser.parse_args()

    # Determinar host destino y 'to' lógico del payload
    if args.to.lower() == "all":
        host = "255.255.255.255"
        logical_to = "*"
        use_broadcast = True
    else:
        if not is_ipv4(args.to):
            print("Error: --to debe ser una IPv4 válida o 'all'.", file=sys.stderr)
            sys.exit(2)
        host = args.to
        logical_to = args.to
        use_broadcast = False

    payload = {
        "type": args.ptype,
        "to": logical_to,
        "from": args.name,
        "message": args.message,
        "value": args.value
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if use_broadcast:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.sendto(json.dumps(payload).encode("utf-8"), (host, PORT))
    print(f"Msg sent to {host}:{PORT} -> {payload}")

if __name__ == "__main__":
    main()
