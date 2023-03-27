from utils import *

def withdraw(cursor, account_no, amount):
  sql = f"""
    UPDATE accounts a SET a.balance = a.balance -{amount} WHERE a.AccountNo = {account_no};
  """
  cursor.execute(sql)


def deposit(cursor, account_no, amount):
  sql = f"""
    UPDATE accounts a SET a.balance = a.balance+{amount} WHERE a.AccountNo = {account_no};
  """
  cursor.execute(sql)

def issueCheque(cursor, amount, payer_ac):
  chequeNumber = generateRandomNumberOfSize(6);
  sql = f"""
    INSERT INTO cheques_issued VALUES ({payer_ac},{chequeNumber},{amount});
  """
  cursor.execute(sql)