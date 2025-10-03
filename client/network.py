import socket
import json
import threading

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server =  "127.0.0.1"
        self.port = 64340
        self.addr = (self.server, self.port)
        self.name = None #string
        self.otherClients=[]
        self.status = False
        self.lock = threading.Lock()

    def update(self):
        pass
    def connect(self, option,name,password):

            try:
                if hasattr(self, "client"):
                    self.reset()
                self.name = name
                self.client.connect(self.addr)
                self.client.send(json.dumps([option, name, password]).encode())
                self.status=json.loads(self.client.recv(2048).decode()) #list format of all names in string
                if not self.status:
                    self.reset()
                return self.status
            except Exception as e:
                print("Connection error:", e)
                return False

    def reset(self):
        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self,data):
        with self.lock:
            try:
                self.client.send(json.dumps(data).encode())
                return json.loads(self.client.recv(4096).decode())
            except socket.error as e:
                print("Socket error: ", e)

