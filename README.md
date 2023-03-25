The central server communicates with
1. Cheque Managing Server
2. ATM Managing Server

### Cheque Managing Server
- Cheque is used to withdraw money. Therefore, it has only the account number where it's withdrawn from.
  - Client's A/C No. is "TO" field
  - A/C No. on cheque is "FROM" field
- Fields:
  1. Date (Validity Check: 6 months)
  2. Reciever's Name === Client's A/C Name
  3. Amount
  4. Cheque Number
  5. MICR Code
  6. Payers A/C Number

### ATM Managing Server (INPUT: Card Number, AmountWithdrawn)
- Deduces the amount from account of Card Number.
  - Accepts Cards
- Fields:
  - Card Number
  - Expiry
  - Card Holder's Name

