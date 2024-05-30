import streamlit as st
import smtplib
import ssl
import random
import time
from loan_predict import *

class OTPVerification:
    def __init__(self):
        self.session = st.session_state
        if 'otp_verification' not in self.session:
            self.session.otp_verification = {
                'email': None,
                'otp': None,
                'sent_time': None,
                'verification_done': False
                
            }

    def send_email(self, receiver_email, otp):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "rajeshsingha1947@gmail.com"  # Enter your address
        password = "ojxg ybsl zvvl pfdl"  # Enter your password
        message = f"""\
        Subject: OTP Verification

        Your OTP is: {otp}"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    def generate_otp(self):
        self.session.otp_verification['otp'] = random.randint(100000, 999999)
        self.session.otp_verification['sent_time'] = time.time()

    def run(self):
        st.title("Email OTP Verification")
        if not self.session.otp_verification['verification_done']:
            self.session.otp_verification['email'] = st.text_input("Enter your email:")

            if st.button("Send OTP"):
                if self.session.otp_verification['email']:
                    self.generate_otp()
                    self.send_email(self.session.otp_verification['email'], self.session.otp_verification['otp'])
                    st.success("OTP has been sent to your email!")

            if self.session.otp_verification['otp']:
                entered_otp = st.text_input("Enter OTP:")
                if st.button('Verify OTP'):
                    if int(entered_otp) == self.session.otp_verification['otp']:
                        self.session.otp_verification['verification_done'] = True
                        st.success("OTP Verified!")
                        #run1()
                    else:
                        st.error("Incorrect OTP, please try again.")

                if self.session.otp_verification['sent_time'] and time.time() - self.session.otp_verification['sent_time'] > 60:
                    self.session.otp_verification['otp'] = None
                    self.session.otp_verification['sent_time'] = None
                    st.warning("OTP expired. Please click 'Send OTP' to resend.")

          

#if __name__ == "__main__":
 #   otp_verification = OTPVerification()
  #  otp_verification.run()
