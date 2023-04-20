import requests #để gửi các yêu cầu HTTP
import json #được dùng để lưu trữ và thể hiện các dữ liệu có  cấu trúc.
import sys
from fastapi import FastAPI
app= FastAPI() ## gọi constructor và gán vào biến app
class DELIVERY:
    def __init__(self, delivery_id, name, address): #hàm khởi tạo, self là tham số đầu tiên của hàm __init__(). Đây là một tham chiếu đến đối tượng hiện tại của lớp và được sử dụng để truy cập các biến thuộc về lớp đó.
        self.delivery_id = delivery_id
        self.name = name
        self.address=address
    
    #có __ trước tên thì đó là để khai báo private,
    #%s thay thế cho giá trị của phương thức __str__ tạo nên đối  tượng đó.
    #Cả hai hàm str() và repr() đều được sử dụng để lấy về dạng thức kiểu string của một đối tượng
    def __str__(self): 
        return f"delivery_id: {self.delivery_id}\n name: {self.name}\n address: {self.address}"
class dishType:
    def __init__(self, delivery_id, dish_type_id, dish_type_name):
        self.delivery_id = delivery_id
        self.dish_type_id = dish_type_id
        self.dish_type_name=dish_type_name
    def __str__(self):
        return f"delivery_id: {self.delivery_id}\ndish_type_id: {self.dish_type_id}\ndish_type_name: {self.dish_type_name}"
class DISH:
    def __init__(self, id, name, quantity, dish_type_id):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.dish_type_id = dish_type_id
    def __str__(self):
        return f"id: {self.id}\n name: {self.name}\n quantity: {self.quantity} \n dish_type_id: {self.dish_type_id}"
    
    
@app.get("/crawl_deliveries")
async def crawl_deliveries():
    # cào id quán ở đa nang
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
    # Lấy 5 delivery_id đầu tiên
    first_five_deliveries = delivery_ids[:5]
    print(first_five_deliveries)


    # cào thông tin cả 5 quán
    url = "https://gappapi.deliverynow.vn/api/delivery/get_browsing_infos"

    payload = json.dumps({
    "delivery_ids": first_five_deliveries,
    "city_id": 219,
    "sort_type": 2,
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
    delivery_infos = response.json()['reply']['delivery_infos']
    delivery_informations=[]
    for delivery_info in delivery_infos:
        delivery_id = delivery_info["id"]
        name = delivery_info["name"]
        address = delivery_info["address"]
        delivery = DELIVERY( delivery_id= delivery_id, name = name, address = address)
        delivery_informations.append(delivery)
    return {"message": "Data crawled and saved successfully", "data": delivery_informations}

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
    # Lấy 2 delivery đầu tiên
    first_five_deliveries = delivery_ids[:5]
    print(first_five_deliveries)
    # Lấy  menu quán 
    dish_types = []
    dishess= []
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
            maloaimon = menu_info["dish_type_id"]
            tenloaimon = menu_info["dish_type_name"]
            dishes = menu_info["dishes"]
            for dish in dishes:
                id = dish["id"]
                name = dish["name"]
                quantity = dish["quantity"]
                dish = DISH(id = id, name = name, quantity = quantity, dish_type_id = maloaimon)
                dishess.append(dish)
            dish_type = dishType(delivery_id= delivery_id, dish_type_id = maloaimon,dish_type_name = tenloaimon )
            dish_types.append(dish_type)
            # print(dish_type)
    return {"message": "Data crawled and saved successfully", "data": dishess}

# # Connect to MySQL database
# mydb = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     password="thuluyen",
#     database="foody_db"
# )
# mycursor = mydb.cursor()

# # Insert data into MySQL database
# for place in response.json()["Data"]["Place"]["Location"]:
#     name = place["Name"]
#     address = place["Address"]
#     phone = place["Phone"]
#     category = place["CategoryName"]
#     rating = place["AvgRating"]
#     num_reviews = place["TotalReview"]
#     sql = "INSERT INTO places (name, address, phone, category, rating, num_reviews) VALUES (%s, %s, %s, %s, %s, %s)"
#     val = (name, address, phone, category, rating, num_reviews)
#     mycursor.execute(sql, val)
# mydb.commit()

# # Close MySQL connection
# mycursor.close()
# mydb.close()
