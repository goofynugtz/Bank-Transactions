import socket as s, threading as t, sqlite3 as db, pickle
from models import *
from transactions import *
from utils import *

CEN_PORT = 3000
CHQ_PORT = 3001
ATM_PORT = 3002
CSH_PORT = 3003

HOST_IP = '127.0.0.1'

class central_server:
  def __init__(self, host_ip=HOST_IP, port=CEN_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []
    print(f"[CEN] >> Central Server listening @ PORT: {self.port}")
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
    elif (client_response == '2'):
      c.send(f'{ATM_PORT}'.encode());
    elif (client_response == '3'):
      c.send(f'{CSH_PORT}'.encode());
    else :
      c.send("0".encode());
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
    print(f"[CHQ] >> Server [1] listening @ PORT: {self.port}")

  def issue(self, c, cheque:cheque):
    if (validateAccountNumber(cheque.payer_ac)):
      issueCheque(cheque_no=cheque.cheque_no, amount=cheque.amount, payer_ac=cheque.payer_ac)
      c.send(f'{cheque.cheque_no}'.encode())

  def claim(self, c, cheque:cheque, payee_ac):
    if (validateCheque(cheque)):
      if(validateAccountNumber(payee_ac)):
        if (validateTransactionAmount(cheque.payer_ac,cheque.amount)):
          withdrawCheque(cheque_no=cheque.cheque_no, amount=cheque.amount, account_no=cheque.payer_ac)
          deposit(payee_ac, cheque.amount)
          addTransaction(cheque.payer_ac, payee_ac, cheque.amount, "CHQ")
          c.send(f'>> Cheque Claimed. Transferred amount {cheque.amount}.'.encode())
        else:
          c.send(f'[!] Cheque Bounced.'.encode())
      else:
        c.send(f'[!] Invalid Payee A/C Number.'.encode())
    else:
      c.send(f'[!] Invalid Cheque.'.encode())

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self._connections.append(c)
      option = c.recv(1024).decode()
      print(option)
      if (option == "1"):
        cheque_dump = c.recv(1024)
        cheque = pickle.loads(cheque_dump)
        # print(cheque.cheque_no)
        # print(cheque.amount)
        # print(cheque_dump)
        thread = t.Thread(target=self.issue, args=[c,cheque])
        thread.start()
      elif (option == "2"):
        cheque_dump = c.recv(1024)
        cheque, payee_ac = pickle.loads(cheque_dump)
        payee_ac = str(payee_ac)
        print(payee_ac)
        thread = t.Thread(target=self.claim, args=[c,cheque, payee_ac])
        thread.start()


class atm_server:
  def __init__(self, host_ip=HOST_IP, port=ATM_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []
    print(f"[ATM] >> Server [1] listening @ PORT: {self.port}")

  def withdrawAmount(self, c):
    card_dump = c.recv(1024)
    card = pickle.loads(card_dump)
    pin = c.recv(1024).decode()
    if (validateCard(card, pin)):
      c.send("0".encode())
      amount = c.recv(1024).decode("utf-8")
      account_no = getAccountNumber(card)
      if (validateTransactionAmount(account_no,amount)):
        c.send(">> Processing Transaction...".encode())
        withdraw(account_no, amount)
        addTransaction(account_no, None, amount, mode="ATM")
      else:
        c.send("[!] Insufficient Balance".encode())
      
      balance = getAccountBalance(account_no)
      c.send(f"Balance Left: {balance}".encode())
    else:
      c.send("1".encode())

  def run(self):
    while True:
      c, _ = self.server_socket.accept()
      self._connections.append(c)
      thread = t.Thread(target=self.withdrawAmount, args=[c])
      thread.start()


class cash_deposit_server:
  def __init__(self, host_ip=HOST_IP, port=CSH_PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self._connections = []
    print(f"[CSH] >> Server [1] listening @ PORT: {self.port}")

  def depositAmount(self, c, slip:slip):
    if (validateAccountNumber(slip.account_no)):
      deposit(slip.account_no, slip.amount)
      addTransaction(None, slip.account_no, slip.amount, "CSH")
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
