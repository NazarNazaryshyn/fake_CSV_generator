import datetime
import random
import csv
import uuid
import time

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from data_schemas.models import Schema, SchemaColumn, DataType, DataSet


# Dictionary to determine csv string characters and column separators
csv_character = {
    'DoubleQuote': '"',
    'SingleQuote': "'",
    'Comma': ',',
    'Tab': "\t",
    'SemiColon': ';',
    'Pipe': '|'
}


# Dictionary with data for csv generation
data_types_random_value = {
    "Date": ["May 10, 1992", "August 3, 1987", "November 22, 2001", "July 17, 1998", "January 4, 2004",
             "September 19, 1995", "March 8, 1989", "December 12, 2008", "April 29, 1991", "October 2, 1997"],
    "Address": ["1234 Main Street, Anytown, USA", "5678 Elm Street, Somewhere, USA", "9101 Pine Avenue, Anywhere, USA",
                "2345 Maple Road, Nowhere, USA", "6789 Oak Lane, Everywhere, USA", "1111 Cherry Street, Here, USA",
                "2222 Magnolia Avenue, There, USA", "3333 Cedar Boulevard, Anyplace, USA",
                "4444 Birch Lane, Someplace, USA", "5555 Willow Way, Everywhere, USA"],
    "Text": ["The quick brown fox jumps over the lazy dog.", "A penny saved is a penny earned.",
             "The early bird catches the worm.", "All work and no play makes Jack a dull boy.",
             "The sky is the limit.", "Actions speak louder than words.",
             "You can't judge a book by its cover.", "When life gives you lemons, make lemonade."],
    "Company name": ["Facebook", "Google", "Amazon", "SparkleTech", "BluePeak", "SwiftWorks",
                     "GreenScape", "DreamWorks Inc.", "Silverline Solutions", "BrightStar Corporation"],
    "Phone number": ["+380 67 123 4567", "+380 63 987 6543", "+380 99 456 7890", "+380 98 765 4321",
                     "+380 73 456 7891", "+380 66 789 0123", "+380 50 123 4567", "+380 68 901 2345"],
    "Domain name": ["sparrowcloud.com", "bluemermaid.net", "greentiger.org", "yellowbutterfly.io",
                    "silverdolphin.co", "redfoxtech.biz", "purpleowlpro.com", "orangecatstudios.net",
                    "bluewhalecreative.org", "goldenlionagency.co"],
    "Email": ["johnsmith85@gmail.com", "sarahbrown23@yahoo.com", "davidlee42@hotmail.com",
              "emilyjones98@outlook.com", "robertwilson76@gmail.com", "jenniferbaker87@icloud.com",
              "adamclark54@yahoo.com", "lauramiller32@hotmail.com", "kevinwhite61@outlook.com",
              "melissagreen19@gmail.com"],
    "Job": ["Accountant", "Software Developer", "Graphic Designer", "Lawyer", "Sales Representative",
            "Chef", "Nurse", "Marketing Manager", "Electrician", "Physical Therapist"],
    "Full name": ["Michaela Thompson", "William Rodriguez", "Natasha Patel", "Benjamin Lee", "Olivia Carter",
                  "Isaac Davis", "Emma Jackson", "Aaron Cooper", "Samantha Wright", "Christopher Kim"]
}


# View to create new schema
def new_schema(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        new_schema = Schema(
                            owner=request.user,
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
    return render(request, "data_schemas/new_schema.html", {"data_types": data_types})


# Data sets view
def data_sets(request: HttpRequest, pk: int) -> HttpResponse:
    schema = Schema.objects.filter(id=pk).first()
    schema_columns = SchemaColumn.objects.filter(schema=schema).all()
    return render(request, "data_schemas/data_sets.html", {
                                                           "schema": schema,
                                                           "schema_columns": schema_columns
                                                           })


# View to generate csv with fake data
def generate_data(request: HttpRequest) -> JsonResponse:
    schema_id = int(request.GET.get('schema_id'))
    column_separator = request.GET.get('column_separator')
    string_character = request.GET.get('string_character')
    rows = int(request.GET.get('rows_amount'))

    schema = Schema.objects.filter(id=schema_id).first()
    schema_cols = SchemaColumn.objects.filter(schema_id=schema_id).order_by('order').all()

    unique_id = uuid.uuid4()

    new_data_set = DataSet(
        status=False,
        schema=schema,
        unique_id=unique_id
    )
    new_data_set.save()

    time.sleep(0.5)

    csv_headers = [header.column_name for header in schema_cols]
    data_type_rows = [type.data_type for type in schema_cols]

    with open(f'media/{unique_id}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=csv_character[column_separator],
                            quotechar=csv_character[string_character],
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["#", *csv_headers])
        for index in range(rows):
            for _ in schema_cols:
                row = [random.choice(data_types_random_value[str(header)]) if str(header) != "Integer"
                       else random.randint(18, 60) for header in data_type_rows]
            writer.writerow([index, *row])

    new_data_set.status = True
    new_data_set.save()

    data = {
        "created_at": new_data_set.created_at,
        "status": new_data_set.status,
        "unique_id": new_data_set.unique_id
    }

    return JsonResponse({"status": data})


# View to download csv by its unique_id
def download_csv(request: HttpRequest, unique_id: int) -> HttpResponse:
    file_path = f'media/{unique_id}.csv'
    with open(file_path, 'r') as f:
        csv_data = f.read()
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{unique_id}.csv"'

    return response


# View to delete schema by its id
def delete_schema(request: HttpRequest, schema_id: int) -> JsonResponse:
    Schema.objects.filter(id=schema_id).delete()

    return JsonResponse({"status": "deleted"})


# View to delete user's data sets
def delete_all_sets(request: HttpRequest) -> JsonResponse:
    DataSet.objects.filter(schema_id=(request.GET.get("schema_id"))).delete()

    return JsonResponse({"status": "deleted"})


# View to edit user's schemas
def edit_schema(request: HttpRequest, pk: int) -> HttpResponse:
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


# Main page with all user's schemas
def data_schemas(request: HttpRequest) -> HttpResponse:
    data_schemas = Schema.objects.filter(owner=request.user).all()

    return render(request, "data_schemas/data_schemas.html", {'schemas': data_schemas})


