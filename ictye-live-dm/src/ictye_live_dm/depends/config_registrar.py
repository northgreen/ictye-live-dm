from typing import Union


def __get_type_default__(type_: type):
    """
    獲取類型的默認值，支持str，boo，int，float，其他的樹形結構請使用ConfigTree
    :param type_: 類型
    :return: 默認值
    """
    if type_ == str:
        return ""
    elif type_ == bool:
        return False
    elif type_ == int:
        return 0
    elif type_ == float:
        return 0.0
    else:
        raise ValueError(f"Unsupported type: {type_},may be you can use ConfigTree to build a tree")


class ConfigKey:
    """
    A config key that can be registered to the ConfigRegistrar.
    """

    def __init__(self, default: str | bool | int | float = None,
                 optional: bool = False,
                 option: list[str | bool | int | float] = None,
                 value: str | bool | int | float = None):
        if value is None and default is None:
            raise ValueError("None ConfigKey is invalid")
        # self.__value = default if value is None else value
        self.__default = __get_type_default__(type(value)) if default is None else default
        self.__optional = optional
        self.__option = option if option else [True, False] if isinstance(default, bool) else None
        self.__value = value

    def get_default(self):
        """
        獲取默認值
        @return: 默認值
        """
        return self.__default

    def is_optional(self):
        """
        檢查是否為可選的
        @return:
        """
        return self.__optional

    def has_option(self):
        """
        檢查是否具有選項
        @return:
        """
        return self.__option is not None

    def get_options(self):
        """
        獲取選項
        @return: 選項
        """
        return self.__option

    def set(self, value):
        """
        設置ConfigKey的值，注意的是，此方法會對類型進行强制轉換
        @param value: 目的值
        @return:
        """
        if self.__option is not None and value not in self.__option:
            raise ValueError(f"Invalid value for unexpected option: {value}")
        if value is None:
            return
        if self.__value is None:
            if self.__default is None:
                self.__value = type(value)
                self.__default = __get_type_default__(type(self.__value))
            self.__value = type(self.__default)(value)
            return
        self.__value = type(self.__value)(value)

    def get_type(self):
        return type(self.__value)

    def is_set(self):
        return self.__value is not None

    def get(self):
        # 检查是否存在存储的值，如果存在则返回该值，否则返回默认值
        return self.__value if self.__value is not None else self.__default

    def __repr__(self):
        return (f"ConfigKey(dfault={self.__default}, "
                f"is optional={self.__optional}, "
                f"options={self.__option}, "
                f"value={self.__value})")

    def __int__(self):
        value = self.get()
        if isinstance(value, int):
            return value
        else:
            raise TypeError(f"Cannot convert {value} to int")

    def __float__(self):
        value = self.get()
        if isinstance(value, float):
            return value
        else:
            raise TypeError(f"Cannot convert {value} to float")

    def __bool__(self):
        value = self.get()
        return bool(value)

    def __str__(self):
        value = self.get()
        if isinstance(value, str):
            return value
        else:
            return self.__repr__()

    def merge(self, other):
        """
        合併兩個ConfigKey
        1. 如果自身沒有默認值，則會采用other的
        2. 會采取other的数据。
        3. 會采取other的option
        @param other: 另一個ConfigKey
        @return: 合併後的ConfigKey
        """
        if self.__default is __get_type_default__(type(other.get())):
            self.__default = other.get_default()

        self.set(other.get())

        if other.has_option():
            self.__option = other.get_options()

        if other.is_optional():
            self.__optional = True

    def __eq__(self, other: Union["ConfigKey", type]):
        if isinstance(other, ConfigKey):
            return self.get() == other.get()
        else:
            return self.get() == other


