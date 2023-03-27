import socket as s, threading as t, sqlite3 as db, pickle
from data_types import *
from transactions import *
from utils import *

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

    print(f"[DNS] >> Central Server listeing @ PORT: {self.port}")

    self.cheque_server = cheque_server(HOST_IP)
    cheque_thread = t.Thread(target=self.cheque_server.run)
    cheque_thread.start()
    self.atm_server = atm_server(HOST_IP)
    atm_thread = t.Thread(target=self.atm_server.run)
    atm_thread.start()

  def distributor(self, c, address):
    print('[DNS] [!] Connection request from:', address)
    connected = True
    while connected:
      client_response = c.recv(1024).decode("utf-8")
      print("[DNS] Client Reponse:", client_response)
      if (client_response == '1'):
        
      if (client_response == '2'):
        pass # to atm_handler

  def run(self):
    while True:
      c, address = self.server_socket.accept()
      self.connections.append(c)
      thread = t.Thread(target=self.distributor, args=[c,address])
      thread.start()
      print(f"[DNS] [Active connections] : {t.active_count()-1}")


class cheque_server:
  def __init__(self, host_ip=HOST_IP, port=CHQ_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []
    print(f"[CHQ] >> Server [1] listeing @ PORT: {self.port}")

  def issue(self, c, cheque:cheque):
    if (chequeIsValid(cheque)):
      issueCheque(cursor, cheque.amount, cheque.payer_ac)
      db_connection.commit()

  def claim(self, c, cheque:cheque):
    if (chequeIsValid(cheque)):
      withdraw(cursor, cheque.payer_ac, cheque.amount)
      deposit(cursor, cheque.receiver, cheque.amount)
      db_connection.commit()

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self.connections.append(c)
      option = c.recv(1024).decode()
      if (option == "1"):
        cheque_dump = c.recv(1024)
        cheque = pickle.loads(cheque_dump)
        thread = t.Thread(target=self.issue, args=[c,cheque])
        thread.start()
      elif (option == "2"):
        cheque_dump = c.recv(1024)
        cheque = pickle.loads(cheque_dump)
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
    print(f"[ATM] >> Server [1] listeing @ PORT: {self.port}")

  def withdrawAmount(self, c, card:card):
    if (cardIsValid(card)):
      amount = c.recv(1024)
      account_no = getAccountNumber(card)
      c.send("Processing Trasaction...".encode())
      withdraw(cursor, account_no, amount)
      db_connection.commit()
      balance = getAccountBalance(account_no)
      c.send(f"Balance Left: {balance}".encode())

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self.connections.append(c)
      card_dump = c.recv(1024)
      card = pickle.loads(card_dump)
      thread = t.Thread(target=self.withdrawAmount, args=[c,card])
      thread.start()


if __name__ == "__main__":
  server = dns_server(HOST_IP, DNS_PORT)
  server.run()
