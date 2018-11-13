import socket
import threading
import tkinter as tk


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except socket.error:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class ClientThread(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.receive_port = 2800
        self.send_port = 2801
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((address, self.receive_port))
        self.client_socket.send("test".encode())


class ServerThread(threading.Thread):
    def __init__(self, listen_socket, conn_ip):
        threading.Thread.__init__(self)
        self.ip = get_ip()
        self.receive_port = 2800
        self.send_port = 2801
        self.connected_ip = conn_ip
        self.current_sock = listen_socket
        test = self.current_sock.recv(1024)
        print(test.decode())


class ListenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = get_ip()
        self.receive_port = 2800
        self.standby_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.standby_sock.bind((self.ip, self.receive_port))
        self.standby_sock.listen(10)
        client, address = self.standby_sock.accept()
        self.server_thread = ServerThread(client, address)
        self.server_thread.start()


class TkinterGui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


if __name__ == '__main__':
    ip = input("input ip ")
    test_thread = ListenThread()
    test_thread.start()
    thread = ClientThread(ip)
    thread.start()
