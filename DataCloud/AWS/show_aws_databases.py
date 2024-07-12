#AWS/show_aws_databases.py
import boto3
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AWSConnectionForm

def aws_connection(request):
    if request.method == 'POST':
        form = AWSConnectionForm(request.POST)
        if form.is_valid():
            aws_access_key_id = form.cleaned_data['aws_access_key_id']
            aws_secret_access_key = form.cleaned_data['aws_secret_access_key']
            aws_region = form.cleaned_data['aws_region']

            # Save AWS credentials in session
            request.session['aws_credentials'] = {
                'aws_access_key_id': aws_access_key_id,
                'aws_secret_access_key': aws_secret_access_key,
                'aws_region': aws_region
            }
            request.session.modified = True  # Ensure session is marked as modified

            messages.success(request, "AWS credentials saved successfully.")
            return redirect('show_aws_databases')
    else:
        form = AWSConnectionForm()

    return render(request, 'cloud/aws_pages/aws_connection.html', {'form': form})

def show_aws_databases(request):
    aws_credentials = request.session.get('aws_credentials')
    if not aws_credentials:
        messages.error(request, "Please enter your AWS credentials.")
        return redirect('aws_connection')

    aws_access_key_id = aws_credentials['aws_access_key_id']
    aws_secret_access_key = aws_credentials['aws_secret_access_key']
    aws_region = aws_credentials['aws_region']

    try:
        rds_client = boto3.client('rds', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        documentdb_client = boto3.client('docdb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        dynamodb_client = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        elasticache_client = boto3.client('elasticache', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        memorydb_client = boto3.client('memorydb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        neptune_client = boto3.client('neptune', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        qldb_client = boto3.client('qldb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        timestream_client = boto3.client('timestream-write', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

        rds_databases = get_rds_databases(rds_client)
        documentdb_databases = get_documentdb_databases(documentdb_client)
        dynamodb_tables = get_dynamodb_tables(dynamodb_client)
        elasticache_clusters = get_elasticache_clusters(elasticache_client)
        memorydb_clusters = get_memorydb_clusters(memorydb_client)
        neptune_clusters = get_neptune_clusters(neptune_client)
        qldb_ledgers = get_qldb_ledgers(qldb_client)
        timestream_tables = get_timestream_tables(timestream_client)

        databases = {
            'RDS': rds_databases,
            'DocumentDB': documentdb_databases,
            'DynamoDB': dynamodb_tables,
            'ElastiCache': elasticache_clusters,
            'MemoryDB': memorydb_clusters,
            'Neptune': neptune_clusters,
            'QLDB': qldb_ledgers,
            'Timestream': timestream_tables
        }
    except Exception as e:
        messages.error(request, f"Error retrieving AWS databases: {e}")
        return redirect('aws_connection')

    return render(request, 'cloud/aws_pages/show_aws_databases.html', {'databases': databases})

def get_rds_databases(client):
    response = client.describe_db_instances()
    rds_databases = [db['DBInstanceIdentifier'] for db in response['DBInstances']]
    return rds_databases

def get_documentdb_databases(client):
    response = client.describe_db_clusters()
    documentdb_databases = [db['DBClusterIdentifier'] for db in response['DBClusters']]
    return documentdb_databases

def get_dynamodb_tables(client):
    response = client.list_tables()
    dynamodb_tables = response['TableNames']
    return dynamodb_tables

def get_elasticache_clusters(client):
    response = client.describe_cache_clusters()
    elasticache_clusters = [cluster['CacheClusterId'] for cluster in response['CacheClusters']]
    return elasticache_clusters

def get_memorydb_clusters(client):
    response = client.describe_clusters()
    memorydb_clusters = [cluster['ClusterName'] for cluster in response['Clusters']]
    return memorydb_clusters

def get_neptune_clusters(client):
    response = client.describe_db_clusters()
    neptune_clusters = [cluster['DBClusterIdentifier'] for cluster in response['DBClusters']]
    return neptune_clusters

def get_qldb_ledgers(client):
    response = client.list_ledgers()
    qldb_ledgers = [ledger['Name'] for ledger in response['Ledgers']]
    return qldb_ledgers

def get_timestream_tables(client):
    response = client.list_tables()
    timestream_tables = response['Tables']
    return timestream_tables



