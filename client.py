import hashlib
import socket as s, pickle
from models import *
from utils import *

HOST_IP = '127.0.0.1'
PORT = 3000

# ACCOUNT_NO = 43902648598
# CARD_NO = 6401128508191489
# ACCOUNTHOLDERS_NAME = "Lorenzo Kim"
# CARD_1 = card(CARD_NO, ACCOUNTHOLDERS_NAME)

# ACCOUNT_NO = 76372390228
# CARD_NO = 3974973546780680
# ACCOUNTHOLDERS_NAME = "Rodolfo Ritter"
# CARD_1 = card(CARD_NO, ACCOUNTHOLDERS_NAME)

class client:
  def __init__(
      self, 
      accountNumber, 
      accountHoldersName,
      card,
      host_ip=HOST_IP, 
      port=PORT, 
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
    print("""
      \n\nEnter transaction method:\n1. Cheque\n2. ATM\n3. Cash Withdrawal/Deposit\n0. Exit
    """)
    user_input = input("[Choice]: ")
    self.server_socket.send(f'{user_input}'.encode())
    # self.ref_port = int(self.server_socket.recv(1024).decode())
    if (user_input == "1"):
      self.cheque_client()
    elif (user_input == "2"):
      self.atm_client()
    elif (user_input == "3"):
      self.cash_client()
    else:
      print("Exiting.")
      return 0
    return 1

  def cheque_client(self):
    # self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    # self.server_socket.connect((self.host_ip, self.ref_port))
    print("\n1. Issue a cheque.\n2. Claim cheque\n")
    user_input = input("[Choice]: ")
    
    # Cheque Issue
    if (user_input == "1"):
      c_no = generateRandomNumberOfSize(6);
      c_amount = input("Amount: ")
      chq = cheque(c_no, c_amount, self.accountNumber)
      cheque_dump = pickle.dumps(chq)
      self.server_socket.send(user_input.encode())
      self.server_socket.send(cheque_dump)
      print("Issued Cheque Number:", 
            self.server_socket.recv(1024).decode('utf-8'))

    # Claim Cheque
    if (user_input == "2"):
      c_payer_ac = input("Enter Payer A/C No: ")
      c_amount = input("Amount: ")
      c_no = input("Enter Cheque No: ")
      chq = cheque(c_no, c_amount, c_payer_ac)
      self.server_socket.send(user_input.encode())
      sender_dump = [chq, self.accountNumber]
      sender_dump = pickle.dumps(sender_dump)
      self.server_socket.send(sender_dump)
      print(self.server_socket.recv(1024).decode('utf-8'))

  def atm_client(self):
    # self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    # self.server_socket.connect((self.host_ip, self.ref_port))
    card_dump = pickle.dumps(self.card)
    self.server_socket.send(card_dump)
    pin = input('\nEnter PIN: ')
    pin = hashlib.sha256(pin.encode('utf-8')).hexdigest()
    self.server_socket.send(pin.encode())
    error = self.server_socket.recv(1024).decode('utf-8')
    if (error == '0'):
      c_amount = input("Amount: ")
      self.server_socket.send(f'{c_amount}'.encode())
      print(self.server_socket.recv(1024).decode('utf-8'))
      print(self.server_socket.recv(1024).decode('utf-8'))
    else:
      print("[!] Invalid PIN.")

  def cash_client(self):
    # self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    # self.server_socket.connect((self.host_ip, self.ref_port))
    print("\nEnter Transaction Slip details:")
    s_account_no = input("Account No: ")
    s_amount = input("Amount: ")
    print("\n1. Withdrawal\n2. Deposit")
    s_method = input("[Choice]: ")
    deposit_slip = slip(s_account_no, s_amount, s_method)
    slip_dump = pickle.dumps(deposit_slip)
    self.server_socket.send(slip_dump)
    print(self.server_socket.recv(1024).decode('utf-8'))


if __name__ == "__main__":
  accountNo = input("\nEnter A/C No: ")
  accountHoldersName = input("Enter A/C Holder's Name: ")
  cardNo = input("Enter Card No: ")
  debitCard = card(cardNo, accountHoldersName)
  print(">> Verifying...")
  
  if validateUserCredentials(accountNo, accountHoldersName, debitCard):
    print("Successfully Verified.")
    c = client(accountNo, accountHoldersName, debitCard, HOST_IP, PORT)
    while(True):
      exitFlag = c.run()
      if (exitFlag == 0): 
        break
  else:
    print("[!] Invalid User Credentials.")
  
