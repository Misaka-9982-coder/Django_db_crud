### 模板源自[Appseed](https://appseed.us/) 的 [Datta Able Django](https://appseed.us/admin-dashboards/django-datta-able)

在`setting.py`中修改默认数据库

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

在命令行中输入以下命令
```
# 安装 mysql 驱动
sudo pip3 install pymysql
# 安装 simpleui
sudo pip3 install django-simpleui
```

加载`lab4.sql`文件导入数据库

配置`Django`环境

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

**ER图** 如下：

![image-20211213230607677](/img/image-20211213230607677.png)

Navicat 模型图如下：

![](/img/image-20211213230919977.png)



#### 需求及功能 ：

  1. 通过设计师名字 检索出该设计师设计过多少包
  2. 查询每个客户每个客户所有手袋的租赁时间。
  3. 编写一个程序来计算和列出每个顾客的消费金额。放映这个包租出去的天数
  4. 添加出租信息的表和包表，租用日期是当前时间
  5. 包被退回的时候，显示出租的总时长和总金额，包可以再次被出租
  6. 为所有异常设计并显示适当的消息

#### 存储过程设计

```sql
 --返回所有表的表名
show_all_tables()				

--传入表名，返回指定表的数据	   
show_table(tableName) 			

--传入表名，返回指定表的表头字段
show_columns_from_table(tableName)

--获取所有客户id
get_customers_id()	

--获取所有设计师名字		  
get_designers_name()				 

--传入设计师名字，获取指定设计师设计的背包
bag_by_designer(designer)			

--按照客户租赁所有包包的总天数排序显示客户
best_customers()					    

--传入用户id，根据用户id计算用户每个租赁交易应支付金额
report_customer_amount(customer_id)	

--传入用户id，根据用户id计算用户所有租赁交易应支付总额
report_customer_totalCost(customer_id)

--传入用户id，包包id，是否支付保险，租用天数，添加一笔租赁交易
add_rentals(customerId, bagId, optionalInsurance, daysOfRent)

--传入包包类型，颜色，设计者，添加一个可以租赁的包包    
add_bag(bagType, bagColor, bagDesigner)

--传入设计师的名字， 每个包包的价格， 添加一个设计师   
add_designer(dname, price)		

--传入客户姓氏，名字, 地址，电话号码，邮箱地址，信用卡号码，性别
add_customer(lname,fname, addr, pnum ,email, cnum, gender)
									            
.....
详见 lab4.sql 文件
```

#### 触发器设计

```
returnBag 	
-- 退回包包的时候，该包包的状态应该恢复可以租借
-- 在触发器中设置 totalDays 记录总租借日期 ， bill 记录总的账单金额
-- 退回包包的时候 通过调用select @totalDays, @bill 来获取这两个值

```

#### 功能设计

##### 1. 通过设计师名字 检索出该设计师设计过多少包

在数据库中设置好存储过程

```sql
/*
    存储过程
    创建显示每个设计师设计了多少包
    传入参数  designer  为该设计师名字
*/
delimiter //
create procedure bag_by_designer(in designer varchar(30))
begin
    select 
        btype as 'Name', 
        color as 'Color', 
        d.name as 'Manufacturer' 
    from bag as b
    left join designer as d
    on b.did = d.did
    where d.name = designer;
end //
delimiter;
```

在 `urls.py` 文件中设置好路由

```python
path('bag_views', views.bag_views, name="bags_views"),
```

在`views.py`文件中定义好 `bag_views` 函数

```python
def bag_views(request):

    # 记录信息， 返回前端
    msg = None
    success = True

    if request.method == "GET":

        # 获取设计师 姓名
        name = request.GET.get('designer_name')
        cur = connection.cursor()

        # 获取所有设计师姓名
        cur.callproc('get_designers_name')
        data = cur.fetchall()
        
        # 将所有设计师姓名存进元组
        names = []
        
        for da in data:
            names.append(da[0])

        if name is not None:

            # 该姓名存在
            if name in names:
                success = True
            else:
                success = False
        
            if success:

                # 执行存储过程，获取该设计师所有的包包
                cur2 = connection.cursor()
                cur2.callproc('bag_by_designer', (name,))
                objss = cur2.fetchall()

                msg = name + "'s bags are all here"
            else:
                msg = "Designer " + name + " doesn't exits"
        

    return render(request, 'home/bag_views.html', locals())
```

创建如下前端页面：

![image-20211213232908806](/img/image-20211213232908806.png)

输入设计师 Coach 的名字，得如下结果：

![image-20211213233003406](/img/image-20211213233003406.png)

异常测试：

![image-20211213233109973](/img/image-20211213233109973.png)

##### 输入客户 id 查询每个客户每个客户所有手袋的租赁时间。



在 `urls.py` 文件中设置好路由

```python
path('best_customer', views.best_customer, name="best_customer"),
```

在 `urls.py` 文件中设置好路由

```python
path('customers_amount', views.customers_amount, name="customers_amount"),
```

在 `urls.py` 文件中设置好路由

```python
path('add_bag', views.add_bag, name="add_bag"),
```

在 `urls.py` 文件中设置好路由

```python
path('rent_bag', views.rent_bag, name="rent_bag"),
```

在 `urls.py` 文件中设置好路由

```python
path('mybag', views.mybag, name="mybag"),
```

