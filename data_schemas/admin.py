from django.contrib import admin
from data_schemas.models import SchemaColumn, Schema, DataType, DataSet


admin.site.register(Schema)
admin.site.register(SchemaColumn)
admin.site.register(DataType)
admin.site.register(DataSet)

