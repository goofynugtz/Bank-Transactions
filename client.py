import socket as s, pickle
from data_types import *
from utils import *

HOST_IP = '127.0.0.1'
PORT = 3000
ACCOUNT_NO = 81971036696
ACCOUNTHOLDERS_NAME = "Lorenzo Kim"

class client:
  def __init__(self, host_ip=HOST_IP, port=PORT, accountNumber=ACCOUNT_NO, accountHoldersName=ACCOUNTHOLDERS_NAME):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.server_socket.connect((self.host_ip, self.port))
    self.accountNumber = accountNumber
    self.accountHoldersName = accountHoldersName
    self.ref_port = None

  def run(self):
    print("Enter transaction method:\n1. Cheque\n2. ATM\n3. Cash Deposit\n0. Exit")
    user_input = input("[Choice]: ")
    self.server_socket.send(f'{user_input}'.encode())
    self.ref_port = int(self.server_socket.recv(1024).decode())
    # self.server_socket.close()
    if (user_input == "1"):
      self.cheque_client()
    if (user_input == "2"):
      self.atm_client()
    print("Exiting.")
      
  def cheque_client(self):
    self._private_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self._private_socket.connect((self.host_ip, self.ref_port))
    print("1. Issue a cheque.\n2. Claim cheque\n")
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
      print(self._private_socket.recv(1024).decode('utf-8'))
    # self._private_socket.close()
    


if __name__ == "__main__":
  client = client(HOST_IP, PORT, ACCOUNT_NO, ACCOUNTHOLDERS_NAME)
  client.run()
