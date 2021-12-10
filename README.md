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

designer ( <u>id</u>, name, price)

bag ( <u>id</u>, designer_id, type, color, already_rented )

customer ( <u>id</u>, phone#, address, name, email, card#, gender)

lease ( <u>id</u>, bag_id, customer_id, start_date, back_date, insure_or_not )



需求 ：
      1. 通过设计师名字 检索出该设计师设计过多少包
      2. 查询每个客户每个客户所有手袋的租赁时间。
      3. 编写一个程序来计算和列出每个顾客的消费金额。放映这个包租出去的天数
      4. 添加出租表和包表，租用日期是当前时间
      5. 包被退回的时候，显示出租的总时长和总金额，包可以再次被出租
      6. 为所有异常设计并显示适当的消息