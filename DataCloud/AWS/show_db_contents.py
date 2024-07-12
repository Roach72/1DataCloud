
from django.shortcuts import render, redirect


from .forms import (
    DatabaseConnectionForm
)
import mysql.connector

from django.contrib import messages



def db_connection(request):
    if request.method == 'POST':
        form = DatabaseConnectionForm(request.POST)
        if form.is_valid():
            endpoint = form.cleaned_data['endpoint']
            user = form.cleaned_data['user']
            port = form.cleaned_data['port']
            password = form.cleaned_data['password']
            dbname = form.cleaned_data['dbname']

            request.session['db_connection'] = {
                'endpoint': endpoint,
                'user': user,
                'port': port,
                'password': password,
                'dbname': dbname
            }

            return redirect('show_db_contents')
    else:
        form = DatabaseConnectionForm()

    return render(request, 'cloud/aws_pages/create_db_connection.html', {'form': form})

def get_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    return tables

def show_db_contents(request):
    db_connection = request.session.get('db_connection')
    if not db_connection:
        return redirect('db_connection')

    endpoint = db_connection['endpoint']
    user = db_connection['user']
    port = db_connection['port']
    password = db_connection['password']
    dbname = db_connection['dbname']

    try:
        connection = mysql.connector.connect(
            host=endpoint,
            user=user,
            password=password,
            database=dbname,
            port=port
        )
    except mysql.connector.Error as err:
        messages.error(request, f"Error connecting to the database: {err}")
        return redirect('db_connection')

    try:
        tables = get_tables(connection)
        db_contents = {}

        cursor = connection.cursor()
        try:
            for table in tables:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                db_contents[table] = rows
        except mysql.connector.Error as err:
            messages.error(request, f"Error fetching data from the table: {err}")
            return redirect('db_connection')
        finally:
            cursor.close()
    finally:
        connection.close()

    return render(request, 'cloud/aws_pages/db_contents.html', {'db_contents': db_contents})


