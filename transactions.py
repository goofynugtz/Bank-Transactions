from utils import *

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


def insertInAccountsTable(name, address, gender):
  balance = 10000
  account_no = generateRandomNumberOfSize(11);
  phone = generateRandomNumberOfSize(10);
  sql = f"""
    INSERT INTO accounts VALUES ("{account_no}","{name}","{address}","{phone}","{gender}",{balance});
  """
  cursor.execute(sql)


def createCardsTable():
  sql = f"""
    CREATE TABLE cards(CardNo varchar(16) PRIMARY KEY, 
    AccountNo varchar(11), 
    FOREIGN KEY (AccountNo) REFERENCES accounts(AccountNo));
  """
  cursor.execute(sql)


def insertInCardsTable(accountNo):
  card_number = generateRandomNumberOfSize(16)
  sql = f"""
    INSERT INTO cards VALUES ("{card_number}", "{accountNo}")
  """
  cursor.execute(sql)

def createChequesIssuedTable():
  sql = f"""
    CREATE TABLE cheque_issued(
    AccountNo varchar(11),
    ChequeNo varchar(6),
    Date date DEFAULT (CURRENT_DATE), Amount int,
    PRIMARY KEY(AccountNo, ChequeNo),
    FOREIGN KEY (AccountNo) REFERENCES accounts(AccountNo));
  """
  cursor.execute(sql)


def issueCheque(amount, payer_ac):
  chequeNumber = generateRandomNumberOfSize(6);
  sql = f"""
    INSERT INTO cheques_issued VALUES ("{payer_ac}","{chequeNumber}",{amount});
  """
  cursor.execute(sql)


def withdraw(account_no, amount):
  sql = f"""
    UPDATE accounts 
    SET balance = balance-{amount} 
    WHERE AccountNo = "{account_no}";
  """
  cursor.execute(sql)


def deposit(account_no, amount):
  sql = f"""
    UPDATE accounts 
    SET balance = balance+{amount} 
    WHERE AccountNo = "{account_no}";
  """
  cursor.execute(sql)


def issueCheque(amount, payer_ac):
  chequeNumber = generateRandomNumberOfSize(6);
  sql = f"""
    INSERT INTO cheques_issued VALUES ("{payer_ac}","{chequeNumber}",{amount});
  """
  cursor.execute(sql)