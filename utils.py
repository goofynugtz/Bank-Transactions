import random, sqlite3 as db
from data_types import *

db_connection = db.connect("data.db")
cursor = db_connection.cursor()

def generateRandomNumberOfSize(n):
  _min = pow(10, n-1)
  _max = pow(10, n) - 1
  return str(random.randint(_min, _max))


def validateCheque(cheque: cheque):
  cursor.execute(f"SELECT AccountNo from accounts WHERE AccountNo={cheque.payer_ac}")
  data = cursor.fetchall()
  return len(data) == 1;


def validateCard(card: card):
  cursor.execute(f"SELECT CardNo from cards WHERE CardNo={card.card_no}")
  data = cursor.fetchall()
  return len(data) == 1;


def getAccountNumber(card: card):
  cursor.execute(f"SELECT AccountNo from cards WHERE CardNo={card.card_no}")
  data = cursor.fetchall()
  return data[0][0]


def getAccountBalance(account_no):
  cursor.execute(f"SELECT balance from accounts WHERE AccountNo={account_no}")
  data = cursor.fetchall()
  return data[0][0]