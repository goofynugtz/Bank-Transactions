def withdraw(cursor, account_no, amount):
  sql = f"""
    UPDATE accounts a SET a.balance = a.balance -{amount} WHERE a.AccountNo = {account_no};
  """
  cursor.execute(sql)


def deposit(cursor, account_no, amount):
  sql = f"""
    UPDATE accounts a SET a.balance = a.balance +{amount} WHERE a.AccountNo = {account_no};
  """
  cursor.execute(sql)