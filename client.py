import hashlib
import socket as s, pickle
from models import *
from utils import *

HOST_IP = '127.0.0.1'
PORT = 3000
# ACCOUNT_NO = 16070322068
# CARD_NO = 2677489830294190
# ACCOUNTHOLDERS_NAME = "Lorenzo Kim"
# CARD_1 = card(CARD_NO, ACCOUNTHOLDERS_NAME)

ACCOUNT_NO = 27030146932
CARD_NO = 6925424292792355
ACCOUNTHOLDERS_NAME = "Rodolfo Ritter"
CARD_1 = card(CARD_NO, ACCOUNTHOLDERS_NAME)

class client:
  def __init__(
      self, host_ip=HOST_IP, 
      port=PORT, 
      accountNumber=ACCOUNT_NO, 
      accountHoldersName=ACCOUNTHOLDERS_NAME,
      card=CARD_1
    ):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.server_socket.connect((self.host_ip, self.port))
    self.accountNumber = accountNumber
    self.accountHoldersName = accountHoldersName
    self.card = card
    self.ref_port = None

  def run(self):
    print("Enter transaction method:\n1. Cheque\n2. ATM\n3. Cash Deposit\n0. Exit")
    user_input = input("[Choice]: ")
    self.server_socket.send(f'{user_input}'.encode())
    self.ref_port = int(self.server_socket.recv(1024).decode())
    if (user_input == "1"):
      self.cheque_client()
    elif (user_input == "2"):
      self.atm_client()
    elif (user_input == "3"):
      self.cash_deposit_client()
    print("Exiting.")

  def cheque_client(self):
    self._private_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self._private_socket.connect((self.host_ip, self.ref_port))
    print("\n1. Issue a cheque.\n2. Claim cheque\n")
    user_input = input("[Choice]: ")
    
    # Cheque Issue
    if (user_input == "1"):
      c_no = generateRandomNumberOfSize(6);
      c_amount = input("Amount: ")
      chq = cheque(c_no, c_amount, self.accountNumber)
      cheque_dump = pickle.dumps(chq)
      self._private_socket.send(user_input.encode())
      self._private_socket.send(cheque_dump)
      print("Issued Cheque Number:", self._private_socket.recv(1024).decode('utf-8'))

    # Claim Cheque
    if (user_input == "2"):
      c_payer_ac = input("Enter Payer A/C No: ")
      c_amount = input("Amount: ")
      c_no = input("Enter Cheque No: ")
      chq = cheque(c_no, c_amount, c_payer_ac)
      cheque_dump = pickle.dumps(chq)
      self._private_socket.send(user_input.encode())
      self._private_socket.send(cheque_dump)
      self._private_socket.send(f'{self.accountNumber}'.encode())
      print(self._private_socket.recv(1024).decode('utf-8'))

  def atm_client(self):
    self._private_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self._private_socket.connect((self.host_ip, self.ref_port))
    card_dump = pickle.dumps(self.card)
    self._private_socket.send(card_dump)
    pin = input('Enter PIN: ')
    pin = hashlib.sha256(pin.encode('utf-8')).hexdigest()
    self._private_socket.send(pin.encode())
    error = self._private_socket.recv(1024).decode('utf-8')

    if (error == '0'):
      c_amount = input("Amount: ")
      self._private_socket.send(f'{c_amount}'.encode())
      print(self._private_socket.recv(1024).decode('utf-8'))
      print(self._private_socket.recv(1024).decode('utf-8'))
    else:
      print("Invalid PIN.")

  def cash_deposit_client(self):
    self._private_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self._private_socket.connect((self.host_ip, self.ref_port))
    s_account_no = input("Account No: ")
    s_amount = input("Amount: ")
    deposit_slip = slip(s_account_no, s_amount)
    slip_dump = pickle.dumps(deposit_slip)
    self._private_socket.send(slip_dump)
    print(self._private_socket.recv(1024).decode('utf-8'))


if __name__ == "__main__":
  client = client(HOST_IP, PORT, ACCOUNT_NO, ACCOUNTHOLDERS_NAME, CARD_1)
  client.run()
