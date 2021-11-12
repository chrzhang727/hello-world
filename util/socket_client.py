import socket

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8085))

    while True:
        prompt = input('1. upload file from test dir\n2. download file from test dir\n==>input: ')
        if prompt == '1':
            f_name = input('file name: ')
            with open(f_name, 'rb') as f:
                c =[]
                for i in f.readlines():
                    c.append(str(i, encoding='utf-8'))
                client.sendall(bytes(''.join(c), encoding='utf-8'))
                d = client.recv(1024)
                print(d)
        elif prompt == '2':
            f_name = input('file name: ')
            client.sendall(bytes(f"download_{f_name}", encoding='utf-8'))
            f_content = client.recv(1024)
            if 'NotFound' in str(f_content, encoding='utf-8'):
                print(f"file {f_name} not exists on server!")
                continue
            with open(f_name, 'wb') as f:
                f.write(f_content)
            print(f"{f_name} was successfully downloaded!\n")
        elif prompt == '3':
            break
        else:
            print("Please input the correct number!\n")

    client.close()


