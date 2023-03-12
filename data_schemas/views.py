import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from data_schemas.models import Schema, SchemaColumn, DataType, DataSet

import csv
import uuid


csv_character = {
    'DoubleQuote': '"',
    'SingleQuote': "'",
    'Comma': ',',
    'Tab': "\t",
    'SemiColon': ';',
    'Pipe': '|'
}


def new_schema(request):
    if request.method == "POST":
        new_schema = Schema(owner=request.user,
                            title=request.POST.get('schema_title'),
                            column_separator=request.POST.get('schema_column_separator'),
                            string_character=request.POST.get('schema_string_character')
                            )
        new_schema.save()

        for index, column in enumerate(request.POST.getlist('column_name')):

            if column == "":
                continue
            else:
                data_type = DataType.objects.filter(column_type=request.POST.getlist('column_type')[index]).first()
                new_column = SchemaColumn(
                                          column_name=request.POST.getlist('column_name')[index],
                                          schema=new_schema,
                                          order=request.POST.getlist('column_order')[index],
                                          data_type=data_type,
                                          )
                new_column.save()
        return redirect('data_sets', new_schema.id)

    data_types = DataType.objects.all()
    return render(request, "data_schemas/new_schema.html",
                  {"data_types": data_types})


def data_sets(request, pk):
    schema = Schema.objects.filter(id=pk).first()
    schema_columns = SchemaColumn.objects.filter(schema=schema).all()
    return render(request, "data_schemas/data_sets.html", {"schema": schema,
                                                           "schema_columns": schema_columns})


def generate_data(request):
    schema_id = int(request.GET.get('schema_id'))
    column_separator = request.GET.get('column_separator')
    string_character = request.GET.get('string_character')
    rows = int(request.GET.get('rows_amount'))

    schema = Schema.objects.filter(id=schema_id).first()
    schema_cols = SchemaColumn.objects.filter(schema_id=schema_id).order_by('order').all()

    items_list = []
    for item in range(rows):
        unique_id = uuid.uuid4()

        new_data_set = DataSet(
            status=False,
            schema=schema,
            unique_id=unique_id
        )
        new_data_set.save()

        items_list.append({"id": item + 1,
                           "created_at": new_data_set.created_at,
                           "status": new_data_set.status,
                           "unique_id": new_data_set.unique_id})

        import time
        time.sleep(0.5)

        with open(f'media/{unique_id}.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter=csv_character[column_separator],
                                quotechar=csv_character[string_character],
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["#", "Column name", "Column type"])
            for index, item in enumerate(schema_cols):
                writer.writerow([index + 1, item.column_name, item.data_type])

        new_data_set.status = True
        new_data_set.save()

    return JsonResponse({"status": items_list})


def download_csv(request, unique_id):
    file_path = f'media/{unique_id}.csv'
    with open(file_path, 'r') as f:
        csv_data = f.read()
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{unique_id}.csv"'

    return response


def check_for_processing(request):

    items = DataSet.objects.filter(schema_id=int(request.GET.get('schema_id'))).all()
    items_list = []

    for item in items:
        if item.status:
            items_list.append({
                               "id": item.id,
                               "status": item.status,
                               "unique_id": item.unique_id
                               })

    return JsonResponse({"status": items_list})


def delete_schema(request, schema_id):
    Schema.objects.filter(id=schema_id).delete()

    return JsonResponse({"status": "deleted"})


def delete_all_sets(request):
    DataSet.objects.filter(schema_id=(request.GET.get("schema_id"))).delete()

    return JsonResponse({"status": "deleted"})


def edit_schema(request, pk):
    schema = Schema.objects.filter(id=pk).first()
    schema_columns = SchemaColumn.objects.filter(schema=schema).all()
    data_types = DataType.objects.filter().all()

    if request.method == "POST":
        schema.title = request.POST.get('schema_title')
        schema.column_separator = request.POST.get('schema_column_separator')
        schema.string_character = request.POST.get('schema_string_character')
        schema.updated_at = datetime.datetime.now()

        schema.save()

        SchemaColumn.objects.filter(schema=schema).delete()

        for index, col in enumerate(request.POST.getlist('column_name')):
            data_type = DataType.objects.filter(column_type=request.POST.getlist('column_type')[index]).first()
            new_col = SchemaColumn(
                column_name=col,
                schema=schema,
                order=request.POST.getlist('column_order')[index],
                data_type=data_type,
            )

            new_col.save()

        return redirect('data_schemas')

    return render(request, "data_schemas/edit_schema.html", {'schema': schema,
                                                             'schema_columns': schema_columns,
                                                             'data_types': data_types})


class DataSchemas(ListView):
    model = Schema
    template_name = "data_schemas/data_schemas.html"
    context_object_name = "schemas"

    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user).all()
