#AWS/forms.py
from django import forms

DATABASE_CHOICES = [
    ('rds', 'RDS'),
    ('documentdb', 'DocumentDB'),
    ('dynamodb', 'DynamoDB'),
    ('elasticache', 'ElastiCache'),
]

ENGINE_CHOICES = [
    ('postgres', 'PostgreSQL'),
    ('mysql', 'MySQL'),
    ('mariadb', 'MariaDB'),
    ('oracle', 'Oracle'),
    ('sqlserver', 'SQL Server'),
]

class DBTypeForm(forms.Form):
    db_type = forms.ChoiceField(label='Select Database Type', choices=DATABASE_CHOICES)

class RDSInstanceForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    db_instance_identifier = forms.CharField(label='DB Instance Identifier', max_length=100)
    db_instance_class = forms.CharField(label='DB Instance Class', max_length=100)
    engine = forms.ChoiceField(label='Engine', choices=ENGINE_CHOICES)
    engine_version = forms.ChoiceField(label='Engine Version', choices=[])  # سيتم ملؤها ديناميكياً عبر JavaScript
    allocated_storage = forms.IntegerField(label='Allocated Storage')
    master_username = forms.CharField(label='Master Username', max_length=100)
    master_user_password = forms.CharField(label='Master User Password', max_length=100)
    backup_retention_period = forms.IntegerField(label='Backup Retention Period')
    db_name = forms.CharField(label='Database Name', max_length=100)
    publicly_accessible = forms.BooleanField(label='Publicly Accessible', required=False)


class DocumentDBForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    db_cluster_identifier = forms.CharField(label='DB Cluster Identifier', max_length=100)
    db_instance_class = forms.CharField(label='DB Instance Class', max_length=100)
    engine_version = forms.CharField(label='Engine Version', max_length=100)
    master_username = forms.CharField(label='Master Username', max_length=100)
    master_user_password = forms.CharField(label='Master User Password', max_length=100)
    backup_retention_period = forms.IntegerField(label='Backup Retention Period')
    db_name = forms.CharField(label='Database Name', max_length=100)
    publicly_accessible = forms.BooleanField(label='Publicly Accessible', required=False)


class DynamoDBForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    table_name = forms.CharField(label='Table Name', max_length=100)
    partition_key = forms.CharField(label='Partition Key', max_length=100)
    sort_key = forms.CharField(label='Sort Key', max_length=100, required=False)
    read_capacity_units = forms.IntegerField(label='Read Capacity Units')
    write_capacity_units = forms.IntegerField(label='Write Capacity Units')


class ElastiCacheForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    cache_cluster_id = forms.CharField(label='Cache Cluster ID', max_length=100)
    cache_node_type = forms.CharField(label='Cache Node Type', max_length=100)
    engine = forms.ChoiceField(label='Engine', choices=ENGINE_CHOICES)
    engine_version = forms.ChoiceField(label='Engine Version', choices=[])
    num_cache_nodes = forms.IntegerField(label='Number of Cache Nodes')
    parameter_group_name = forms.CharField(label='Parameter Group Name', max_length=100)
    maintenance_window = forms.CharField(label='Maintenance Window', max_length=100)


class AmazonKeyspacesForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    keyspace_name = forms.CharField(label='Keyspace Name', max_length=100)
    table_name = forms.CharField(label='Table Name', max_length=100)
    billing_mode = forms.ChoiceField(label='Billing Mode', choices=[('PROVISIONED', 'Provisioned'), ('PAY_PER_REQUEST', 'Pay per request')])


class MemoryDBForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    cluster_name = forms.CharField(label='Cluster Name', max_length=100)
    node_type = forms.CharField(label='Node Type', max_length=100)
    num_replicas_per_shard = forms.IntegerField(label='Number of Replicas per Shard')
    shard_count = forms.IntegerField(label='Shard Count')
    engine_version = forms.CharField(label='Engine Version', max_length=100)


class NeptuneForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    db_cluster_identifier = forms.CharField(label='DB Cluster Identifier', max_length=100)
    db_instance_class = forms.CharField(label='DB Instance Class', max_length=100)
    engine_version = forms.ChoiceField(label='Engine Version', choices=[])
    db_name = forms.CharField(label='Database Name', max_length=100)


class QLDBForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    ledger_name = forms.CharField(label='Ledger Name', max_length=100)
    permissions_mode = forms.ChoiceField(label='Permissions Mode', choices=[('ALLOW_ALL', 'Allow All'), ('STANDARD', 'Standard')])
    deletion_protection = forms.BooleanField(label='Deletion Protection', required=False)


class TimestreamForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
    database_name = forms.CharField(label='Database Name', max_length=100)
    table_name = forms.CharField(label='Table Name', max_length=100)
    retention_period_hours = forms.IntegerField(label='Retention Period (Hours)')
    memory_store_retention_period_hours = forms.IntegerField(label='Memory Store Retention Period (Hours)')
    magnetic_store_retention_period_days = forms.IntegerField(label='Magnetic Store Retention Period (Days)')


#AWS/forms.py
class DatabaseConnectionForm(forms.Form):
    endpoint = forms.CharField(label='Endpoint', max_length=100)
    user = forms.CharField(label='User', max_length=100)
    port = forms.IntegerField(label='Port')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    dbname = forms.CharField(label='Database Name', max_length=100)

#AWS/forms.py
class AWSConnectionForm(forms.Form):
    aws_access_key_id = forms.CharField(label='AWS Access Key ID', max_length=100)
    aws_secret_access_key = forms.CharField(label='AWS Secret Access Key', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=100)
