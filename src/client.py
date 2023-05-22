import socket
import time

HOST = "192.168.144.157"
PORT = 9000

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send("Hello".encode("utf-8"))
    
    while True:
        data = s.recv(1024)
        print("Received: " + data.decode("utf-8"))
        time.sleep(2)
        s.send("listen now".encode("utf-8"))
        print("Sending: listen now")


if __name__ == "__main__":
    main()