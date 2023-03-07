import os

class FolderManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def check_folder_existence(self):
        if os.path.exists(self.folder_path):
            return 1
        else:
            return 0
    
    def create_folder_or_file(self, is_folder=True):
        try:
            if is_folder:
                os.mkdir(self.folder_path)
            else:
                open(self.folder_path, 'a').close()
            return 1
        except Exception as e:
            return 0
    
    def delete_folder_or_file(self, is_folder=True):
        try:
            if is_folder:
                os.rmdir(self.folder_path)
            else:
                os.remove(self.folder_path)
            return 1
        except Exception as e:
            return 0
