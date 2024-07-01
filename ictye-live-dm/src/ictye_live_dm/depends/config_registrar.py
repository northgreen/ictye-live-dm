from typing import TypeVar, Generic, Union

T = TypeVar('T')


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


class ConfigKey(Generic[T]):
    """
    A config key that can be registered to the ConfigRegistrar.
    """

    def __init__(self, default: T = None, optional: bool = False, option: list[T] = None, value: T = None):
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
            raise ValueError(f"Invalid __value for __option: {value}")
        self.__value = value

    def is_set(self):
        return self.__value is not None

    def get(self):
        # 检查是否存在存储的值，如果存在则返回该值，否则返回默认值
        return self.__value if self.__value is not None else self.__default

    def __add__(self, other):
        # 如果other是選項則檢查選項是否一致
        if other.has_option() and self.has_option():
            if other.get_options() != other.get_options():
                raise ValueError(f"Invalid __option for __option: {other.get_options()}")
        # 如果other有default則并入
        if other.get_default() is not None:
            self.__default = other.get_default()

    def __repr__(self):
        return (f"ConfigKey(dfault={self.__default}, is optional={self.__optional}, options={self.__option}, "
                f"value={self.__value})")


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
                 *args: ConfigKey,
                 **kwargs: ConfigKey):
        """
        構造函數
        :param value: 樹的根值
        :param is_list: 是否為列表結構
        :param args: 列表結構的子節點
        :param kwargs: 字典結構的子節點
        """
        self.__value: ConfigKey = value
        self.__content: dict[str, Union[ConfigKey, ConfigTree]] = {}
        self.__is_list: bool = is_list
        self.__list_content: list[Union[ConfigKey, ConfigTree]] = []

        if is_list:
            self.__list_content = list(args)
        else:
            self.__content = dict(kwargs)

        # 從我測試環境拿來的代碼，它運行地很好，雖然我想改一下子但是我還是太懶了
        # 構造節點
        if build_with_default:
            if build_dict:
                for key, value in build_dict.items():
                    if isinstance(value, ConfigKey):
                        self.__content[key] = value
                    elif isinstance(value, dict):
                        self.__content[key] = ConfigTree(build_dict=value, build_with_default=True)
                    elif isinstance(value, list):
                        self.__content[key] = ConfigTree(is_list=True, build_list=value, build_with_default=True)
                    elif isinstance(value, ConfigTree):
                        self.__content[key] = value
                    else:
                        self.__content[key] = ConfigKey(default=value)
            elif build_list:
                self.__is_list = True
                for value in build_list:
                    if isinstance(value, ConfigKey):
                        self.__list_content.append(value)
                    elif isinstance(value, dict):
                        self.__list_content.append(ConfigTree(build_dict=value, build_with_default=True))
                    elif isinstance(value, list):
                        self.__list_content.append(ConfigTree(is_list=True, build_list=value, build_with_default=True))
                    elif isinstance(value, ConfigTree):
                        self.__list_content.append(value)
                    else:
                        self.__list_content.append(ConfigKey(default=value))
        else:
            if build_dict:
                for key, value in build_dict.items():
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
            elif build_list and is_list:
                for value in build_list:
                    if isinstance(value, ConfigKey):
                        self.__list_content.append(value)
                    elif isinstance(value, dict):
                        self.__list_content.append(ConfigTree(build_dict=value))
                    elif isinstance(value, list):
                        self.__list_content.append(ConfigTree(is_list=True, build_list=value))
                    elif isinstance(value, ConfigTree):
                        self.__list_content.append(value)
                    else:
                        self.__list_content.append(ConfigKey(value))

    def get(self, key: str) -> Union[ConfigKey]:
        # 检查存储内容是否为列表
        if self.__is_list:
            # 将键转换为整数并返回对应索引处的值
            return self.__list_content[int(key)]
        else:
            # 对于字典存储，直接使用键来获取值
            return self.__content[key]

    def __getitem__(self, item):
        return self.get(item)

    def get_value(self) -> ConfigKey:
        return self.__value

    def read_value(self) -> Union[str, int, float, bool]:
        return self.__value.get()

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key: T, value: T):
        if self.__is_list:
            self.__list_content[int(key)] = value
        else:
            self.__content[key] = value

    def __iter__(self):
        if self.__is_list:
            return iter(self.__list_content)
        else:
            return iter(self.__content)

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

    def __add__(self, other):
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
