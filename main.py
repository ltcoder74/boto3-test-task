import boto3
import yaml
from settings import conn_args, key_pair_name
from utils import execute_commands_on_linux_instances, deploy_instance, mount_volume, add_user

# Load configs
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream).get('server')

client = boto3.client('ec2', region_name=config.get('region'))

response = deploy_instance(config, conn_args, client, key_pair_name)
# Exit if some error
if response['ResponseMetadata']['HTTPStatusCode'] != 200:
    sys.exit(response['ResponseMetadata'])

instance_ids = [
    instance['InstanceId'] for instance in response['Instances']
]
client.get_waiter('instance_running').wait(
    InstanceIds=instance_ids
)
print('Instance in running state!')

# Wait for ssm agent to be active
not_worked_instances = [1]
while len(not_worked_instances) > 0:
    ssm_enabled_instances, not_worked_instances, outputs = execute_commands_on_linux_instances('ls', instance_ids, conn_args)

print('Mounting volumes')
for volume in config.get('volumes'):
    mount_volume(conn_args, instance_ids, volume)

print('Adding users')
for user in config.get('users'):
    add_user(conn_args, instance_ids, user)
