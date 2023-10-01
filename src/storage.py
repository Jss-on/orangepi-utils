import os

class USBStorage:
    def __init__(self):
        self.mount_path = "/media/orangepi_usb"
        if not os.path.isdir(self.mount_path):
            try:
                os.mkdir(self.mount_path)
                print(f"Directory {self.mount_path} created.")
            except PermissionError:
                print(f"You don't have permission to create {self.mount_path}. Try running the script as sudo.")
        self.is_connected()

    def is_connected(self):
        return self.mount_path is not None and os.path.ismount(self.mount_path)

    def read(self, file_path):
        if self.is_connected():
            full_path = os.path.join(self.mount_path, file_path)
            with open(full_path, 'r') as f:
                return f.read()
        else:
            return "USB not connected"

    def write(self, file_path, content):
        if self.is_connected():
            full_path = os.path.join(self.mount_path, file_path)
            with open(full_path, 'w') as f:
                f.write(content)
        else:
            return "USB not connected"

    def remove(self, file_path):
        if self.is_connected():
            full_path = os.path.join(self.mount_path, file_path)
            os.remove(full_path)
        else:
            return "USB not connected"

    def mkdir(self, dir_path):
        if self.is_connected():
            full_path = os.path.join(self.mount_path, dir_path)
            os.makedirs(full_path)
        else:
            return "USB not connected"

    def ls(self, dir_path):
        if self.is_connected():
            full_path = os.path.join(self.mount_path, dir_path)
            return os.listdir(full_path)
        else:
            return "USB not connected"

    def rmdir(self, dir_path):
        if self.is_connected():
            full_path = os.path.join(self.mount_path, dir_path)
            os.rmdir(full_path)
        else:
            return "USB not connected"

    def available_space(self):
        if self.is_connected():
            statvfs = os.statvfs(self.mount_path)
            return statvfs.f_frsize * statvfs.f_bfree
        else:
            return "USB not connected"

    def total_space(self):
        if self.is_connected():
            statvfs = os.statvfs(self.mount_path)
            return statvfs.f_frsize * statvfs.f_blocks
        else:
            return "USB not connected"
