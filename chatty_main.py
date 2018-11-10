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
    def __init__(self, use_socket):
        threading.Thread.__init__(self)
        self.ip = get_ip()
        self.receive_port = 2800
        self.send_port = 2801
        self.tcp_sock = use_socket


class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = get_ip()
        self.receive_port = 2800
        self.send_port = 2801
        self.standby_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class TkinterGui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable
    root.geometry("900x600+360+180")
    root.title("Chatty")
    tk.mainloop()
