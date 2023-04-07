import socket as s, pickle
from data_types import *
from utils import *

HOST_IP = '127.0.0.1'
PORT = 3000

class client:
  def __init__(self, host_ip=HOST_IP, port=PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.server_socket.connect((self.host_ip, self.port))
    self.connected = True
    self.accountNumber = 57449294988
    self.accountHoldersName = "Lorenzo Kim"
    while self.connected:
      print("Enter transaction method:\n1. Cheque\n2. ATM\n3. CashDeposit\n0. Exit")
      user_input = input("[Choice]: ")
      self.server_socket.send(f'{user_input}'.encode())
      self.port = int(self.server_socket.recv(1024).decode())
      print(self.port)
      self.server_socket.close()
      if (user_input == "1"):
        print("CHQ\n")
        self.cheque_client()

      if (user_input == "2"):
        self.server_socket.connect((self.host_ip, self.port))
        self.atm_client()
      if (user_input == "0"):
        self.connected = False
        break


  def cheque_client(self):
    self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.server_socket.connect((self.host_ip, self.port))
    print("1. Issue a cheque.\n2. Claim cheque\n")
    user_input = input("[Choice]: ")
    
    # Cheque Issue
    if (user_input == "1"):
      c_amount = input("Amount: ")
      chq = cheque(c_amount, self.accountNumber)
      cheque_dump = pickle.dumps(chq)
      self.server_socket.send(user_input.encode())
      self.server_socket.send(cheque_dump)
      print("Issued Cheque Number: ", self.server_socket.recv(1024).decode('utf-8'), end="")

    # Claim Cheque
    if (user_input == "2"):
      c_payer_ac = input("Enter Payer A/C No:")
      c_amount = input("Amount:")
      chq = cheque(c_amount, c_payer_ac)
      cheque_dump = pickle.dumps(chq)
      self.server_socket.send(user_input.encode())
      self.server_socket.send(cheque_dump)
    # self.server_socket.close()
    


if __name__ == "__main__":
  client = client(HOST_IP, PORT)
  client.run()
