import macEnvUNIX
import macEnvFile

if __name__ == '__main__':
    ssh_client = macEnvUNIX.SSHClient('ip', 'user', 'password')
    error = ssh_client.connect()

    if error is not None:
        print(error)
    else:
        # 上传文件
        error = ssh_client.upload_file('/local/path/to/file.txt', '/remote/path/to/file.txt')
        if error is not None:
            print(error)

        # 下载文件
        error = ssh_client.download_file('/remote/path/to/file.txt', '/local/path/to/file.txt')
        if error is not None:
            print(error)

        # 执行远程命令
        output = ssh_client.execute_command('ls -l /')
        if output is not None:
            print(output)

        ssh_client.close()

    # 实例化 FolderManager 类
    folder_manager = macEnvFile.FolderManager("test_folder")

    # 检查文件夹是否存在
    if folder_manager.check_folder_existence():
        print("文件夹已经存在")
    else:
        print("文件夹不存在")
        
    # 创建文件夹
    folder_manager.create_folder_or_file()

    # 删除文件夹
    folder_manager.delete_folder_or_file()
    
