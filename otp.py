import smtplib
import ssl
import random
import time
import streamlit as st
class OTPVerification:
    def __init__(self):
       # self.email = None
        self.otp = None
        self.sent_time = None

    def send_email(self, receiver_email, otp):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"  # Change if using a different SMTP server
        sender_email = "rajeshai2000@gmail.com"  # Your email address
        password = "thle qvmb eodm wfgv"  # Your email password
        message = f"""\
        Subject: Email OTP Verification from abc bank

        Your OTP is: {otp}"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    def generate_otp(self):
        self.otp = random.randint(100000, 999999)
        self.sent_time = time.time()

    def verify_otp(self,entered_otp):
        current_time = time.time()
        if self.otp and (current_time - self.sent_time) < 60:
        
            if self.otp and int(entered_otp) == self.otp:

                return True
            else:
                st.error('invalid otp please provide the currect otp')
            return False
        else:
            st.error('time is over please resend otp')
        return False
