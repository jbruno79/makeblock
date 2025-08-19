# recv_broadcast.py
import socket, json, time

PORT = 37020
MY_ID = "PC-Receiver"  # Cambia a un ID único para este receptor

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))  # "" = todas las interfaces
sock.settimeout(0.1)

print(f"Escuchando UDP {PORT} ...")
while True:
    try:
        data, addr = sock.recvfrom(4096)
    except OSError:
        time.sleep(0.05)
        continue
    try:
        msg = json.loads(data.decode("utf-8"))
    except Exception as e:
        print(f"[{addr}] JSON inválido: {e}")
        continue
    # print(msg)
    # ¿Es para mí o para todos?
    if msg.get("to") in (MY_ID, "*"):
        
        # Aquí tu lógica: p.ej. si message == "set_value"
        if msg.get("type") == "iam":
            value = msg.get("value")
            name = msg.get("from")
            print(f"New device [{name}] : online {value}")

        print(f"[{addr}] {msg}")
