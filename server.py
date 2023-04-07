import socket as s, threading as t, sqlite3 as db, pickle
from data_types import *
from transactions import *
from utils import *

CEN_PORT = 3000
CHQ_PORT = 3001
ATM_PORT = 3002
CSD_PORT = 3003

HOST_IP = '127.0.0.1'

class central_server:
  def __init__(self, host_ip=HOST_IP, port=CEN_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []

    print(f"[CEN] >> Central Server listeing @ PORT: {self.port}")

    self.cheque_server = cheque_server(HOST_IP)
    cheque_thread = t.Thread(target=self.cheque_server.run)
    cheque_thread.start()
    self.atm_server = atm_server(HOST_IP)
    atm_thread = t.Thread(target=self.atm_server.run)
    atm_thread.start()
    self.cash_deposit_server = cash_deposit_server(HOST_IP)
    cash_deposit_thread = t.Thread(target=self.cash_deposit_server.run)
    cash_deposit_thread.start()

  def distributor(self, c, address):
    print('[CEN] [!] Connection request from:', address)
    client_response = c.recv(1024).decode("utf-8")
    if (client_response == '1'):
      c.send(f'{CHQ_PORT}'.encode());
    if (client_response == '2'):
      c.send(f'{ATM_PORT}'.encode());
    if (client_response == '3'):
      c.send(f'{CSD_PORT}'.encode());
    c.close()

  def run(self):
    while True:
      c, address = self.server_socket.accept()
      self._connections.append(c)
      thread = t.Thread(target=self.distributor, args=[c,address])
      thread.start()


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
    print("Cheque Issue")
    if (validateAccountNumber(cheque)):
      issueCheque(cheque_no=cheque.cheque_no, amount=cheque.amount, payer_ac=cheque.payer_ac)
      c.send(f'{cheque.cheque_no}'.encode())


  def claim(self, c, cheque:cheque):
    print("Cheque Claim")
    if (validateCheque(cheque)):
      withdrawCheque(cheque_no=cheque.cheque_no, amount=cheque.amount, account_no=cheque.payer_ac)
      # deposit(cheque.receiver, cheque.amount)
      c.send(f'>> Cheque Claimed. Withdrawn amount {cheque.amount}.'.encode())
    else:
      c.send(f'[!] Invalid Cheque.'.encode())

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self._connections.append(c)
      option = c.recv(1024).decode()
      print(f"Option: {option}")
      cheque_dump = c.recv(1024)
      cheque = pickle.loads(cheque_dump)
      if (option == "1"):
        thread = t.Thread(target=self.issue, args=[c,cheque])
        thread.start()
      elif (option == "2"):
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
    if (validateCard(card)):
      amount = c.recv(1024).decode("utf-8")
      account_no = getAccountNumber(card)
      c.send(">> Processing Trasaction...".encode())
      withdraw(account_no, amount)
      balance = getAccountBalance(account_no)
      c.send(f"\nBalance Left: {balance}".encode())

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self._connections.append(c)
      card_dump = c.recv(1024)
      card = pickle.loads(card_dump)
      thread = t.Thread(target=self.withdrawAmount, args=[c,card])
      thread.start()


class cash_deposit_server:
  def __init__(self, host_ip=HOST_IP, port=CSD_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []
    print(f"[CSD] >> Server [1] listeing @ PORT: {self.port}")

  def depositAmount(self, c, slip:slip):
    if (validateAccountNumber(slip.account_no)):
      deposit(slip.account_no, slip.amount)
      c.send(f"\nSuccessfully Deposited".encode())
    else:
      c.send(f"\nInvalid Details.".encode())

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self._connections.append(c)
      slip_dump = c.recv(1024)
      slip = pickle.loads(slip_dump)
      thread = t.Thread(target=self.depositAmount, args=[c,slip])
      thread.start()

if __name__ == "__main__":
  server = central_server(HOST_IP, CEN_PORT)
  server.run()
