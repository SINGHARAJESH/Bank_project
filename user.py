from database import DB
import re

db = DB()

class Reg:
    def __init__(self):
        pass

    def check_password_strength(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if re.match(pattern, password):
            return True
        else:
            return False

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        else:
            return False

    def login_user(self):
        email = input("Enter your email:")
        password = input("Enter your password:")

        sql = "SELECT * FROM accounts where email = %s AND password = %s"
        data = (email, password)
        result = db.execute_query(sql, data)

        if result:
            print('Login successful')
        else:
            print("Wrong email or password")

    def register_user(self):
        username = input("Enter your name:")
        email = input("Enter your email:")
        password = input("Enter your password:")

        if not self.validate_email(email):
            print("Please enter a valid email address.")
        elif not self.check_password_strength(password):
            print("Password should be at least 8 characters, one uppercase letter, one lowercase letter, and one special character.")
        else:
            sql = "SELECT * FROM accounts WHERE email = %s"
            data = (email,)
            existing_user = db.execute_query(sql, data)

            if existing_user:
                print("Email already exists. Please choose a different email.")
            else:
                sql = "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)"
                data = (username, email, password)
                db.execute_query(sql, data)
                db.commit_changes()
                print("Registration successful")

#rs = Reg()
#rs.register_user()
def create_pin(self):
        # Step 1: Get account number and PIN from the user
        account_number = st.text_input('Enter your account number:')
        user_pin = st.text_input('Enter your PIN:', type="password")
        
        if st.button('Create PIN', key='create_pin'):
            # Ensure account number and PIN are provided
            if account_number and user_pin:
                self.account_number = account_number
                self.user_pin = user_pin
                
                sql = "SELECT balance, email FROM abc WHERE account_number = %s"
                data1 = (account_number,)
                record = db.execute_query(sql, data1)
                
                # Check if account number exists
                if not record:
                    st.write('Account number does not exist')
                else:
                    # Fetch balance and email
                    self.balance = float(record[0][0])
                    email = record[0][1]

                    # Generate and send OTP
                    self.otp.generate_otp()
                    self.otp.send_email(email, self.otp.otp)
                    st.success("OTP has been sent to your email.")

                    # Move to next step
                    self.verify_otp()
            else:
                st.write("Please provide both account number and PIN.")

    def verify_otp(self):
        # Step 2: Verify OTP
        entered_otp = st.text_input("Enter the OTP received:")

        if st.button('Verify OTP', key='verify_otp'):
            if self.otp.verify_otp(entered_otp):
                st.success('Verification successful')

                try:
                    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Insert new ATM PIN into the database
                    insert_sql = "INSERT INTO ATMs (account_number, ATM_PIN, balance, creation_time) VALUES (%s, %s, %s, %s)"
                    insert_data = (
                        self.account_number,
                        self.user_pin,
                        self.balance,
                        current_datetime
                    )
                    db.execute_query(insert_sql, insert_data)
                    db.commit_changes()

                    st.write('PIN created successfully!')
                except Exception as e:
                    st.write('An error occurred:', e)
            else:
                st.write('Invalid OTP. Please try again.')