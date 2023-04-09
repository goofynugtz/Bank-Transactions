from utils import *
import hashlib

def cleanup():
  cursor.execute("DROP TABLE IF EXISTS accounts;")
  db_connection.commit()  
  cursor.execute("DROP TABLE IF EXISTS cards;")
  db_connection.commit()  
  cursor.execute("DROP TABLE IF EXISTS cheques_issued;")
  db_connection.commit()  
  cursor.execute("DROP TABLE IF EXISTS transactions;")
  db_connection.commit()  


def createAccountsTable():
  sql = f"""
    CREATE TABLE accounts(
      AccountNo varchar(11) PRIMARY KEY, 
      Name varchar(50), 
      Address varchar(200), 
      Phone varchar(12), 
      Gender varchar(1), 
      Balance decimal(20,2)
    );
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
    INSERT INTO cards VALUES ("{card_number}", "{accountNo}", "{hashlib.sha256(pin.encode('utf-8')).hexdigest()}");
  """
  cursor.execute(sql)
  db_connection.commit()

def createTransactionsTable():
  sql = f"""
    CREATE TABLE transactions(
      TransactionId integer PRIMARY KEY AUTOINCREMENT, 
      FromAccount varchar(11) NULL,
      ToAccount varchar(11) NULL,
      Amount DECIMAL(3) NOT NULL,
      Mode varchar(3) NOT NULL,
      TransactionDateTime DATETIME DEFAULT (CURRENT_TIMESTAMP),
      FOREIGN KEY (FromAccount) REFERENCES accounts(AccountNo),
      FOREIGN KEY (ToAccount) REFERENCES accounts(AccountNo)
    );
  """
  cursor.execute(sql)
  db_connection.commit()
  # sql = """ALTER TABLE transactions AUTO_INCREMENT = 23590;"""
  # cursor.execute(sql)
  # db_connection.commit()

def addTransaction(from_account, to_account, amount, mode="ATM"):
  sql = None
  if (to_account is None):
    sql = f"""
      INSERT INTO transactions (FromAccount, Amount, Mode) VALUES ("{from_account}", {amount}, "{mode}");
    """
  elif (from_account is None):
    sql = f"""
      INSERT INTO transactions (ToAccount, Amount, Mode) VALUES ("{to_account}", {amount}, "{mode}");
    """
  else:
    sql = f"""
      INSERT INTO transactions (FromAccount, ToAccount, Amount, Mode) VALUES("{from_account}", "{to_account}", {amount}, "{mode}");
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
      FOREIGN KEY (AccountNo) REFERENCES accounts(AccountNo)
    );
  """
  cursor.execute(sql)
  db_connection.commit()

def issueCheque(cheque_no, amount, payer_ac):
  sql = f"""
    INSERT INTO cheques_issued (AccountNo, ChequeNo, Amount) VALUES ("{payer_ac}","{cheque_no}",{amount});
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

def bounceCheque(cheque_no, account_no):
  sql = f"""
    DELETE FROM cheques_issued 
    WHERE AccountNo="{account_no}" AND ChequeNo="{cheque_no}";
  """
  cursor.execute(sql)
  db_connection.commit()

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
