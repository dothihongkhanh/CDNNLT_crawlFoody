import pandas as pd
import mysql.connector
import csv

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


# cnx = mysql.connector.connect(user='root', password='psw123', port='6603', host='127.0.0.1', database='foody_db')
# cursor = cnx.cursor()
# table_name = 'Delivery_Infos'
# add_delivery_info = (f"INSERT INTO {table_name} " "(delivery_id, delivery_name, phones , delivery_address, rating ) "   "VALUES (%s, %s, %s, %s, %s)")
# data_delivery_info = ('222', '300','ssssssssssssssssssss','Conan','5')

# cursor.execute(add_delivery_info, data_delivery_info)
# cnx.commit() # lưu những dữ liệu chúng ta đã chèn vào DB
# cursor.close()
# cnx.close()
