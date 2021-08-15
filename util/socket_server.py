import os
import socket
import time

if __name__ == '__main__':

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8085))
    server.listen(128)

    while True:
        conn, addr = server.accept()
        data = conn.recv(1024)
        if b'download' in data:
            data = str(data, encoding='utf-8')
            f_name = data[data.find('_')+1:]
            if f_name not in os.listdir("test"):
                print(f"{f_name} doesn't exist on server")
                conn.sendall(b'NotFound')
            else:
                with open(f"test/{f_name}", 'rb') as f:
                    conn.sendall(b''.join(f.readlines()))
        else:
            t = time.strftime("%Y%m%d_%H%M", time.localtime())
            f_name = f"test/test_{t}.xml"
            with open(f_name, 'wb') as f:
                f.write(data)
            conn.sendall(b'file was successfully stored on server!')

    server.close()
