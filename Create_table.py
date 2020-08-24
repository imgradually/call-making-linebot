import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a 你-APP-的名字').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

SQL_order = '''CREATE TABLE variable(
      var_name VARCHAR(100) PRIMARY KEY,
      value VARCHAR(100));
      '''
SQL_order = SQL_order + '''CREATE TABLE group_info(
      group_name VARCHAR(100) PRIMARY KEY,
      group_id VARCHAR(100),
      group_tag VARCHAR(100));
       '''

SQL_order = SQL_order + '''CREATE TABLE user_info(
      user_name VARCHAR(100) PRIMARY KEY,
      user_id VARCHAR(100),
      user_phone_number VARCHAR(100));
       '''
SQL_order = '''CREATE TABLE admin_info(
      admin_name VARCHAR(100) PRIMARY KEY,
      admin_id VARCHAR(100));
      '''
SQL_order = "INSERT INTO variable (var_name,value) VALUES ('greeting','Hi')"
cursor.execute(SQL_order)
conn.commit()
cursor.close()
conn.close()