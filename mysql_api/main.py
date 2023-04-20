import mysql.connector
cnx = mysql.connector.connect(user='root', password='psw123', port='6603', host='127.0.0.1', database='foody_db')
cursor = cnx.cursor()
table_name = 'Delivery_Infos'
add_delivery_info = (f"INSERT INTO {table_name} " "(delivery_id, delivery_name, phones , delivery_address, rating ) "   "VALUES (%s, %s, %s, %s, %s)")
data_delivery_info = ('222', '300','ssssssssssssssssssss','Conan','5')

cursor.execute(add_delivery_info, data_delivery_info)
cnx.commit() # lưu những dữ liệu chúng ta đã chèn vào DB
cursor.close()
cnx.close()