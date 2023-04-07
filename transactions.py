from utils import *
import hashlib

def createAccountsTable():
  sql = f"""
    CREATE TABLE accounts(AccountNo varchar(11) PRIMARY KEY, 
    Name varchar(50), 
    Address varchar(200), 
    Phone varchar(12), 
    Gender varchar(1), 
    Balance bigint);
  """
  cursor.execute(sql)
  db_connection.commit()

def insertInAccountsTable(name, address, gender):
  balance = 10000
  account_no = generateRandomNumberOfSize(11);
  phone = generateRandomNumberOfSize(10);
  sql = f"""
    INSERT INTO accounts VALUES ("{account_no}","{name}","{address}","{phone}","{gender}",{balance});
  """
  cursor.execute(sql)
  db_connection.commit()

def createCardsTable():
  sql = f"""
    CREATE TABLE cards(CardNo varchar(16) PRIMARY KEY, 
    AccountNo varchar(11), 
    Pin varchar(1000),
    FOREIGN KEY (AccountNo) REFERENCES accounts(AccountNo));
  """
  cursor.execute(sql)
  db_connection.commit()

def insertInCardsTable(accountNo, pin):
  card_number = generateRandomNumberOfSize(16)
  sql = f"""
    INSERT INTO cards VALUES ("{card_number}", "{accountNo}", "{hashlib.sha256(pin.encode('utf-8')).hexdigest()}")
  """
  cursor.execute(sql)
  db_connection.commit()

def createChequesIssuedTable():
  sql = f"""
    CREATE TABLE cheques_issued(
    AccountNo varchar(11) NOT NULL,
    ChequeNo varchar(6) NOT NULL,
    Amount int NOT NULL,
    Date date DEFAULT (CURRENT_DATE), 
    PRIMARY KEY(AccountNo, ChequeNo),
    FOREIGN KEY (AccountNo) REFERENCES accounts(AccountNo));
  """
  cursor.execute(sql)
  db_connection.commit()

def issueCheque(cheque_no, amount, payer_ac):
  sql = f"""
    INSERT INTO cheques_issued VALUES ("{payer_ac}","{cheque_no}",{amount},"07-04-2023");
  """
  cursor.execute(sql)
  db_connection.commit()

def withdrawCheque(cheque_no, amount, account_no):
  sql = f"""
    DELETE FROM cheques_issued 
    WHERE AccountNo="{account_no}" AND ChequeNo="{cheque_no}";
  """
  cursor.execute(sql)
  db_connection.commit()
  withdraw(account_no, amount)

def withdraw(account_no, amount):
  sql = f"""
    UPDATE accounts 
    SET balance = balance-{amount} 
    WHERE AccountNo = "{account_no}";
  """
  cursor.execute(sql)
  db_connection.commit()

def deposit(account_no, amount):
  sql = f"""
    UPDATE accounts 
    SET balance = balance+{amount} 
    WHERE AccountNo = "{account_no}";
  """
  cursor.execute(sql)
  db_connection.commit()
