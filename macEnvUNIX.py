import paramiko

class SSHClient:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = None
        self.sftp = None

    def connect(self):
        try:
            # 创建SSH客户端对象
            self.client = paramiko.SSHClient()

            # 允许连接不在本地known_hosts文件中的主机
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 连接SSH服务器
            self.client.connect(self.hostname, username=self.username, password=self.password)

            # 创建SFTP客户端对象
            self.sftp = self.client.open_sftp()

        except paramiko.AuthenticationException as e:
            error_msg = f"Authentication failed: {e}"
            return error_msg
        except paramiko.SSHException as e:
            error_msg = f"Unable to establish SSH connection: {e}"
            return error_msg
        except Exception as e:
            error_msg = f"Error occurred while connecting to remote host: {e}"
            return error_msg

    def execute_command(self, command):
        try:
            # 在SSH会话中执行命令
            stdin, stdout, stderr = self.client.exec_command(command)

            # 输出命令执行结果
            output = stdout.read().decode()

            return output

        except paramiko.SSHException as e:
            error_msg = f"Error occurred while executing remote command: {e}"
            return error_msg

    def upload_file(self, local_path, remote_path):
        try:
            # 使用SFTP协议上传文件
            self.sftp.put(local_path, remote_path)

        except IOError as e:
            error_msg = f"Error occurred while uploading file: {e}"
            return error_msg

    def download_file(self, remote_path, local_path):
        try:
            # 使用SFTP协议下载文件
            self.sftp.get(remote_path, local_path)

        except IOError as e:
            error_msg = f"Error occurred while downloading file: {e}"
            return error_msg

    # 下载文件夹
    def download_folder(self, remote_dir, local_dir):
        for filename in self.sftp.listdir(remote_dir):
            remote_path = os.path.join(remote_dir, filename)
            local_path = os.path.join(local_dir, filename)
            if '.' not in filename:
                os.makedirs(local_path, exist_ok=True)
                download_folder(remote_path, local_path)
            else:
                self.sftp.get(remote_path, local_path)

    # 上传文件夹
    def upload_folder(self, local_dir, remote_dir):
        for filename in os.listdir(local_dir):
            local_path = os.path.join(local_dir, filename)
            remote_path = os.path.join(remote_dir, filename)
            if os.path.isfile(local_path):
                self.sftp.put(local_path, remote_path)
            elif os.path.isdir(local_path):
                try:
                    self.sftp.stat(remote_path)
                except IOError:
                    self.sftp.mkdir(remote_path)
                upload_folder(local_path, remote_path)

    def close(self):
        if self.sftp is not None:
            self.sftp.close()
            self.sftp = None

        if self.client is not None:
            self.client.close()
            self.client = None

