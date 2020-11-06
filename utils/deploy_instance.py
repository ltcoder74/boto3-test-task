import boto3

def deploy_instance(config, conn_args, client, key_pair_name):
    userdata = """#cloud-config

    runcmd:
        - cd /tmp
        - sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
    """

    ec2_r = boto3.resource('ec2', **conn_args)

    rolename = "amazonec2ssmrole"
    i_pro_name = "ins_pro_for_ssm"

    # Create an iam instance profile and add required role to this instance profile.
    # Create a role and attach a policy to it if not exist.
    # Instances will have this role to build ssm (ec2 systems manager) connection.
    iam = boto3.resource('iam', **conn_args)

    try:
        response = iam.meta.client.get_instance_profile(InstanceProfileName=i_pro_name)
    except:
        iam.create_instance_profile(InstanceProfileName=i_pro_name)
    try:
        response = iam.meta.client.get_role(RoleName=rolename)
    except:
        iam.create_role(
                    AssumeRolePolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":["ec2.amazonaws.com"]},"Action":["sts:AssumeRole"]}]}',
                    RoleName=rolename)
        role = iam.Role(rolename)
        role.attach_policy(PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM')
        iam.meta.client.add_role_to_instance_profile(InstanceProfileName=i_pro_name, RoleName=rolename)

    iam_ins_profile = {'Name': i_pro_name}

    response = client.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': volume.get('device'),
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': volume.get('size_gb'),
                    'VolumeType': 'gp2'
                },
            } for volume in config.get('volumes')
        ],
        ImageId='ami-00b6a8a2bd28daf19',
        InstanceType=config.get('instance_type'),
        MaxCount=config.get('max_count'),
        MinCount=config.get('min_count'),
        KeyName=key_pair_name,
        IamInstanceProfile=iam_ins_profile
    )
    return response
