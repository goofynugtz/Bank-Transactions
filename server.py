import socket as s, threading as t, json, sqlite3 as db, pickle
from data_types import *
from transactions import *

DNS_PORT = 3000
CHQ_PORT = 3001
ATM_PORT = 3002

HOST_IP = '127.0.0.1'
db_connection = db.connect("data.db")
cursor = db_connection.cursor()

class dns_server:
  def __init__(self, host_ip=HOST_IP, port=DNS_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []

    self.cheque_server = cheque_server(HOST_IP)
    
    self.cheque_server.run()
    self.atm_server = atm_server(HOST_IP)
    self.atm_server.run()
    print(f">> Central Server listeing @ PORT: {self.port}")

  def distributor(self, c, address):
    print('[!] Connection request from:', address)
    connected = True
    while connected:
      client_response = c.recv(1024).decode("utf-8")
      print("Client Reponse:", client_response)
      if (client_response == '1'):
        pass # to cheque_handler
      if (client_response == '2'):
        pass # to atm_handler

  def run(self):
    while True:
      c, address = self.server_socket.accept()
      self.connections.append(c)
      thread = t.Thread(target=self.distributor, args=[c,address])
      thread.start()
      print(f"[Active connections to DNS] : {t.active_count()-1}")



class cheque_server:
  def __init__(self, host_ip=HOST_IP, port=CHQ_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []
    print(f">> Cash Server [1] listeing @ PORT: {self.port}")

  def claim(self, c, cheque:cheque):
    print("Waiting for amount: ")
    amount = c.recv(1024).decode('utf-8')
    withdraw(cursor, cheque.payer_ac, amount)
    deposit(cursor, cheque.receiver, amount)

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self.connections.append(c)
      data = c.recv(1024)
      cheque = pickle.loads(data)
      thread = t.Thread(target=self.claim, args=[c,cheque])
      thread.start()


class atm_server:
  def __init__(self, host_ip=HOST_IP, port=ATM_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []
    print(f">> ATM Server [1] listeing @ PORT: {self.port}")

  def run(self):
    pass



if __name__ == "__main__":
  server = dns_server(HOST_IP, DNS_PORT)
  server.run()