class ConfigTree:
    """
    配置數，用於表示樹形結構配置，可以用於配置文件或數據庫查詢等。
    """

    def __init__(self,
                 value: ConfigKey = None,  # 根值
                 is_list: bool = False,  # 是否為列表結構
                 build_dict: dict = None,  # 字典結構的子節點
                 build_list: list = None,  # 列表結構的子節點
                 build_with_default: bool = False,  # 是否使用默認值構造子節點
                 allow: list = None,
                 tree_lock=False,
                 *args: any,
                 **kwargs: any):
        """
        構造函數
        :param value: 樹的根值
        :param is_list: 是否為列表結構
        :param args: 列表結構的子節點
        :param kwargs: 字典結構的子節點
        """

        self.__allow = allow
        self.__tree_lock = tree_lock
        self.__value: ConfigKey = value
        self.__content: dict[str, Union[ConfigKey, ConfigTree]] = {}
        self.__is_list: bool = is_list
        self.__list_content: list[Union[ConfigKey, ConfigTree]] = []

        if is_list:
            self.__build_list(args, default=build_with_default)
        else:
            self.__build_dict(kwargs, default=build_with_default)

        if build_dict is not None or build_list is not None:
            if self.__is_list:
                self.__build_list([*args, *build_list], default=build_with_default)
            else:
                self.__build_dict({**build_dict, **kwargs}, default=build_with_default)

    def __build_list(self, value, default=False):
        if not self.__is_list:
            raise TypeError("This is not a list")
        for i in value:

            if default:
                if isinstance(i, ConfigKey):
                    self.__list_content.append(i)
                elif isinstance(i, dict):
                    self.__list_content.append(ConfigTree(build_dict=i, build_with_default=True))
                elif isinstance(i, list):
                    self.__list_content.append(ConfigTree(is_list=True, build_list=i, build_with_default=True))
                elif isinstance(i, ConfigTree):
                    self.__list_content.append(i)
                else:
                    self.__list_content.append(ConfigKey(default=i))
            else:
                if isinstance(i, ConfigKey):
                    self.__list_content.append(i)
                elif isinstance(i, dict):
                    self.__list_content.append(ConfigTree(build_dict=i))
                elif isinstance(i, list):
                    self.__list_content.append(ConfigTree(is_list=True, build_list=i))
                elif isinstance(i, ConfigTree):
                    self.__list_content.append(i)
                else:
                    self.__list_content.append(ConfigKey(value=i))

    def __build_dict(self, value, default=False):
        """
        内部構造鍵值對樹的函數
        @param value: 傳入參數
        @param default: 是否默認
        @return:
        """
        if self.__is_list:
            raise TypeError("This is not a dict")
        for key, value in value.items():
            if default:
                if isinstance(value, ConfigKey):
                    self.__content[key] = value
                elif isinstance(value, dict):
                    self.__content[key] = ConfigTree(build_dict=value, build_with_default=True)
                elif isinstance(value, list):
                    self.__content[key] = ConfigTree()
                elif isinstance(value, ConfigTree):
                    self.__content[key] = value
                else:
                    self.__content[key] = ConfigKey(default=value)
            else:
                if isinstance(value, ConfigKey):
                    self.__content[key] = value
                elif isinstance(value, dict):
                    self.__content[key] = ConfigTree(build_dict=value)
                elif isinstance(value, list):
                    self.__content[key] = ConfigTree(is_list=True, build_list=value)
                elif isinstance(value, ConfigTree):
                    self.__content[key] = value
                else:
                    self.__content[key] = ConfigKey(value)

    def get(self, key: str) -> Union[ConfigKey]:
        # 检查存储内容是否为列表
        if self.__is_list:
            # 将键转换为整数并返回对应索引处的值
            return self.__list_content[int(key)]
        else:
            # 对于字典存储，直接使用键来获取值
            return self.__content[key]

    @staticmethod
    def has_option() -> bool:
        return False

    def __getitem__(self, item) -> Union[ConfigKey]:
        return self.get(item)

    def get_value(self) -> ConfigKey:
        return self.__value

    def read_value(self) -> Union[str, int, float, bool]:
        return self.__value.get()

    def __setitem__(self, key: Union[str, int],
                    value: Union[ConfigKey, "ConfigTree"]):
        self.set(key, value)

    def set(self, key: Union[str, int],
            value: Union[ConfigKey, "ConfigTree"]):
        """
        設置值
        @param key: 鍵名
        @param value: 值
        @return: None
        """
        if self.__is_list:
            self.__list_content[int(key)] = value
        else:
            self.__content[key] = value

    def __iter__(self):
        if self.__is_list:
            return iter(self.__list_content)
        else:
            return iter(self.__content.items())

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return (f"ConfigTree(value= {self.__value}, is_list= {self.__is_list},"
                f"content= {self.__content if not self.__is_list else self.__list_content})")

    def __len__(self):
        if self.__is_list:
            return len(self.__list_content)
        else:
            return len(self.__content)

    def items(self) -> list:
        if self.__is_list:
            return self.__list_content
        else:
            return list(self.__content.items())

    def keys(self) -> list:
        if self.__is_list:
            return self.__list_content
        else:
            return list(self.__content.keys())

    def values(self) -> Union[list, dict]:
        if self.__is_list:
            return self.__list_content
        else:
            return self.__content

    def is_dict(self) -> bool:
        return not self.__is_list

    def is_list(self) -> bool:
        return self.__is_list

    def to_list(self) -> list:
        """
        將樹轉換爲列表和其他python標準内容
        @return: 列表
        """
        ret = []
        if not self.is_list():
            raise TypeError("Cannot convert dict to list")
        for i in self:
            if isinstance(i, ConfigTree):
                if i.is_list():
                    ret.append(i.to_list())
                else:
                    ret.append(i.to_dict())
            elif isinstance(i, ConfigKey):
                ret.append(i.get())
            else:
                raise TypeError("???")
        return ret

    def to_dict(self) -> dict:
        """
        將樹的額所有内容都轉換爲字典和python標準内容
        @return: 字典
        """
        ret = {}
        if self.is_list():
            raise TypeError("Cannot convert list to dict")
        for k, v in self.items():
            if isinstance(v, ConfigTree):
                if v.is_list():
                    ret[k] = v.to_list()
                else:
                    ret[k] = v.to_dict()
            elif isinstance(v, ConfigKey):
                ret[k] = v.get()
            else:
                raise TypeError("??? How can you did it???")
        return ret

    def merge(self, other: "ConfigTree") -> "ConfigTree":
        """
        合併兩個配置樹
        @param other: 另一個配置樹
        @return: 合併後的配置樹
        """
        if self.is_list() and other.is_list():  # 兩個都是列表
            for i in other.values():
                self.__list_content.append(i)  # TODO：此處邏輯仍然有問題
        elif not self.is_list() and not other.is_list():  # 兩個都是字典
            for k, v in other.items():
                if k in self.__content:
                    self.__content[k].merge(v)
                else:
                    self.set(k, v)
        else:
            raise TypeError("Cannot merge list with dict")
        return self

    def __contains__(self, item):
        if self.is_list():
            for i in self.__list_content:
                if i == item:
                    return True
        else:
            for k, v in self.__content.items():
                if k == item:
                    return True
        return False


