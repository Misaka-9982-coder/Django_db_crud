from datetime import datetime
import time
from django.contrib.auth import authenticate
from .forms import SignUpForm, ResetForm


from django.db import connection
from django.db.models.base import Model
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import *




# Create your views here.


# index 页面， 通过调用 存储过程来实现
@login_required(login_url="/login/")
def index(request):
    cur = connection.cursor()
    
    cur.callproc('get_total_sales')
    data = cur.fetchall()
    total = data[0][0]

    cur.callproc('get_cnt_table', ('rentals',))
    data = cur.fetchall()
    rent_amount = data[0][0]

    cur.callproc('get_cnt_table', ('designer',))
    data = cur.fetchall()
    designer_cnt = data[0][0]

    cur.callproc('get_cnt_table', ('bag',))
    data = cur.fetchall()
    bag_cnt = data[0][0]

    cur.callproc('get_cnt_table', ('customer',))
    data = cur.fetchall()
    customer_cnt = data[0][0]

    cus_obj = Customer.objects.all()
    
    return render(request, 'home/index.html', locals())
    # return HttpResponse(html_template.render(data, context, request))




'''展示数据表'''
@login_required(login_url="/login/")
def show_bags(request):
    data = Bag._meta.fields
    columns = [data[i].name for i in range(len(data))]
    objs = Bag.objects.all()
    return render(request, 'home/bags_table.html', locals())



@login_required(login_url="/login/")
def show_bags(request):
    data = Bag._meta.fields
    columns = [data[i].name for i in range(len(data))]
    objs = Bag.objects.all()
    return render(request, 'home/bags_table.html', locals())



@login_required(login_url="/login/")
def show_designers(request):
    data = Designer._meta.fields
    columns = [data[i].name for i in range(len(data))]
    objs = Designer.objects.all()
    return render(request, 'home/designers_table.html', locals())



@login_required(login_url="/login/")
def show_customers(request):
    data = Customer._meta.fields
    columns = [data[i].name for i in range(len(data))]
    objs = Customer.objects.all()
    return render(request, 'home/customers_table.html', locals())


@login_required(login_url="/login/")
def show_rentals(request):
    data = Rentals._meta.fields
    columns = [data[i].name for i in range(len(data))]
    objs = Rentals.objects.all()
    return render(request, 'home/rentals_table.html', locals())



# 注册用户
@login_required(login_url="/login/")
def customer_register(request):
    msg = None
    success = False
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            msg = 'Modified success  - please <a href="/"> Return </a>.'
            success = True

            # 获取前端返回数据
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            phone = form.cleaned_data.get("phone")
            addr = form.cleaned_data.get("address")
            email = form.cleaned_data.get("email")
            card = form.cleaned_data.get("card")
            gender = form.cleaned_data.get("gender")
            
            # return redirect("/")
            
            # 获取当前 user 的 id ，查看该 user 是否补全个人信息
            uid = request.user.id
            objs = Customer.objects.all()
            
            # 标记该 user 是修改个人信息还是添加个人信息
            flag = 0
            for obj in objs:
                if uid == obj.uid:
                    flag = 1


            if flag:
                # 修改个人信息
                cust = Customer.objects.filter(uid = uid).first()
                cust.first_name = firstname
                cust.last_name = lastname
                cust.phone = phone
                cust.address = addr
                cust.email = email
                cust.card = card
                cust.gender = gender
                cust.save()               
            else:
                # 添加个人信息
                add_customer=Customer(first_name=firstname,
                    last_name=lastname, phone=phone,
                    address=addr, email=email,
                    card=card, gender= gender, uid=uid)
            
                add_customer.save()
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "home/register.html", {"form": form, "msg": msg, "success": success})



@login_required(login_url="/login/")
def reset_pass(request):
    msg = None
    success = False

    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():

            # 获取 用户名
            user = request.user.username
            password = form.cleaned_data.get("password")
            new_password = form.cleaned_data.get("password1")

            # 获取用户
            user = authenticate(username=user, password=password)


            if user is not None:
                #用户存在
                user.set_password(new_password)
                user.save()

                msg = 'Password Reseted - please <a href="/">return</a>.'
                success = True
            else:
                # 当前 旧密码 有误
                msg = 'Current Password error'
        else:
            msg = 'Form is not valid'
    else:
        form = ResetForm()

    return render(request, "home/reset-pass.html", {"form": form, "msg": msg, "success": success})



@login_required(login_url="/login/")
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



@login_required(login_url="/login/")
def best_customer(request):

    # 调用存储过程，返回前端
    cur = connection.cursor()
    cur.callproc("best_customers")
    datas = cur.fetchall()
    return render(request, 'home/best_customer.html', locals())



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



'''分页'''
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
