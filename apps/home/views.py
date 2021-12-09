# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.db import connection
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import *

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



# Create your views here.
# def add_stu(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         sex = request.POST.get('sex')
#         birthday = request.POST.get('birthday')

#         # 添加书籍记录，一对多
#         stu_obj = Student.objects.create(name=name, sex=sex, birthday=birthday)
        
#         return redirect('/tables')

#     students = Student.objects.all()
#     return render(request, 'home/addStudent.html', locals())



# '''删除操作'''
# @login_required(login_url="/login/")
# def delete_stu(request, delete_stu_id):
#     Student.objects.filter(id=delete_stu_id).delete()
#     students = Student.objects.all()
#     return render(request, 'home/tables.html', locals())



# '''编辑操作'''
# def change_stu(request, edit_stu_id):
#     stu_obj = Student.objects.filter(id=edit_stu_id).first()
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         sex = request.POST.get('sex')
#         birthday = request.POST.get('birthday')

#         # 更新书籍记录
#         Student.objects.filter(id=edit_stu_id).update(name=name, sex=sex, birthday=birthday)
#         return redirect('/tables')

#     return render(request, 'home/editStudent.html', locals())



'''展示数据表'''
@login_required(login_url="/login/")
def show(request):
    cur = connection.cursor()
    cur.callproc("show_columns_from_table", ("bag",))
    connection.connection.commit()
    data = cur.fetchall()
    t_name = []
    for i in data:
        t_name.append(i[0])
    cur.close()
    cur = connection.cursor()
    cur.callproc("show_table", ("bag",))
    data = cur.fetchall()
    t_body = []
    for i in data:
        t_body.append(i)
    return render(request, 'home/tables.html', locals())



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

        # students = models.Student.objects.all()
        # if load_template == 'tables':
        #     return render(request, 'home/tables.html', locals())

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
