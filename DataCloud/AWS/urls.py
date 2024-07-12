# AWS/urls.py
from django.urls import path
from . import views
from . import show_aws_databases
from . import show_db_contents
from . import database_details

urlpatterns = [
    path('AWS/', views.choose_database_service, name='AWS'),
    path('AWS/create/<str:service_name>/', views.create_aws_instance, name='create_aws_instance'),
    path('AWS/success/', views.success, name='success_url'),

    path('AWS/connection/', show_db_contents.db_connection, name='db_connection'),
    path('AWS/show-contents/', show_db_contents.show_db_contents, name='show_db_contents'),

    path('aws_connection/', show_aws_databases.aws_connection, name='aws_connection'),
    path('show_aws_databases/', show_aws_databases.show_aws_databases, name='show_aws_databases'),

    path('database_details/<str:db_type>/<str:db_identifier>/', database_details.database_details, name='database_details'),



]