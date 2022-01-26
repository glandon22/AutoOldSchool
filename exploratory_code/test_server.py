def open_port():
    import socket
    import time
    import re
    import json

    host = 'localhost'
    port = 7778
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))
    while True:
        time.sleep(2)
        socket.listen(1)
        conn, addr = socket.accept()
        data = conn.recv(4096)
        if data:
            decoded = data.decode('utf-8')
            body = re.split(r"\s(?=[{\[])", decoded)[-1]
            parsed = json.loads(body)
            print(json.dumps(parsed["attack"], sort_keys=True, indent=4))
        conn.sendall(data)
        conn.close()


open_port()