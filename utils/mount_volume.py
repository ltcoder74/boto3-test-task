from .execute_commands_on_linux_instances import execute_commands_on_linux_instances

def mount_volume(conn_args, instance_ids, volume):
    create_file_system = f'sudo mkfs -t {volume.get("type")} {volume.get("device")}'
    create_mount_directory = '' if volume.get('mount') == '/' else f'sudo mkdir {volume.get("mount")}'
    mount_volume = f'sudo mount {volume.get("device")} {volume.get("mount")}'
    ssm_enabled_instances, not_worked_instances, outputs = execute_commands_on_linux_instances(' && '.join(list(filter(lambda x: x, [
        create_file_system,
        create_mount_directory,
        mount_volume
    ]))), instance_ids, conn_args)
    print(outputs)