```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名称',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```



```
$ pip install virtualenv
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port 
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

#### 数据表设计

designer ( <u>id</u>, name, price)

bag ( <u>id</u>, designer_id, type, color, already_rented )

customer ( <u>id</u>, phone#, address, name, email, card#, gender)

lease ( <u>id</u>, bag_id, customer_id, start_date, back_date, insure_or_not )



#### 需求及功能 ：

  1. 通过设计师名字 检索出该设计师设计过多少包
  2. 查询每个客户每个客户所有手袋的租赁时间。
  3. 编写一个程序来计算和列出每个顾客的消费金额。放映这个包租出去的天数
  4. 添加出租表和包表，租用日期是当前时间
  5. 包被退回的时候，显示出租的总时长和总金额，包可以再次被出租
  6. 为所有异常设计并显示适当的消息

#### 存储过程设计

```sql
show_all_tables()					--返回所有表的表名
show_table(tableName) 				--传入表名，返回指定表的数据
show_columns_from_table(in tableName varchar(30))
									--传入表名，返回指定表的表头字段
get_customers_id()					--获取所有客户id
get_designers_name()				--获取所有设计师名字
bag_by_designer(in designer varchar(30))
									--传入设计师名字，获取指定设计师设计的背包
best_customers()					--按照客户租赁所有包包的总天数排序显示客户
report_customer_amount(in customer_id int(32))
									--传入用户id，根据用户id计算用户每个租赁交易应支付金额
report_customer_totalCost(in customer_id int(32))
									--传入用户id，根据用户id计算用户所有租赁交易应支付总额
add_rentals(customerId int(32), bagId int(32), optionalInsurance tinyint(1), daysOfRent int(10))
									--传入用户id，包包id，是否支付保险，租用天数，添加一笔租赁交易
add_bag(bagType varchar(30), bagColor varchar(10), bagDesigner varchar(30))
									--传入包包类型，颜色，设计者，添加一个可以租赁的包包
```

