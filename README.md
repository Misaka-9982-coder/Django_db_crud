#### 界面效果
![请添加图片描述](https://img-blog.csdnimg.cn/c0ef56f5af854a2a95cdaf7768432e64.gif)
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

在数据库中设置好存储过程

```sql
/*
    存储过程
    创建 按照所有交易总租赁奢侈包总天数排序 显示客户
*/
delimiter //
create procedure best_customers()
begin 
    select 
        last_name as 'Last Name',
        first_name as 'First Name',
        address as 'Address',
        phone as 'Telephone',
        ifnull(sum(datediff( date_returned, date_rented)), 0) 
            as 'Total Length of Rentals' 
    from customer as c 
    left join rentals as r 
    on c.cid = r.cid 
    group by c.cid 
    order by `Total Length of Rentals` desc;
end //
delimiter;
```

在 `urls.py` 文件中设置好路由

```python
path('best_customer', views.best_customer, name="best_customer"),
```

在`views.py`文件中定义好 `best_customer` 函数

```python
def best_customer(request):

    # 调用存储过程，返回前端
    cur = connection.cursor()
    cur.callproc("best_customers")
    datas = cur.fetchall()
    return render(request, 'home/best_customer.html', locals())
```

创建如下前端页面

![image-20211214102433196](/img/image-20211214102433196.png)

##### 编写一个程序来计算和列出每个顾客的消费金额。放映这个包租出去的天数

在数据库中设置好存储过程

```sql
/*
    存储过程
    按照用户 id 计算 用户每个租赁交易应支付 账单金额 从大到小排序
    传入参数为用户 id
*/
delimiter //
create procedure report_customer_amount(in customer_id int(32))
begin
    select 
        c.last_name as 'Last Name',
        c.first_name as 'First Name',
        d.name as 'Manufacturer',
        b.btype as 'Name',
        datediff( r.date_returned, r.date_rented) as 'totalDays',
        (d.price + r.optional_insurance) 
            * datediff( r.date_returned, r.date_rented) as 'Cost'
    from rentals as r 
    left join customer as c 
    on r.cid = c.cid 
    left join bag as b 
    on r.bid = b.bid 
    left join designer as d 
    on d.did = b.did 
    where r.cid = customer_id
    order by Cost desc;
    
end //
delimiter;

-- call report_customer_amount(17);



/*
    存储过程
    按照用户 id 计算 用户所有租赁交易应支付 账单金额 
    传入参数为用户 id
*/
delimiter //
create procedure report_customer_totalCost(in customer_id int(32))
begin
    select 
        c.last_name as 'Last Name',
        c.first_name as 'First Name',
        sum((d.price + r.optional_insurance) 
            * datediff( r.date_returned, r.date_rented)) as totalCost
    from rentals as r 
    left join customer as c 
    on r.cid = c.cid 
    left join bag as b 
    on r.bid = b.bid 
    left join designer as d 
    on d.did = b.did 
    where r.cid = customer_id;
end //
delimiter;
```

在 `urls.py` 文件中设置好路由

```python
path('customers_amount', views.customers_amount, name="customers_amount"),
```

在`views.py`文件中定义好 `customers_amount` 函数

```python
@login_required(login_url="/login/")
def customers_amount(request):
    msg = None
    success = True

    if request.method == "GET":

        # 获取前端输入的用户 id
        customer_id = request.GET.get('customer_id')
        if customer_id is not None: 

            # 输入的 id 为 str 类， 应该强制类型转换
            id = int(customer_id)

            # 执行存储过程， 获取所有的 用户 id
            cur = connection.cursor()
            cur.callproc('get_customers_id')
            data = cur.fetchall()
            cur.close()

            # 将所有用户 id 存进元组
            ids = []
            
            for da in data:
                ids.append(da[0])

            if id is not None:
                if id in ids:
                    # 这个用户 id 存在
                    success = True
                else:
                    success = False
            
                if success:
                    cur2 = connection.cursor()
                    cur3 = connection.cursor()

                    # 获取该用户所有租赁信息
                    cur2.callproc('report_customer_amount', (id,))

                    # 获取该用户所有租赁账单总金额
                    cur3.callproc('report_customer_totalCost', (id,))

                    amounts = cur2.fetchall()
                    totalCosts = cur3.fetchall()
                    cur2.close()
                    cur3.close()

                    cost = totalCosts[0][2]
                    msg = "The customer whose id is " + customer_id + "'s bill"
                else:
                    msg = "The customer whose id is " + customer_id + " doesn't exits"
    
    return render(request, 'home/customers_amount.html', locals())
```

创建如下前端页面：

![image-20211214103336986](/img/image-20211214103336986.png)

输入客户id，得如下结果

![image-20211214103251551](/img/image-20211214103251551.png)

异常情况测试

![image-20211214103523450](/img/image-20211214103523450.png)



##### 添加包

存储过程

```sql
/*
    存储过程
    新建一个奢侈品背包
    传入参数为  包的类型， 包的颜色， 包的设计者
*/
delimiter //
create procedure add_bag(bagType varchar(30), bagColor varchar(10), bagDesigner varchar(30))
begin
    insert into bag( btype, color, did) 
    values ( bagType, bagColor, (select did 
                                from designer
                                where name = bagDesigner));
end //
delimiter;
```

在 `urls.py` 文件中设置好路由

```python
path('add_bag', views.add_bag, name="add_bag"),
```

在`views.py`文件中定义好 `add_bag` 函数

```python
@login_required(login_url="/login/")
def add_bag(request):
    msg = None
    flag = True
    success = True

    if request.method == "POST":

        # 获取前端输入的包包 信息
        bname = request.POST.get('bag_name')
        bcolor = request.POST.get('bag_color')

        dname = request.POST.get('designer_name')
        bprice = request.POST.get('price_per_day')
        
        try:
            # 将价格转为 浮点数
            dprice = float(bprice)
        except:
            msg = "please enter a current number"
            success = False


        if success:

            # 获取所有设计师名字
            cur = connection.cursor()
            cur.callproc('get_designers_name')
            data = cur.fetchall()
            cur.close()

            d_names = []
            for i in data:
                d_names.append(i[0])
            
            cur = connection.cursor()
            

            if dname in d_names:
                # 该设计师 存在
                cur.callproc('get_designer_price', (dname,),)
                data = cur.fetchall()
                price = data[0][0]

                # 价格不公道
                if dprice != price:
                    msg = "The price is not equal to this designer's price"
                    flag = False
            else:
                # 设计师不存在， 添加一个设计师
                cur.callproc('add_designer', (dname, dprice),)
            
            cur.close()

            if flag:

                # 添加包包
                cur = connection.cursor()
                cur.callproc("add_bag", (bname, bcolor, dname))
                cur.close()
                msg = 'Success - please <a href="/">return</a>.'

    return render(request, 'home/add_bag.html', locals())
```

创建如下前端页面

![image-20211214103903206](/img/image-20211214103903206.png)

添加包包

![image-20211214104018219](/img/image-20211214104018219.png)

添加成功

![image-20211214104111060](/img/image-20211214104111060.png)

在包包表格中可以看到如下信息

![image-20211214104244275](/img/image-20211214104244275.png)

##### 添加出租信息的表，租用日期是当前时间

包被退回的时候，显示出租的总时长和总金额，包可以再次被出租

存储过程

```sql
/*
    存储过程
    创建租赁交易记录
    传入参数为用户 id， 奢侈品 id， 是否支付保险， 租赁天数
*/
delimiter //
create  procedure add_rentals(customerId int(32), bagId int(32), optionalInsurance tinyint(1), daysOfRent int(10))
begin
    insert into rentals(cid, bid, date_rented, date_returned, optional_insurance) 
    values (customerId, bagId, curdate(), curdate() + daysOfRent, optionalInsurance);
    update bag set already_rented = 1 where bid = bagId;
end //
delimiter;
```

在 `urls.py` 文件中设置好路由

```python
path('rent_bag', views.rent_bag, name="rent_bag"),
path('mybag', views.mybag, name="mybag"),
```

在`views.py`文件中定义好 `rent_bag`、`mybag` 函数

```python
@login_required(login_url="/login/")
def rent_bag(request):

    msg = None
    success = True
    flag = True

    # bag 属性名
    data = Bag._meta.fields
    columns = [data[i].name for i in range(len(data))]

    # 获取所有包
    objs = Bag.objects.all()

    # 当前 user id
    uid = request.user.id
    
    # 获取 uid 对应的 customer 表信息
    customer = Customer.objects.filter(uid = uid).first()

    if customer is None: 
        # 当前用户 没有补充个人信息
        flag = False
        msg = 'Please improve your personal information - <a href="/customer_register"> Profile </a>'
        success = False

    if flag:
        # 获取 cid 
        cid = customer.cid
        if request.method == "POST":

            # 获取前端返回的 信息
            bagid = request.POST.get("bag_id")
            days = request.POST.get("days")
            insurance = request.POST.get("insurance")

            cur = connection.cursor()
            try:

                # 添加租赁信息 
                cur.callproc('add_rentals', (cid, bagid, insurance, days),)
                msg = "Rent bag: " + bagid + " Success"
            except:

                # 存储过程执行可能会遇到些问题，为解决
                msg = "Please enter how many days you want to rent"
                success = False
       
    return render(request, 'home/rent_bag.html', locals())



@login_required(login_url="/login/")
def mybag(request):
    msg = None
    success = True

    # 获取 已经租出去的 包包
    bags = Bag.objects.filter(already_rented = 1)
    bids = []
    for bag in bags:
        bids.append(bag.bid)

    # uid 
    uid = request.user.id

    # 当前 user 的 customer 信息
    customer = Customer.objects.filter(uid = uid).first()
    cid = customer.cid

    if customer is None:

        # 当前用户未补充个人信息
        msg = 'Please improve your personal information - <a href="/customer_register"> Profile </a>'
        return render(request, 'home/page-404.html', locals())
    else:

        # 获取 被租出的包的信息
        rentals = Rentals.objects.filter(bid__in=bids)

        # 按照 归还日期从大到小排序
        rents = list(rentals.filter(cid = cid).order_by("-date_returned"))
        
        ids = []
        bids = []

        # 对租赁账单信息去重， 只保留归还日期最新的
        for rent in rents:
            if rent.bid.bid not in bids:
                bids.append(rent.bid.bid)
                ids.append(rent.bid)


        if request.method == "POST":

            # 获取要归还的包包的 bid
            bid = request.POST.get("bag_id")    

            # 获取对应账单的信息
            rids = list(rentals.filter(cid = cid, bid = bid).order_by("-date_returned"))
            rid = rids[0].rid

            cur = connection.cursor()
            
            # ids 元组中存在的 归还的 bid 删去
            for id in ids:
                print(id)
                if id.bid == int(bid):
                    ids.remove(id)

            cur.callproc("turnBack", (rid,),)

            # 获取触发器返回的信息            
            data = cur.fetchall()
            cur.close()

            days = data[0][0]
            bill = data[0][1]
            msg = data
            msg = "The bag id : " + str(bid) + ", total days you rent it : " + str(days) + ", the bill you should pay : $" + str(bill)
            
        return render(request, 'home/mybag.html', locals())
```

触发器

```sql
/*
    触发器
    创建会话变量 totalDays，bill
    totalDays   记录总的租赁天数
    bill        记录租赁期间应付账单金额
    update      语句更新包的租赁状态
    退回包包后可以通过执行 select 语句获取会话变量的值
*/
delimiter //
create trigger returnBag after update on rentals for each row 
begin 
    declare pricePerday double(10,2);
    set @totalDays = 0;
    set @bill = 0.00;
    if new.date_returned then 
        select 
            price into pricePerday 
            from bag as b, designer d
            where b.bid = new.bid
            and b.did = d.did;
        select 
            datediff(new.date_returned, new.date_rented) into @totalDays;
        select 
            (pricePerday + new.optional_insurance) * @totalDays into @bill;
    end if;
    update bag set already_rented = false where bid = new.bid;
end //
delimiter;
```

租包

![image-20211214110959086](/img/image-20211214110959086.png)

成功

![image-20211214111030324](/img/image-20211214111030324.png)

租赁账单信息

![image-20211214111127429](/img/image-20211214111127429.png)

个人已租包包信息

![image-20211214111335407](/img/image-20211214111335407.png)

退回

![image-20211214111900596](/img/image-20211214111900596.png)
