from django.db import models
from django.contrib.auth.models import User

import datetime


class Schema(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    column_separator = models.CharField(max_length=50)
    string_character = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=datetime.datetime.now())
    updated_at = models.DateField(auto_now_add=datetime.datetime.now())

    def __str__(self):
        return f"Title - {self.title}. Owner - {self.owner}"


class DataType(models.Model):
    column_type = models.CharField(max_length=50)

    def __str__(self):
        return self.column_type


class SchemaColumn(models.Model):
    column_name = models.CharField(max_length=250)
    order = models.IntegerField()
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=datetime.datetime.now())
    updated_at = models.DateField(auto_now_add=datetime.datetime.now())

    def __str__(self):
        return self.column_name


class DataSet(models.Model):
    status = models.BooleanField(default=False)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=datetime.datetime.now())
    unique_id = models.CharField(unique=True, max_length=500, default='')

