from typing import Union


def __get_type_default__(type_: type):
    """
    獲取類型的默認值
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

    def __init__(self, default: Union[str, bool, int, float] = None,
                 optional: bool = False,
                 option: list[Union[str, bool, int, float]] = None,
                 value: Union[str, bool, int, float] = None):
        self.__default = __get_type_default__(type(value)) if default is None else default
        self.__optional = optional
        self.__option = option if option else [True, False] if isinstance(default, bool) else None
        self.__value = value

    def get_default(self):
        return self.__default

    def is_optional(self):
        return self.__optional

    def has_option(self):
        return self.__option is not None

    def get_options(self):
        return self.__option

    def set(self, value):
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

    def __add__(self, other):
        return self.merge(other)

    def __repr__(self):
        return (f"ConfigKey(dfault={self.__default}, is optional={self.__optional}, options={self.__option}, "
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
        if isinstance(value, bool):
            return value
        else:
            raise TypeError(f"Cannot convert {value} to bool")

    def __str__(self):
        value = self.get()
        if isinstance(value, str):
            return value
        else:
            raise TypeError(f"Cannot convert {value} to str")

    def merge(self, other):
        if self.__default is None:
            self.__default = other.get_default()

        self.set(other.get())

        if other.has_option():
            self.__option = other.get_options()

        if other.is_optional():
            self.__optional = True


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
            self.__build_dict(kwargs)

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
                    self.__list_content.append(ConfigKey(i))

    def __build_dict(self, value, default=False):
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
            return iter(self.__content)

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
        for k, v in self:
            if isinstance(v, ConfigTree):
                if v.is_list():
                    ret[k] = v.to_list()
                else:
                    ret[k] = v.to_dict()
            elif isinstance(v, ConfigKey):
                ret[k] = v.get()
            else:
                raise TypeError("???")
        return ret

    def merage(self, other: "ConfigTree") -> "ConfigTree":
        """
        合併兩個配置樹
        @param other: 另一個配置樹
        @return: 合併後的配置樹
        """
        # TODO: 未完成的部分
        if self.is_list() and other.is_list():
            for i in other.values():
                pass
        elif not self.is_list() and not other.is_list():
            pass
        else:
            raise TypeError("Cannot merge list with dict")

    def __add__(self, other):
        # TODO:
        if isinstance(other, ConfigTree):
            if self.is_list() and other.is_list():
                return ConfigTree(is_list=True, build_list=self.values() + other.values())
            elif self.is_list() and not other.is_list():
                return ConfigTree(is_list=True, build_list=self.values() + list(other.values().values()))
            elif not self.is_list() and other.is_list():
                return ConfigTree(is_list=True, build_list=list(self.values().values()) + other.values())
            else:
                return ConfigTree(build_dict={**other.values(), **self.values()})
        elif isinstance(other, ConfigKey):
            if self.is_list():
                self.__list_content.append(other)
                return self
            elif not self.is_list():
                raise TypeError("Cannot add ConfigKey to ConfigTree as a dict")
        else:
            raise TypeError("Cannot add ConfigKey to ConfigTree")


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
        elif isinstance(value, dict):
            self.config[key] = ConfigTree(build_dict=value)
        elif isinstance(value, list):
            self.config[key] = ConfigTree(is_list=True, build_list=value)

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
        # TODO：要在這裏合并所有配置
        if isinstance(value, dict):
            self.config = ConfigTree(build_dict=value, build_with_default=True) + self.config
        elif isinstance(value, list):
            self.config = ConfigTree(is_list=True, build_list=value, build_with_default=True) + self.config

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
        return {key: self.config.get(key).get() for key in self.config}

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
    # TODO: 調試代碼
    import ipdb

    config = ConfigRegistrar()
    config.register("test", "test", "test", optional=True, option=["test", "test2"])
    ipdb.set_trace()
