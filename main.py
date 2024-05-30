from database import DB
import pandas as pd
import streamlit as st
from register import Reg
from bank import Customer1
from loan_predict import *
from customer import Bank
from atm import matm
db = DB()
rs = Reg() 
cs = Customer1()
bk = Bank()
atm = matm()
#first_input = int(input('enter the number'))
def first_menu():

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
    

        second_menu()
    else:
        st.title("First Menu")
        first_input = st.sidebar.selectbox("Menu Options", ["Login", "Register", "Forget Password"])
        
        if first_input == "Login":
            if rs.login_user():
                second_menu()
        elif first_input == "Register":
            rs.register_user() 
        elif first_input == "Forget Password":
            rs.reset_password()


1

def second_menu():
    st.write("<h2 style='color:#1EC9E3;'>Perform Your Task</h2>", unsafe_allow_html=True)

    second_input = st.sidebar.selectbox("Menu Options", ["open account","loan predict", "matm","apes","deposit","withdraw","Fund transfer","Check Balance","Logout"])

    if second_input == "open account":
        cs.createaccount()
    elif second_input == "loan predict":
        cs.close_account()
        
    elif second_input == "matm":
        atm_menu()
    elif second_input == "apes":
        aadhaar_menu()
    elif second_input == "deposit":
        bk.deposit()
    
    elif second_input =="withdraw":
        bk.withdraw()
    elif second_input == 'Fund transfer':
        bk.fund_transfer()
        
    elif second_input == "Check Balance":
        bk.check_balance()
    elif second_input =="":
        pass
    elif second_input == "":
        pass
    elif second_input == "Logout":
        st.session_state.logged_in = False
        first_menu()
def atm_menu():

    if 'page' not in st.session_state:
        st.session_state.page = 'main'

    if st.session_state.page == 'main':
        st.title("ATM Operations")

        # Create a horizontal layout with columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button('Create PIN'):
                st.session_state.page = 'create_pin'
        
        with col2:
            if st.button('Reset PIN'):
                st.session_state.page = 'reset_pin'
        
        with col3:
            if st.button('Check Balance'):
                st.session_state.page = 'check_balance'
        
        with col4:
            if st.button('Withdraw'):
                st.session_state.page = 'withdraw'
        
        with col5:
            if st.button('Deposit'):
                st.session_state.page = 'deposit'

    elif st.session_state.page == 'create_pin':
        st.title('Create PIN')
        if st.button('Back'):
            st.session_state.page = 'main'
        else:
            atm.create_pin()

    elif st.session_state.page == 'reset_pin':
        st.title('Reset PIN')
        if st.button('Back'):
            st.session_state.page = 'main'
        else:
            st.write('Reset pin functionality will be implemented here.')
            atm.reset_pin()

    elif st.session_state.page == 'check_balance':
        st.title('Check Balance')
        if st.button('Back'):
            st.session_state.page = 'main'
        else:
            st.write('Check balance functionality will be implemented here.')
            atm.atm_check_balance()

    elif st.session_state.page == 'withdraw':
        st.title('Withdraw')
        if st.button('Back'):
            st.session_state.page = 'main'
        else:
            st.write('Withdraw functionality will be implemented here.')
            atm.atm_withdraw()

    elif st.session_state.page == 'deposit':
        st.title('Deposit')
        if st.button('Back'):
            st.session_state.page = 'main'
        else:
            st.write('Deposit functionality will be implemented here.')


def aadhaar_menu():

    if 'page' not in st.session_state:
        st.session_state.page = 'main'

    if st.session_state.page == 'main':
        st.title("ATM Operations")

        # Create a horizontal layout with columns
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button('withdraw'):
                st.session_state.page = 'withdraw'
        
        with col2:
            if st.button('balance'):
                st.session_state.page = 'balance'

    elif st.session_state.page == 'withdraw':
        st.title('withdraw')
        if st.button('Back'):
            st.session_state.page = 'main'
        else:
            bk.aadhaar_withdraw()

    elif st.session_state.page == 'balance':
        st.title('balance')
        if st.button('Back'):
            st.session_state.page = 'main'
        else:
            bk.aadhaar_balance()
first_menu()