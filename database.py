import mysql.connector
import streamlit as st


class DB:
    def __init__(self):

        try:

            self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='RajeshSingha@123',
            database = 'gs',
            auth_plugin = 'mysql_native_password')

            self.cur_obj = self.conn.cursor()
            print('connection estiblished')
        except:
            print('connection error')
    
    
    def execute_query(self, query, data=None):
        try:
            if data:
                self.cur_obj.execute(query, data)
            else:
                self.cur_obj.execute(query)
            return self.cur_obj.fetchall()
        except mysql.connector.Error as e:
            print('error executing query:', e)
    
    


    def commit_changes(self):
        try:
            self.conn.commit()
            print('changes committed successfully')
        except mysql.connector.Error as e:
            print('error committing changes:', e)

    def rowcount(self):

        try:
            rows_affected  = self.cur_obj.rowcount

            if rows_affected > 0 :
                st.success('update successfull!')

            else:
                st.error('server down')

        except mysql.connector.Error as e:
            print(f"Error: {e}")
db = DB()