class ConfigRegistrar:
    """
    A config registrar that can be used to register config keys.
    """

    def __init__(self):
        self.config = ConfigTree()

    def register(self, key, value=None, default=None, optional: bool = False, option: list = None):
        """
        Register a config key.
        @param key: key name
        @param value: config __value
        @param default: config __default __value, if not provided, will use the __value type's __default __value
        @param optional: is this config key __optional
        @param option: list of valid options for this config key
        """
        if key in self.config:
            raise ValueError(f"Config key '{key}' already registered")

        if isinstance(value, ConfigTree) or isinstance(value, ConfigKey):
            self.config[key] = value
            return
        elif isinstance(value, dict):
            self.config[key] = ConfigTree(build_dict=value)
            return
        elif isinstance(value, list):
            self.config[key] = ConfigTree(is_list=True, build_list=value)
            return

        if isinstance(default, dict):
            self.config[key] = ConfigTree(build_dict=default, build_with_default=True)
            return
        elif isinstance(default, list):
            self.config[key] = ConfigTree(is_list=True, build_list=default, build_with_default=True)
            return

        self.config[key] = ConfigKey(default, optional, value=value, option=option)

    def set(self, key, value):
        """
        Set the __value of a config key.
        @param key: key name
        @param value: config __value
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        self.config.get(key).set(value)

    def dump(self, value):
        if isinstance(value, dict):
            self.config = ConfigTree(build_dict=value)
        elif isinstance(value, list):
            self.config = ConfigTree(is_list=True, build_list=value)

    def dump_default(self, value):
        """
        將傳入的作爲默認配置并且合并
        @param value:
        @return:
        """
        if isinstance(value, dict):
            self.config = self.config.merge(ConfigTree(build_dict=value))
        elif isinstance(value, list):
            self.config = self.config.merge(ConfigTree(is_list=True, build_list=value))

    def get(self, key):
        """
        Get the __value of a config key.
        @param key: key name
        @return: config __value
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        value = self.config.get(key)
        if isinstance(value, ConfigKey):
            return value.get()
        elif isinstance(value, ConfigTree):
            return value
        else:
            print("value:", value)
            return value

    def is_optional(self, key):
        """
        Check if a config key is __optional.
        @param key: key name
        @return: True if __optional, False otherwise
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config.get(key).is_optional()

    def get_option(self, key):
        """
        Get the valid options for a config key.
        @param key: key name
        @return: list of valid options
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config.get(key).get_options()

    def is_option(self, key):
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config.get(key).has_option()

    def isset(self, key):
        """
        Check if a config key is set.
        @param key: key name
        @return: True if set, False otherwise
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config.get(key).is_set()

    def items(self):
        return self.config.items()

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()

    def to_dict(self):
        """
        Convert the config registrar to a dictionary.
        @return: dictionary representation of the config registrar
        """
        return self.config.to_dict()

    def get_config_tree(self):
        return self.config

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.config

    def __iter__(self):
        return iter(self.config)

    def __repr__(self):
        return f"ConfigRegistrar({self.config})"

    def __len__(self):
        return len(self.config)


if __name__ == "__main__":
    config = ConfigTree(build_dict={'key1': ConfigKey('value1'), 'key2': ConfigKey('value2')})
    result_dict = config.to_dict()
