import boto3
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AWSConnectionForm


def database_details(request, db_type, db_identifier):
    aws_credentials = request.session.get('aws_credentials')
    if not aws_credentials:
        messages.error(request, "Please enter your AWS credentials.")
        return redirect('aws_connection')

    aws_access_key_id = aws_credentials['aws_access_key_id']
    aws_secret_access_key = aws_credentials['aws_secret_access_key']
    aws_region = aws_credentials['aws_region']

    try:
        if db_type == 'RDS':
            client = boto3.client('rds', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_db_instances(DBInstanceIdentifier=db_identifier)
            db_details = response['DBInstances'][0]
        elif db_type == 'DocumentDB':
            client = boto3.client('docdb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_db_clusters(DBClusterIdentifier=db_identifier)
            db_details = response['DBClusters'][0]
        elif db_type == 'DynamoDB':
            client = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_table(TableName=db_identifier)
            db_details = response['Table']
        elif db_type == 'ElastiCache':
            client = boto3.client('elasticache', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_cache_clusters(CacheClusterId=db_identifier)
            db_details = response['CacheClusters'][0]
        elif db_type == 'MemoryDB':
            client = boto3.client('memorydb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_clusters(ClusterName=db_identifier)
            db_details = response['Clusters'][0]
        elif db_type == 'Neptune':
            client = boto3.client('neptune', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_db_clusters(DBClusterIdentifier=db_identifier)
            db_details = response['DBClusters'][0]
        elif db_type == 'QLDB':
            client = boto3.client('qldb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_ledger(Name=db_identifier)
            db_details = response['Ledger']
        elif db_type == 'Timestream':
            client = boto3.client('timestream-write', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
            response = client.describe_table(DatabaseName='YourDatabaseName', TableName=db_identifier)
            db_details = response['Table']
        else:
            db_details = None

    except Exception as e:
        messages.error(request, f"Error retrieving database details: {e}")
        return redirect('show_aws_databases')

    return render(request, 'cloud/aws_pages/database_details.html', {'db_type': db_type, 'db_details': db_details})