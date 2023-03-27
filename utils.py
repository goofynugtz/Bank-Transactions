import math, random

def createUsers():
  pass


def generateRandomNumberOfSize(n):
  digits = [i for i in range(0, 10)]
  random_number = ""
  for _ in range(n):
    index = math.floor(random.random() * 10)
  random_number += str(digits[index])
  return random_number

