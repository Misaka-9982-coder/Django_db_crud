# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    id = models.AutoField(primary_key=True) # id 会自动创建,可以手动写入
    name = models.CharField(max_length=32)  # 名称
    sex = models.CharField(max_length=32)   # 性别
    birthday = models.DateField()           # 出版时间