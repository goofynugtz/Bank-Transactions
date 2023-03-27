class cheque:
  def __init__(self, date, receiver, amount, cheque_no, micr, payer_ac):
    self.date = date
    self.receiver = receiver
    self.amount = amount
    self.cheque_no = cheque_no
    # self.micr = micr
    self.payer_ac = payer_ac

class card:
  def __init__(self, card_no, cardholders_name):
    self.card_no = card_no
    self.cardholders_name = cardholders_name

