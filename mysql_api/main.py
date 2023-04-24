import pandas as pd
import mysql.connector
import csv
import os
from fastapi import FastAPI
app= FastAPI()

@app.get("/insert_file")
async def insert_file():
    # Kết nối đến cơ sở dữ liệu
    mydb = mysql.connector.connect(user='root', password='psw123', port='6603',
    host='127.0.0.1',
    database='foody_db')

    # Tạo một con trỏ để thao tác với database
    mycursor = mydb.cursor()

    # Đọc file CSV

    with open('../data_crawl/code/dishes.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # bỏ qua dòng tiêu đề
        for row in csvreader:
            # xử lý dữ liệu trong mỗi row
            # ví dụ, lưu dữ liệu vào database
            sql = "INSERT INTO Dishes (dish_id, dish_name, price,d_description,dish_type_name,delivery_id) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (row[0], row[1], row[2],row[3],row[4],row[5])
            mycursor.execute(sql, val)

    mydb.commit()
    # Đóng kết nối đến cơ sở dữ liệu
    mycursor.close()
    mydb.close()

@app.post("/add_dish/")
def add_dish(id: str, name: str, price: str, description: str, dish_type_name: str, delivery_id: str):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="psw123",
        port='6603',
        database="foody_db"
    )
    sql = "INSERT INTO Dishes (dish_id,dish_name,price,d_description,dish_type_name,delivery_id) VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor = conn.cursor()
    temp = (id,name,price,description,dish_type_name,delivery_id)
    try:
        mycursor.execute(sql,temp)
        conn.commit()
        result = 'Inserted successful!'
    except:
        result = 'Inserted fail!'  
    mycursor.close()
    conn.close()
    return {"result":result}

@app.delete("/delete_dish2/")
def delete_dish(id: str):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="psw123",
        port='6603',
        database="foody_db"
    )
    sql = "DELETE FROM Dishes WHERE dish_id = %s"
    mycursor = conn.cursor()
    try:
        mycursor.execute(sql,id)
        conn.commit()
        result = 'Inserted successful!'
    except:
        result = 'Inserted fail!'  
    mycursor.close()
    conn.close()
    return {"result":result}