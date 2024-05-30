from database import DB
from datetime import datetime
import random
import streamlit as st
#from net_banking import OTPVerification
from otp import OTPVerification
db = DB()
otp = OTPVerification()
class Customer1:

    def __init__(self):
        self.__aadhaar_number = None
        self.__username = None
        self.__name = None
        self.__gender = None
        self.__email = None
        self.__phone_number = None
        self.__bod = None
        self.__age = None
        self.__city = None
        self.__account_number = None

    def get_customer_data(self):
        return {
            "aadhaar_number": self.__aadhaar_number,
            "username": self.__username,
            "name": self.__name,
            "gender":self.__gender,
            "email":self.__email,
            "phone_number": self.__phone_number,
            "bod": self.__bod,
            "age": self.__age,
            "city": self.__city,
            "account_number": self.__account_number
        }

    def createaccount(self):

        #self.current_date = datetime.now()
        #self.birth_date = datetime.strptime(self.__bod, "%Y-%m-%d")
       #age = self.current_date.year - self.birth_date.year

        select2 = ['Male','Female']

        self.__aadhaar_number = st.text_input('Enter your Aadhaar number: ')
        self.__username = st.text_input('Enter your username: ')
        self.__name = st.text_input("Enter your name")
        self.__gender = st.selectbox("Enter your sex",(select2))
        self.__email = st.text_input("Enter your email")
        self.__phone_number = st.text_input('Enter your phone number: ')
        #col1, col2 = st.columns(3)
       # with col1:
        self.__bod = st.date_input('Enter your date of birth:', min_value=datetime(1900, 1, 1), max_value=datetime.now())
            #if self.__bod is not None:
        self.__age = (datetime.now().date() - self.__bod).days // 365
        #self.__age =(datetime.now().date() - self.__bod).days // 365
        #with col2:
        self.__age = st.text_input('Age',(self.__age))
       # self.__age = st.text_input(self.__age)
        self.__city = st.text_input('Enter your city: ')
        #self.current_date = datetime.now()
       # self.birth_date = datetime.strptime(self.__bod, "%Y-%m-%d")
       # self.__age = (datetime.now().date() - self.__bod).days // 365


        self.__account_number = random.randint(100000000, 999999999)
       # current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
       
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if st.button('Create Account', key='create_account'):
            otp.generate_otp()
            otp.send_email(self.__email, otp.otp)
            st.success("OTP has been sent to your email.")
                     
        entered_otp = st.text_input("Enter the OTP received:")
            
        if st.button('Verify OTP', key='verify_otp'):
            if otp.verify_otp(entered_otp):
                st.success('Verification successful')
                try:
                    customer_data = self.get_customer_data()
                    db.execute_query(
                                    f"INSERT INTO abc VALUES ('{customer_data['aadhaar_number']}', '{customer_data['username']}', '{customer_data['name']}', '{customer_data['gender']}', '{customer_data['email']}', '{customer_data['phone_number']}', '{customer_data['bod']}', {customer_data['age']}, '{customer_data['city']}', 0, {customer_data['account_number']}, '{current_datetime}');"
                                )
                    db.commit_changes()
                    st.success('Account created successfully!')
                    st.write(f'Your account number is {self.__account_number} and your initial balance is 0')
                            
                except Exception as e:
                    st.error(f"An error occurred: {e}")
           # else:
#               st.error("Incorrect OTP. Please try again.") 

        if st.button('Resend Otp', key='Resend Otp'):
            otp.generate_otp()
            otp.send_email(self.__email, otp.otp)
            st.success("OTP has been sent to your email.")
                   
           

    def close_account(self):

        account_number = st.text_input('enter your account number:')

        if st.button('closed'):


            sql = ("""INSERT INTO close_account (aadhaar_number, username,name,gender,email phone_number, bod, age, city, balance, account_number, current_datetime)
                    SELECT aadhaar_number, username,name,gender,email phone_number, bod, age, city, balance, account_number, current_datetime
                    FROM abc
                    WHERE aadhaar_number = %s;""")
            data = (account_number,)
            print(sql)
            db.execute_query(sql,data)
            db.commit_changes()
            st.success('Account closed successfull!')

            sql = ("DELETE FROM abc where aadhaar_number = %s;")
            data= (account_number,)
            print(sql)
            try:
                db.execute_query(sql, data)
                db.rowcount()
            except:
                st.error("Account number does not exist")

       

    def kyc_account(self):

        #account_number = input('enter your account number:')
       
        


        #account_number = input('enter your account number:')

        sql = db.execute_query(f"DELETE FROM close_account where aadhaar_number =")
        print(sql)
        try:
            #db.execute_query(sql,data)
            db.rowcount()
        except:
             print("Account number does not exist")




#cs = Customer1()
#cs.createaccount()
#cs.close_account()
#cs.kyc_account()
