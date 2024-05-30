from database import DB
import streamlit as st
db = DB()

class Up:

    def __init__(self):
        
        self.account_number = None
        self.aadhaar_number = None
        self.pin = None
        self.date_time = None
        self.description = None
        self.transtion_type = None
        self.amount = None
        self.balance = None



    def update_abc(self,pin):

        update = ("""UPDATE abc
                    SET Balance = (SELECT Balance FROM ATMs WHERE ATM_PIN  = %s)
                    WHERE account_number = (SELECT account_number FROM ATMs WHERE ATM_PIN = %s);""")
        data2 = (pin,pin)
        db.execute_query(update,data2)
        db.commit_changes()

    def update_atm(self,account_number):

        update = ("""UPDATE ATMs
                      SET Balance = (SELECT Balance FROM abc WHERE account_number = %s)
                      WHERE account_number = %s;""")
        data2 = (account_number,account_number,)
        try:

            db.execute_query(update,data2)
            db.commit_changes()
        except Exception as e:
            st.error(f"Error: {e}")

    def update_atm_th_aadhaar(self,aadhaar_number):

        update = ("""UPDATE ATMs
                      SET Balance = (SELECT Balance FROM abc WHERE aadhaar_number = %s)
                      WHERE account_number = (SELECT account_number FROM abc where aadhaar_number = %s);""")
        data2 = (aadhaar_number,aadhaar_number,)
        
        try:
            db.execute_query(update,data2)
            db.commit_changes()
        except Exception as e:
            st.error(f"Error: {e}")

    def update_statement(self,account_number,date_time,description,transtion_type,amount,balance):

        sql =    (""" INSERT INTO bank_statement (account_number, date_time, description, transaction_type, amount, balance)
                       VALUES (%s,%s,%s,%s,%s,%s);""")
        data = (account_number,date_time,description,transtion_type,amount,balance)
        db.execute_query(sql,data)
        db.commit_changes()



        