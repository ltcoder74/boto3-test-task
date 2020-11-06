import boto3
import os
from settings import key_pair_name

ec2 = boto3.resource('ec2')

# create a file to store the key locally
outfile = open(
    os.path.join(
        'keys',
        f'{key_pair_name}.pem'
    ),
    'w'
)

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName=key_pair_name)

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)
