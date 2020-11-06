from .execute_commands_on_linux_instances import execute_commands_on_linux_instances

def add_user(conn_args, instance_ids, user):
    adduser = f'sudo adduser {user.get("login")}'
    user_ssh_dir = f'/home/{user.get("login")}/.ssh'
    create_ssh_directory = f'sudo -u {user.get("login")} mkdir {user_ssh_dir} && sudo -u {user.get("login")} chmod 700 {user_ssh_dir} && sudo -u {user.get("login")} touch {user_ssh_dir}/authorized_keys && sudo -u {user.get("login")} chmod 600 {user_ssh_dir}/authorized_keys'
    set_public_key = f'sudo -u {user.get("login")} echo {user.get("ssh_key")} >> {user_ssh_dir}/authorized_keys'
    ssm_enabled_instances, not_worked_instances, outputs = execute_commands_on_linux_instances(' && '.join(list(filter(lambda x: x, [
        adduser,
        create_ssh_directory,
        set_public_key
    ]))), instance_ids, conn_args)
    print(outputs)
