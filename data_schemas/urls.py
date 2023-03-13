from django.urls import path
from data_schemas.views import new_schema, data_sets, data_schemas, generate_data, download_csv, \
                               delete_schema, delete_all_sets, edit_schema

urlpatterns = [
    path('', data_schemas, name='data_schemas'),
    path('new/', new_schema, name='new_schema'),
    path('data_sets/<int:pk>', data_sets, name='data_sets'),
    path('data_sets/generate_data/', generate_data, name='generate_data'),
    path('data_sets/<unique_id>', download_csv, name='download_csv'),
    path('<int:schema_id>/', delete_schema, name='delete_schema'),
    path('data_sets/delete_all/', delete_all_sets, name='delete_all_sets'),
    path('edit_schema/<int:pk>', edit_schema, name='edit_schema')
]
