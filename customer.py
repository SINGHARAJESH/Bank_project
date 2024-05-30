from database import DB
from datetime import datetime
import random
from update import Up
import streamlit as st
up = Up()
db = DB()

class Bank:

    def __init__(self):
        pass


    def check_balance(self):

        account_number = st.text_input('please enter your account number')
        if st.button('Check Balance'):
            try:
                query = ("select balance from abc where account_number =%s;")
                data = (account_number,)
                record = db.execute_query(query,data)
                if not record:
                    print('Account number does not exist')
                
                else:
                    for i in record:
                        balances = float(i[0])
                        st.write(f'so the balance is {balances}')

            except Exception as e:
                print(f"An error occurred: {e}")

    def deposit(self):

        account_number = st.text_input('enter your aacount number to deposit money')
        amount = st.text_input('enter the amount')

        if st.button('deposit'):
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            sql = ("select balance from abc where account_number = %s")
            data1 = (account_number,)

            record = db.execute_query(sql,data1)
            if not record:
                st.error('Account number does not exist')
            else:
                balance = float(record[0][0])
                balance = balance + int(amount)

                st.write(f'so your balance after deposit is {balance}')


            #account_number = int(input('enter your aacount number to deposit money'))
            #amount = int(input('enter the amount'))
            

                query = ("UPDATE abc set balance = %s where account_number = %s")

                data = (balance,account_number)

                #record = db.execute_query(query,data)
                #db.commit_changes()
                try:
                    db.execute_query(query,data)
                    db.commit_changes()
                    
                    db.rowcount()
                except Exception as e:
                    print(f"Error: {e}")

            query = ("select * from sbi")

            record = db.execute_query(query)
            bank_balance = float(record[0][0])

            bank_balance = bank_balance - int(amount)
            sql = ("update sbi set bank_balance = %s")
            data = (bank_balance,)
            db.execute_query(sql,data)
            db.commit_changes()
            print(f'success')
            

            up.update_atm(account_number)
            up.update_statement(account_number,current_datetime,"th_account_number","deposit",amount,balance)



    def withdraw(self):


        account_number = st.text_input('enter your aacount number to deposit money')
        amount = st.text_input('enter the amount')

        if st.button('withdraw'):
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = ("select balance from abc where account_number = %s")
            data1 = (account_number,)

            record = db.execute_query(sql,data1)
            balance = float(record[0][0])
            if not record:
                st.error('Account number does not exist')
            else:

                if balance < int(amount):
                
                    st.error('insuffient balance')
                else:
                    balance = balance - int(amount)

                    query = ("UPDATE abc set balance = %s where account_number = %s")

                    data = (balance,account_number)

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

                    up.update_atm(account_number)
                    up.update_statement(account_number,current_datetime,"th_account_number","withdraw",amount,balance)

    def fund_transfer(self):
        st.write("FROM")
        from_account_number = st.text_input('please enter your account number:')
        st.write("To")
        to_account_number = st.text_input('please enter account number')

        amount = st.text_input('enter the amount that you wnat to transfer')

        if st.button('Transfer fund'):

            sql = ("select balance from abc where account_number = %s")
            data1 = (from_account_number,)

            record = db.execute_query(sql,data1)
            balance = float(record[0][0])
            if not record:
                st.error('Account number does not exist')
            else:

                if balance < int(amount):
                    
                    st.error('insuffient balance')
                else:
                    balance = balance - int(amount)

                    query = ("UPDATE abc set balance = %s where account_number = %s")
                    data = (balance,from_account_number)

                    #record = db.execute_query(query,data)
                    #db.commit_changes()
                    try:
                            db.execute_query(query,data)
                            db.commit_changes()
                            
                            db.rowcount()
                    except Exception as e:
                            print(f"Error: {e}")
                    up.update_atm(from_account_number)

            sql = ("select balance from abc where account_number = %s")
            data1 = (to_account_number,)

            record = db.execute_query(sql,data1)
            if not record:
                    st.error('Account number does not exist')
            else:
                balance = float(record[0][0])
                balance = balance + int(amount)

                st.write(f'so your balance after deposit is {balance}')


                #account_number = int(input('enter your aacount number to deposit money'))
                #amount = int(input('enter the amount'))
                

                query = ("UPDATE abc set balance = %s where account_number = %s")

                data = (balance,to_account_number)

                    #record = db.execute_query(query,data)
                    #db.commit_changes()
                try:
                    db.execute_query(query,data)
                    db.commit_changes()
                        
                    db.rowcount()
                except Exception as e:
                    print(f"Error: {e}")
                up.update_atm(to_account_number)

            #query = ("select * from sbi")

            #record = db.execute_query(query)
            #bank_balance = float(record[0][0])
                    
    

    def check_action_allowed(self, aadhaar_number, action_type):
        query = "SELECT last_check FROM balance_check_log WHERE aadhaar_number = %s AND action_type = %s;"
        data = (aadhaar_number, action_type)
        record = db.execute_query(query, data)
        if record:
            last_check = record[0][0]
            if last_check and (datetime.now() - last_check).days < 1:
                return False
        return True
    def update_action_log(self, aadhaar_number, action_type):
        query = """
        INSERT INTO balance_check_log (aadhaar_number, last_check, action_type)
        VALUES (%s, %s, %s);
        """
        data = (aadhaar_number, datetime.now(), action_type)
        db.execute_query(query, data)
        db.commit_changes()

    def aadhaar_withdraw(self):


        aadhaar_number = st.text_input('enter your aadhaar number to deposit money')
        amount = st.text_input('enter the amount')
        
        if st.button('withdraw'):

            
                #st.error('you can only withdraw money less than 10000')

            
                if not self.check_action_allowed(aadhaar_number, 'withdrawal'):
                    st.error('You can only withdraw money once per day.')
                    return


                sql = ("select balance from abc where aadhaar_number = %s")
                data1 = (aadhaar_number,)

                record = db.execute_query(sql,data1)
                
                balance = float(record[0][0])
                
                if not record:
                    print('aadhaar number does not link with bank account')
                else:

                    if balance < int(amount):
                    
                        st.error('insuffient balance')
                    else:
                        balance = balance - int(amount)

                        query = ("UPDATE abc set balance = %s where aadhaar_number = %s")

                        data = (balance,aadhaar_number)

                    #record = db.execute_query(query,data)
                    #db.commit_changes()
                        try:
                            db.execute_query(query,data)
                            db.commit_changes()
                            
                            db.rowcount()
                            st.write(f'so your balance after deposit is {balance}')
                            self.update_action_log(aadhaar_number, 'withdrawal')


                        except Exception as e:
                            st.error(f"Error: {e}")


                        up.update_atm_th_aadhaar(aadhaar_number)

                        sql2 = ("SELECT account_number FROM abc where aadhaar_number = %s;")
                        data2 = (aadhaar_number,)
                        record1 = db.execute_query(sql2,data2)
                        account_number = record1[0][0]

                        up.update_statement(account_number,datetime.now(),"th_aadhaar_number","withdraw",amount,balance)

                       # st.write(f'so your balance after deposit is {balance}')

                #self.update_action_log(aadhaar_number, 'withdrawal')

            

    def aadhaar_balance(self):

        aadhaar_number = st.text_input('please enter your aadhaar number')

        if st.button('check balance'):

            try:
                
                if not self.check_action_allowed(aadhaar_number, 'balance_check'):
                    st.error('You can only check your balance once per day.')
                    return             

            
                query = ("select balance from abc where aadhaar_number =%s;")
                data = (aadhaar_number,)
                record = db.execute_query(query,data)
                if not record:
                    st.error('Aadhaar number does not exist')
                
                else:
                    for i in record:
                        balances = float(i[0])
                        st.write(f'so the balance is {balances}')

                       
                        self.update_action_log(aadhaar_number, 'balance_check')


            except Exception as e:
                st.error(f"An error occurred: {e}")



    




    def bank_balance(self):

        amount = int(input('enter the amount'))

        sql = ("insert into sbi (bank_balance) values (%s)")

        data= (amount,)

        db.execute_query(sql,data)
        db.commit_changes()



        




#bk = Bank()
#bk.check_balance()
#bk.deposit()
#bk.withdraw()
#bk.fund_transfer()
            

