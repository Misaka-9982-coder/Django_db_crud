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




@login_required(login_url="/login/")
def customer_register(request):
    msg = None
    success = False
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            msg = 'Modified success  - please <a href="/"> Return </a>.'
            success = True
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            phone = form.cleaned_data.get("phone")
            addr = form.cleaned_data.get("address")
            email = form.cleaned_data.get("email")
            card = form.cleaned_data.get("card")
            gender = form.cleaned_data.get("gender")
            
            # return redirect("/")
            
            uid = request.user.id
            objs = Customer.objects.all()
            flag = 0
            for obj in objs:
                if uid == obj.uid:
                    flag = 1


            if flag:
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
            user = request.user.username
            password = form.cleaned_data.get("password")
            new_password = form.cleaned_data.get("password1")
            user = authenticate(username=user, password=password)

            user = None
            if user is not None:
                user.set_password(new_password)
                user.save()

                msg = 'Password Reseted - please <a href="/">return</a>.'
                success = True
            else:
                msg = 'Current Password error'
        else:
            msg = 'Form is not valid'
    else:
        form = ResetForm()

    return render(request, "home/reset-pass.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url="/login/")
def bag_views(request):

    msg = None
    success = True

    if request.method == "GET":
        name = request.GET.get('designer_name')
        cur = connection.cursor()


        cur.callproc('get_designers_name')
        data = cur.fetchall()
        
        names = []
        
        for da in data:
            names.append(da[0])

        if name is not None:
            if name in names:
                success = True
            else:
                success = False
        
            if success:
                cur2 = connection.cursor()
                cur2.callproc('bag_by_designer', (name,))
                objss = cur2.fetchall()

                msg = name + "'s bags are all here"
            else:
                msg = "Designer " + name + " doesn't exits"
        

    return render(request, 'home/bag_views.html', locals())



@login_required(login_url="/login/")
def best_customer(request):
    cur = connection.cursor()
    cur.callproc("best_customers")
    datas = cur.fetchall()
    return render(request, 'home/best_customer.html', locals())



@login_required(login_url="/login/")
def customers_amount(request):
    msg = None
    success = True

    if request.method == "GET":
        customer_id = request.GET.get('customer_id')
        if customer_id is not None: 
            id = int(customer_id)
            cur = connection.cursor()

            cur.callproc('get_customers_id')
            data = cur.fetchall()
            
            ids = []
            
            for da in data:
                ids.append(da[0])

            if id is not None:
                if id in ids:
                    success = True
                else:
                    success = False
            
                if success:
                    cur2 = connection.cursor()
                    cur3 = connection.cursor()

                    cur2.callproc('report_customer_amount', (id,))
                    cur3.callproc('report_customer_totalCost', (id,))

                    amounts = cur2.fetchall()
                    totalCosts = cur3.fetchall()
                    cost = totalCosts[0][2]
                    msg = "The customer whose id is " + customer_id + "'s bill"
                else:
                    msg = "The customer whose id is " + customer_id + " doesn't exits"
    
    return render(request, 'home/customers_amount.html', locals())


    

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
