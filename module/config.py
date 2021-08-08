import configparser


class ReadConfig:
    """定义一个读取配置文件的类"""
    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))
            configpath = os.path.join(root_dir, "config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def get_val(self, section, item):
        value = self.cf.get(section, item)
        return value

if __name__ == '__main__':
    cf = ReadConfig('../config.ini')
    print(cf.get_val('sqlite_db','database_dir'))
