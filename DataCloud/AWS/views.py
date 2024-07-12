# AWS/views.py
from django.shortcuts import render, redirect
import boto3
from .forms import RDSInstanceForm 

from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.urls import reverse

from .forms import (
    DocumentDBForm, DynamoDBForm, ElastiCacheForm, AmazonKeyspacesForm,
    MemoryDBForm, NeptuneForm, QLDBForm, TimestreamForm, RDSInstanceForm,

)

def choose_database_service(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        return redirect('create_aws_instance', service_name=service_name)
    return render(request, 'cloud/AWS.html')

def create_aws_instance(request, service_name):
    form_class = get_form_class(service_name)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            aws_access_key_id = form.cleaned_data['aws_access_key_id']
            aws_secret_access_key = form.cleaned_data['aws_secret_access_key']
            aws_region = form.cleaned_data['aws_region']
            db_name = form.cleaned_data.get('db_name', None)
            db_instance_identifier = form.cleaned_data.get('db_instance_identifier', None)
            db_cluster_identifier = form.cleaned_data.get('db_cluster_identifier', None)
            table_name = form.cleaned_data.get('table_name', None)
            partition_key = form.cleaned_data.get('partition_key', None)
            sort_key = form.cleaned_data.get('sort_key', None)
            read_capacity_units = form.cleaned_data.get('read_capacity_units', None)
            write_capacity_units = form.cleaned_data.get('write_capacity_units', None)
            cache_cluster_id = form.cleaned_data.get('cache_cluster_id', None)
            cache_node_type = form.cleaned_data.get('cache_node_type', None)
            num_cache_nodes = form.cleaned_data.get('num_cache_nodes', None)
            parameter_group_name = form.cleaned_data.get('parameter_group_name', None)
            maintenance_window = form.cleaned_data.get('maintenance_window', None)
            keyspace_name = form.cleaned_data.get('keyspace_name', None)
            billing_mode = form.cleaned_data.get('billing_mode', None)
            cluster_name = form.cleaned_data.get('cluster_name', None)
            node_type = form.cleaned_data.get('node_type', None)
            num_replicas_per_shard = form.cleaned_data.get('num_replicas_per_shard', None)
            shard_count = form.cleaned_data.get('shard_count', None)
            ledger_name = form.cleaned_data.get('ledger_name', None)
            permissions_mode = form.cleaned_data.get('permissions_mode', None)
            deletion_protection = form.cleaned_data.get('deletion_protection', None)
            database_name = form.cleaned_data.get('database_name', None)
            retention_period_hours = form.cleaned_data.get('retention_period_hours', None)
            memory_store_retention_period_hours = form.cleaned_data.get('memory_store_retention_period_hours', None)
            magnetic_store_retention_period_days = form.cleaned_data.get('magnetic_store_retention_period_days', None)

            try:
                client = boto3.client(
                    service_name.lower(),
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=aws_region
                )

                if service_name == 'RDS':
                    response = client.create_db_instance(
                        DBInstanceIdentifier=db_instance_identifier,
                        AllocatedStorage=form.cleaned_data['allocated_storage'],
                        DBInstanceClass=form.cleaned_data['db_instance_class'],
                        Engine=form.cleaned_data['engine'],
                        MasterUsername=form.cleaned_data['master_username'],
                        MasterUserPassword=form.cleaned_data['master_user_password'],
                        BackupRetentionPeriod=form.cleaned_data['backup_retention_period'],
                        EngineVersion=form.cleaned_data['engine_version'],
                        PubliclyAccessible=form.cleaned_data['publicly_accessible'],
                        DBName=db_name
                    )

                    # انتظر حتى تصبح قاعدة البيانات متاحة
                    waiter = client.get_waiter('db_instance_available')
                    waiter.wait(DBInstanceIdentifier=db_instance_identifier)

                    # استرداد معلومات قاعدة البيانات بعد إنشائها
                    db_info = client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
                    instance_info = db_info['DBInstances'][0]

                elif service_name == 'DocumentDB':
                    response = client.create_db_cluster(
                        DBClusterIdentifier=db_cluster_identifier,
                        Engine='docdb',
                        MasterUsername=form.cleaned_data['master_username'],
                        MasterUserPassword=form.cleaned_data['master_user_password'],
                        BackupRetentionPeriod=form.cleaned_data['backup_retention_period'],
                        EngineVersion=form.cleaned_data['engine_version'],
                        Port=27017,
                        StorageEncrypted=True,
                        DeletionProtection=True,
                        Tags=[
                            {
                                'Key': 'Name',
                                'Value': 'MyDocumentDBCluster'
                            },
                        ]
                    )

                    # انتظار حتى يصبح الكتلة متاحة
                    waiter = client.get_waiter('db_cluster_available')
                    waiter.wait(DBClusterIdentifier=db_cluster_identifier)

                    # استرداد معلومات الكتلة بعد إنشائها
                    cluster_info = client.describe_db_clusters(DBClusterIdentifier=db_cluster_identifier)
                    instance_info = cluster_info['DBClusters'][0]

                elif service_name == 'DynamoDB':
                    response = client.create_table(
                        TableName=table_name,
                        KeySchema=[
                            {
                                'AttributeName': partition_key,
                                'KeyType': 'HASH'
                            },
                            {
                                'AttributeName': sort_key,
                                'KeyType': 'RANGE'
                            } if sort_key else {}
                        ],
                        AttributeDefinitions=[
                            {
                                'AttributeName': partition_key,
                                'AttributeType': 'S'
                            },
                            {
                                'AttributeName': sort_key,
                                'AttributeType': 'S'
                            } if sort_key else {}
                        ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': read_capacity_units,
                            'WriteCapacityUnits': write_capacity_units
                        }
                    )
                    
                    # استرداد معلومات الجدول بعد إنشائه
                    table_info = client.describe_table(TableName=table_name)
                    instance_info = table_info['Table']

                elif service_name == 'ElastiCache':
                    response = client.create_cache_cluster(
                        CacheClusterId=cache_cluster_id,
                        CacheNodeType=cache_node_type,
                        Engine=form.cleaned_data['engine'],
                        EngineVersion=form.cleaned_data['engine_version'],
                        NumCacheNodes=num_cache_nodes,
                        CacheParameterGroupName=parameter_group_name,
                        CacheSubnetGroupName='default',
                        AutoMinorVersionUpgrade=True,
                        PreferredMaintenanceWindow=maintenance_window
                    )

                    # انتظار حتى يصبح الكتلة متاحة
                    waiter = client.get_waiter('cache_cluster_available')
                    waiter.wait(CacheClusterId=cache_cluster_id)

                    # استرداد معلومات الكتلة بعد إنشائها
                    cluster_info = client.describe_cache_clusters(CacheClusterId=cache_cluster_id)
                    instance_info = cluster_info['CacheClusters'][0]

                elif service_name == 'AmazonKeyspaces':
                    response = client.create_table(
                        Keyspace=keyspace_name,
                        Table=table_name,
                        BillingMode=billing_mode
                    )

                    # لا يمكن استرداد معلومات الجدول مباشرة، لذلك نقوم بإعادة البيانات المرسلة
                    instance_info = {
                        'Keyspace': keyspace_name,
                        'TableName': table_name,
                        'BillingMode': billing_mode
                    }

                elif service_name == 'MemoryDB':
                    response = client.create_cluster(
                        ClusterName=cluster_name,
                        NodeType=node_type,
                        NumReplicasPerShard=num_replicas_per_shard,
                        ShardCount=shard_count,
                        EngineVersion=form.cleaned_data['engine_version']
                    )

                    # انتظار حتى يصبح الكتلة متاحة
                    waiter = client.get_waiter('cluster_available')
                    waiter.wait(ClusterName=cluster_name)

                    # استرداد معلومات الكتلة بعد إنشائها
                    cluster_info = client.describe_clusters(ClusterName=cluster_name)
                    instance_info = cluster_info['Clusters'][0]

                elif service_name == 'Neptune':
                    response = client.create_db_cluster(
                        DBClusterIdentifier=db_cluster_identifier,
                        Engine='neptune',
                        EngineVersion=form.cleaned_data['engine_version'],
                        Tags=[
                            {
                                'Key': 'Name',
                                'Value': 'MyNeptuneCluster'
                            },
                        ]
                    )

                    # انتظار حتى يصبح الكتلة متاحة
                    waiter = client.get_waiter('db_cluster_available')
                    waiter.wait(DBClusterIdentifier=db_cluster_identifier)

                    # استرداد معلومات الكتلة بعد إنشائها
                    cluster_info = client.describe_db_clusters(DBClusterIdentifier=db_cluster_identifier)
                    instance_info = cluster_info['DBClusters'][0]

                elif service_name == 'QLDB':
                    response = client.create_ledger(
                        Name=ledger_name,
                        PermissionsMode=permissions_mode,
                        DeletionProtection=deletion_protection
                    )

                    # انتظار حتى يصبح الدفتر متاح
                    waiter = client.get_waiter('ledger_active')
                    waiter.wait(Name=ledger_name)

                    # استرداد معلومات الدفتر بعد إنشائه
                    ledger_info = client.describe_ledger(Name=ledger_name)
                    instance_info = ledger_info

                elif service_name == 'Timestream':
                    response = client.create_database(
                        DatabaseName=database_name
                    )
                    response = client.create_table(
                        DatabaseName=database_name,
                        TableName=table_name,
                        RetentionProperties={
                            'MemoryStoreRetentionPeriodInHours': memory_store_retention_period_hours,
                            'MagneticStoreRetentionPeriodInDays': magnetic_store_retention_period_days
                        }
                    )

                    # استرداد معلومات الجدول بعد إنشائه
                    table_info = client.describe_table(DatabaseName=database_name, TableName=table_name)
                    instance_info = table_info['Table']

                return render(request, 'cloud/success.html', {'instance_info': instance_info})

            except NoCredentialsError:
                form.add_error(None, "Invalid AWS credentials")
            except PartialCredentialsError:
                form.add_error(None, "Incomplete AWS credentials")
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = form_class()

    return render(request, 'cloud/aws_pages/create_aws_instance.html', {'form': form, 'service_name': service_name})

def get_form_class(service_name):
    forms = {
        'RDS': RDSInstanceForm,
        'DocumentDB': DocumentDBForm,
        'DynamoDB': DynamoDBForm,
        'ElastiCache': ElastiCacheForm,
        'AmazonKeyspaces': AmazonKeyspacesForm,
        'MemoryDB': MemoryDBForm,
        'Neptune': NeptuneForm,
        'QLDB': QLDBForm,
        'Timestream': TimestreamForm,
    }
    return forms.get(service_name)



def success(request):
    return render(request, 'cloud/success.html')



#والجزء الذي يعمل بنجاح في تسجيل الجلسات

