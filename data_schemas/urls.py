from django.urls import path
from data_schemas.views import new_schema, data_sets, DataSchemas, generate_data, download_csv, \
                               delete_schema, delete_all_sets, check_for_processing, edit_schema

urlpatterns = [
    path('', DataSchemas.as_view(), name='data_schemas'),
    path('new/', new_schema, name='new_schema'),
    path('data_sets/<int:pk>', data_sets, name='data_sets'),
    path('data_sets/generate_data/', generate_data),
    path('data_sets/<unique_id>', download_csv),
    path('<int:schema_id>/', delete_schema),
    path('data_sets/delete_all/', delete_all_sets),
    path('data_sets/check_for_processing/', check_for_processing),
    path('edit_schema/<int:pk>', edit_schema, name='edit_schema')
]
