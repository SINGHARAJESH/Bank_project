from database import DB
#from main import *
import re  

import streamlit as st
db = DB()

class Reg:
    def __init__(self):
        
        #self.email = None
        #self.password = None
        pass

    
    def check_password_strength(self,password):
    
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if re.match(pattern,password):
            return True
        else:
            return False

    def validate_email(self,email):

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        else:
            return False
        
    
    def login_user(self):
     

        st.write("<h2 style='color:#D614E6;'>Login Here</h2>", unsafe_allow_html=True)

        email = st.text_input("Enter your email:")
        password = st.text_input("Enter your password:", type="password")

        if st.button("Login"):
            sql = ("SELECT * FROM accounts where email = %s AND password = %s")
            data = (email, password)
            
            result = db.execute_query(sql, data)
            #db.commit_changes()
            if result:
                st.session_state.logged_in = True
                #print('login successfull')
                #second_menu()
            else:
                st.error('Wrong email or password')
                #print("Wrong email or password")

    def register_user(self):
        st.write("<h3 style='color:#3C17BD;'>Register Here</h3>", unsafe_allow_html=True)

        username = st.text_input("Enter your name:")
        email = st.text_input("Enter your email:")
        password = st.text_input("Enter your password:", type="password")


        if st.button('Register'):
            if not self.validate_email(email):
                st.error("Please Enter a Valid Email Address")

            
            #print("Please Enter a Valid Email Address")
            elif not self.check_password_strength(password):
                st.error("Password should be at least 8 characters, one uppercase letter, one lowercase letter and one special character.")

                #print("Password should be at least 8 characters, one uppercase letter, one lowercase letter and one special character.")
            else:
                sql = "SELECT * FROM accounts WHERE email = %s"
                data = (email,)
                db.execute_query(sql,data)
                existing_user = db.execute_query(sql,data)
                if existing_user:
                    st.error("Email already exists. Please choose a different email.")

                    #print("Email already exists. Please choose a different email.")
                else:
                    sql = "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)"
                    data = (username, email, password)
                    db.execute_query(sql, data)
                    db.commit_changes()
                    st.success('Registration successful')
                   # print("Registration successful")

#rs = Reg()
#rs.register_user()