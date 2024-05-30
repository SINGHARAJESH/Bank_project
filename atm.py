from database import DB
import streamlit as st
from datetime import datetime
from otp import OTPVerification
from update import Up
otp = OTPVerification()
up = Up()
db = DB()

class matm:

    def __init__(self):

        self.account_number = None
        self.user_pin = None
        #self.balance = None
       # self.email = None

        
    def create_pin(self):

    # Step 1: Get account number and PIN from the user
        
        self.account_number = st.text_input('Enter your account number:')
        self.user_pin = st.text_input('Enter your PIN:', type="password")
            
        if st.button('Create PIN', key='create_pin'):
                # Ensure account number and PIN are provided
                
            #self.account_number = account_number
            #self.user_pin = user_pin
                    
            sql = "SELECT balance, email FROM abc WHERE account_number = %s"
            data1 = (self.account_number,)
            record = db.execute_query(sql, data1)
                    
                # Check if account number exists
            if not record:
                st.write('Account number does not exist')
            else:
                  # Fetch balance and email
                for i in record:
                    global balance,email
                    balance = float(i[0])
                        
                    email = i[1]
        
                        # Generate and send OTP
                otp.generate_otp()
                otp.send_email(email, otp.otp)
                st.success(f"OTP has been sent to your registered email id .....{email[4:]}")
                        
                #st.experimental_rerun()

        if st.button('resend otp',key='resend otp'):

            otp.generate_otp()
            otp.send_email(email, otp.otp)
            st.success(f"OTP has been sent to your registered email id .....{email[4:]}")           
                    
        
                 
        entered_otp = st.text_input("Enter the OTP received:")
            
        if st.button('Verify OTP', key='verify_otp'):
            if otp.verify_otp(entered_otp):
                st.success('Verification successful')
                print(self.account_number,self.user_pin)
                    
                try:
                    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Insert new ATM PIN into the database
                    insert_sql = "INSERT INTO ATMs (account_number, ATM_PIN, balance, creation_time) VALUES (%s, %s, %s, %s)"
                    insert_data = (self.account_number,self.user_pin,balance, current_datetime)
                    print(insert_data)
                    db.execute_query(insert_sql, insert_data)
                    db.commit_changes() 
                    st.write('PIN created successfully!')
                    st.session_state.step = 1  # Reset step after successful PIN creation
                except Exception as e:
                    st.write('An error occurred:', e)
            else:
                st.write('Invalid OTP. Please try again.')

       

    def reset_pin(self):
        account_number = st.text_input('Enter your account number:')
        user_pin = st.text_input('Enter your PIN:', type="password")
        self.account_number = account_number
        self.user_pin = user_pin
        
        if st.button('reset pin'):
            try:
                sql = """UPDATE ATMs
                SET ATM_PIN = %s
                WHERE account_number = %s;"""
                value = (self.user_pin,self.account_number)

                db.execute_query(sql,value)
                db.rowcount()
                db.commit_changes()

            except Exception as e:
                        st.error(f"An error occurred: {e}")

      

    def atm_check_balance(self):

        Enter_pin = st.text_input('Enter your pin see balance:')

        if st.button('Check Balance'):

            sql = ("select balance from ATMs where ATM_PIN = %s")
            data = (Enter_pin,)

            record = db.execute_query(sql,data)
            if not record:
                st.error('Pin enter correct pin')
                
            else:
                for i in record:
                    balances = float(i[0])
                    st.write(f'so the balance is {balances}')
                    print(balances)
            sql3 = ("select account_number from ATMs where ATM_PIN = %s")
            data3 = (Enter_pin,)
            record1 = db.execute_query(sql3,data3)
            account_number = record1[0][0]
                    
            up.update_statement(account_number,datetime.now(),"th_atm","check balance",'0.0',balances)

        
        
        pass

    def atm_withdraw(self):
        
        enter_pin = st.text_input('Enter your pin number:')
        amount = st.text_input('Enter the amount:')

        if st.button('withdraw'):

            sql = ("select balance from ATMs where ATM_PIN = %s")
            data = (enter_pin,)
            record = db.execute_query(sql,data)
            print(record)
            balance = float(record[0][0])
            print(balance)

            if balance < int(amount):
                st.error('Insuffient fund')
            else:
                balance = balance - int(amount)
                query = ("UPDATE ATMs set balance = %s where ATM_PIN = %s")

                data = (balance,enter_pin)

                #record = db.execute_query(query,data)
                #db.commit_changes()
                try:
                    db.execute_query(query,data)
                    db.commit_changes()
                        
                    db.rowcount()
                except Exception as e:
                    print(f"Error: {e}")

                st.write(f'Available balance {balance}')
                st.write(f"amount {amount}")
                up.update_abc(enter_pin)

                sql3 = ("select account_number from ATMs where ATM_PIN = %s")
                data3 = (enter_pin,)
                record1 = db.execute_query(sql3,data3)
                account_number = record1[0][0]
                up.update_statement(account_number,datetime.now(),"th_atm","Withdraw",amount,balance)

            

    def atm_deposit(self):
        
        enter_pin = st.text_input('enter your pin number:')
        amount = st.text_input

        if st.button('Deposit'):

            sql = ("select balance from ATMs where ATM_PIN = %s")
            data = (enter_pin,)
            record = db.execute_query(sql,data)
            print(record)
            balance = float(record[0][0])
            print(balance)

            balance = balance + int(amount)
            query = ("UPDATE ATMs set balance = %s where ATM_PIN = %s")

            data = (balance,enter_pin)

                #record = db.execute_query(query,data)
                #db.commit_changes()
            try:
                db.execute_query(query,data)
                db.commit_changes()
                        
                db.rowcount()
            except Exception as e:
                print(f"Error: {e}")

            st.write(f'Available balance {balance}')
            st.write(f"amount {amount}")
            up.update_abc(enter_pin)

            sql3 = ("select account_number from ATMs where ATM_PIN = %s")
            data3 = (enter_pin,)
            record1 = db.execute_query(sql3,data3)
            account_number = record1[0][0]
            up.update_statement(account_number,datetime.now(),"th_atm","deposit",amount,balance)

    