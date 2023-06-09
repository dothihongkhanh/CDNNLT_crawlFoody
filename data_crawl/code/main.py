import requests
import json
import sys
import  csv
from fastapi import FastAPI
import mysql.connector
import os
app= FastAPI()

class DISH:
    def __init__(self, id, name, price, description, dish_type_name, delivery_id):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.dish_type_name = dish_type_name
        self.delivery_id = delivery_id
    def __str__(self):
        return f"\nid: {self.id}\n name: {self.name}\n price: {self.price}\n description: {self.description}\n dish_type_name: {self.dish_type_name}\n delivery_id: {self.delivery_id}"


@app.get("/crawl_dishes")
async def crawl_dishes():
    # cào id quán
    url = "https://gappapi.deliverynow.vn/api/delivery/get_browsing_ids"

    payload = json.dumps({
    "sort_type": 2,
    "city_id": 219,
    "root_category": 1000001,
    "root_category_ids": [
        1000001
    ]
    })
    headers = {
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'X-Foody-Client-Version': '1',
    'X-Foody-Api-Version': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-Foody-Client-Type': '1',
    'X-Foody-App-Type': '1004',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'X-Foody-Client-Id': '',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    delivery_ids = response.json()['reply']['delivery_ids']
    # Lấy 5 delivery đầu tiên
    first_five_deliveries = delivery_ids[:5]
    print(first_five_deliveries)
    # Lấy  menu quán 
    dish_types = []
    dishess= []
    # xóa dữ liệu cũ trong  file csv
    with open ('dishes.csv',mode ='w', encoding='utf-8', newline ='') as file:
        writer = csv.writer(file)
    for delivery_id in first_five_deliveries:
        url = "https://gappapi.deliverynow.vn/api/dish/get_delivery_dishes?id_type=2&request_id=133203"

        payload = {
            "id_type":2,
            "request_id":delivery_id
        }
        headers = {
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'x-foody-client-version': '3.0.0',
        'x-foody-api-version': '1',
        'sec-ch-ua-mobile': '?0',
        'x-foody-client-language': 'vi',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-foody-client-type': '1',
        'x-foody-app-type': '1004',
        'Accept': 'application/json, text/plain, */*',
        'x-foody-client-id': '',
        'x-foody-access-token': '',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
       
        # Truy cập vào menu_infos
        menu_infos = response.json()['reply']['menu_infos']
        for menu_info in  menu_infos:
            dish_type_name = menu_info["dish_type_name"]
            dishes = menu_info["dishes"]
            for dish in dishes:
                id = dish["id"]
                name = dish["name"]
                price = dish["price"]["text"]
                description=dish["description"]
                dishh = [id, name, price, description, dish_type_name, delivery_id ]
                # chèn dữ liệu vào csv
                with open ('dishes.csv',mode ='a', encoding='utf-8', newline ='') as file:
                    writer = csv.writer(file)
                    writer.writerow(dishh)
                dish = DISH(id = id, name = name ,price = price, description = description, dish_type_name = dish_type_name, delivery_id = delivery_id)
                dishess.append(dish)
            # print(dish_type)
    return {"message": "Data crawled and saved successfully", "data": dishess}

#delete---------------------------
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


@app.delete("/delete_dish/}")
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