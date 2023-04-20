CREATE DATABASE foody_db;
USE foody_db;

-- CREATE TABLE Delivery_Infos (
-- delivery_id varchar(15) NOT NULL PRIMARY KEY,
-- delivery_name nvarchar(200),
-- phones varchar(200),
-- delivery_address nvarchar(200),
-- rating float
-- );
-- CREATE TABLE Dish_Type (
-- dish_type_id varchar(15) NOT NULL PRIMARY KEY,
-- dish_type_name nvarchar(200),
-- delivery_id varchar(15) ,
-- foreign key (delivery_id) references Delivery_Infos(delivery_id)
-- );
CREATE TABLE Dishes (
dish_id varchar(15) NOT NULL PRIMARY KEY,
dish_name nvarchar(200),
price varchar(200) ,
d_description nvarchar(200),
dish_type_name nvarchar(200),
delivery_id varchar(200)
);


