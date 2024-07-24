from typing import Union
import re
from abc import ABCMeta, abstractmethod
from deprecated.sphinx import deprecated

s_dict = "dict"
s_list = "list"

s_int = "int"
s_str = "str"
s_float = "float"
s_bool = "bool"

py_data_type = int | float | str | bool
py_struct_type = dict | list


class ConfigKey:
    """
    一個鍵值，用以存儲配置
    """

    def __init__(self, default: py_data_type = None,
                 optional: bool = False,
                 option: list[py_data_type] = None,
                 value: py_data_type = None):
        if value is None and default is None:
            raise ValueError("None ConfigKey is invalid")
        self.__value = default if value is None else value
        self.__default = __get_type_default__(type(value)) if default is None else default
        self.__optional = optional
        self.__option = option if option else [True, False] if isinstance(default, bool) else None
        # self.__value = value

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

    def get_type(self):
        if self.__value is not None:
            return type(self.__value)
        else:
            return type(self.__default)

    def is_set(self):
        return self.__value is not None

    @property
    def value(self):
        return self.__value if self.__value is not None else self.__default

    @value.setter
    def value(self, value):
        if self.has_option() and value not in self.__option:
            raise ValueError(f"Invalid value for unexpected option: {value}")
        if value is None:
            return
        if self.__default is None:
            self.__default = __get_type_default__(type(self.__value))
        if self.__value is None:
            self.__value = type(self.__default)(value)
            return
        self.__value = type(self.__value)(value)

    @deprecated(version="2.0", reason="Use value instead")
    def set(self, value):
        """
        設置ConfigKey的值，注意的是，此方法會對類型進行强制轉換
        @param value: 目的值
        @return:
        """
        self.value = value

    @deprecated(version="2.0", reason="Use value instead")
    def get(self):
        # 检查是否存在存储的值，如果存在则返回该值，否则返回默认值
        return self.value

    def __repr__(self):
        return (f"ConfigKey(dfault={self.__default}, "
                f"is optional={self.__optional}, "
                f"options={self.__option}, "
                f"value={self.__value})")

    def __int__(self):
        value = self.value
        if isinstance(value, int):
            return value
        else:
            raise TypeError(f"Cannot convert {value} to int")

    def __float__(self):
        value = self.value
        if isinstance(value, float):
            return value
        else:
            raise TypeError(f"Cannot convert {value} to float")

    def __bool__(self):
        value = self.value
        return bool(value)

    def __str__(self):
        value = self.value
        if isinstance(value, str):
            return value
        else:
            return self.__repr__()

    def merge(self, other: "ConfigKey"):
        """
        合併兩個ConfigKey
        1. 如果自身沒有默認值，則會采用other的
        2. 會采取other的数据。
        3. 會采取other的option
        @param other: 另一個ConfigKey
        @return: 合併後的ConfigKey
        """
        if self.__default is __get_type_default__(type(other.value)):
            self.__default = other.get_default()

        self.value = other.value

        if other.has_option():
            self.__option = other.get_options()

        if other.is_optional():
            self.__optional = True

    def __eq__(self, other: Union["ConfigKey", py_data_type]):
        if isinstance(other, ConfigKey):
            return self.value == other.value
        else:
            return self.value == other


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
                 schema: "ConfigSchema" = None,
                 *args: any,
                 **kwargs: any):
        """
        此方法表示配置的树形结构
        @param value: 根植
        @param is_list: 是否为列表，一个树的键值对结构和列表的顺序结构是不同的
        @param build_dict: 此项目用于通过字典构建一个配置树
        @param build_list: 此项目用于通过列表构建一个配置树
        @param build_with_default: 在构建ConfigKey的时候，是否选在将提供的数值作为默认值提供，和build_dict和build_list共同使用
        @param allow: 未实装
        @param tree_lock: 是否允许对结构进行修改，现已弃用，未实装
        @param schema: 配置结构验证器，用于自身结构的验证
        @param args: 作为列表生成配置树的时候可用
        @param kwargs: 作为键值对生成配置树的时候可用
        """

        self.schema = schema
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

    def __getitem__(self, item) -> ConfigKey:
        return self.get(item)

    def get_value(self) -> ConfigKey:
        return self.__value

    def read_value(self) -> py_data_type:
        return self.__value.value

    def __setitem__(self, key: str | int,
                    value: Union[ConfigKey, "ConfigTree"]):
        self.set(key, value)

    def set(self, key: str | int,
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
        """
        @return: 一个列表，包含所有的项目，如果是字典的话返回的可能为一个包含元组的字典
        """
        if self.__is_list:
            return self.__list_content
        else:
            return list(self.__content.items())

    def keys(self) -> list:
        """
        @return:返回键的列表，对于列表来说，这就是它本身
        """
        if self.__is_list:
            return self.__list_content
        else:
            return list(self.__content.keys())

    def values(self) -> py_struct_type:
        """
        @return: 返回值的列表或字典
        """
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
                ret.append(i.value)
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
                ret[k] = v.value
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

    def __eq__(self, other):
        if isinstance(other, ConfigTree):
            if self.is_list() and other.is_list():
                if len(self.__list_content) != len(other.__list_content):
                    return False
                for i in range(len(self.__list_content)):
                    if self.__list_content[i] != other.__list_content[i]:
                        return False
                return True
            elif not self.is_list() and not other.is_list():
                if len(self.__content) != len(other.__content):
                    return False
                for k, v in self.__content.items():
                    if k not in other.__content:
                        return False
                    if v != other.__content[k]:
                        return False
                return True
        else:
            return False

    def append(self, value: ConfigKey, key: str = None):
        if self.__is_list:
            self.__list_content.append(value)
        else:
            self.set(key, value)


class ConfigRegistrar:
    """
    A config registrar that can be used to register config keys.
    """

    _inited = False

    def __init__(self):
        if self._inited:
            return
        self._inited = True
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
        self.config.get(key).value = value

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
            return value.value
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


# config schemas
ic_cfg_type = ConfigTree | ConfigKey


class ABConfigSchema(metaclass=ABCMeta):
    """
    抽象架構認證基礎
    """

    def __init__(self,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ic_cfg_type = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        配置驗證器的抽象構造方法
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        self.not_ = not_
        self.one_of = one_of
        self.all_of = all_of
        self.const = const
        self.description = description
        self.title = title
        self.type_ = None
        self._comment = _comment

    @abstractmethod
    def verify(self, other: ic_cfg_type) -> bool:
        """
        驗證
        @param other: 需要認證的對象
        @return: 是否成功驗證
        """
        ...

    @abstractmethod
    def able(self, other) -> bool:
        """
        驗證此架構認證器是否適用於特定的類型
        @param other: 需要認證的對象
        @return: 此驗證器是否適用於目標對象
        """
        ...

    @classmethod
    def __subclasshook__(cls, par):
        marathons = ["verify", "able"]
        for m in marathons:
            if cls is ConfigSchema:
                if not any(m in B.__dict__ for B in par.__mro__):
                    return NotImplemented
        return True


class ConfigSchema(ABConfigSchema):

    def __init__(self,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ic_cfg_type = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        配置驗證器的構造方法
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        super().__init__(title, description, _comment, const, all_of, any_of, one_of, not_)
        self.type_ = None

    def verify(self, other) -> bool:
        if self.const and not other == self.const:
            return False
        if self.all_of and not all([o.verify(other) for o in self.all_of]):
            return False
        if self.one_of and not any([o.verify(other) for o in self.one_of]):
            return False
        if self.not_ and not any([o.verify(other) for o in self.not_]):
            return False
        return True

    def able(self, other):
        if self.type_ == s_dict:
            return isinstance(other, ConfigTree) and not other.is_list()
        elif self.type_ == s_list:
            return isinstance(other, ConfigTree) and other.is_list()
        elif self.type_ == s_int:
            return isinstance(other, ConfigKey) and other.get_type() == int
        elif self.type_ == s_str:
            return isinstance(other, ConfigKey) and other.get_type() == str
        elif self.type_ == s_float:
            return isinstance(other, ConfigKey) and other.get_type() == float
        elif self.type_ == s_bool:
            return isinstance(other, ConfigKey) and other.get_type() == bool


class StringSchema(ConfigSchema):
    """
    字符串驗證器
    """

    def __init__(self,
                 max_length=None,
                 min_length=None,
                 pattern=None,
                 format_=None,
                 content_media_type=None,
                 content_encoding=None,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ic_cfg_type = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        @param max_length: 最長長度
        @param min_length: 最短長度
        @param pattern: 匹配模式
        @param format_: 格式
        @param content_media_type:
        @param content_encoding:
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        super().__init__(title, description, _comment, const, all_of, any_of, one_of, not_)
        self.content_encoding = content_encoding
        self.content_media_type = content_media_type
        self.format_ = format_
        self.pattern = pattern

        self.min_length = min_length
        self.max_length = max_length

        self.__re = re.compile(pattern) if pattern else None

        self.type_ = s_str

    def verify(self, other: ConfigKey):
        if not super().verify(other):
            return False
        if not self.able(other):
            return False
        value: str = other.value
        if self.min_length and len(value) <= self.min_length:
            return False
        if self.max_length and len(value) >= self.max_length:
            return False
        if self.__re and not self.__re.match(value):
            return False
        if self.format_:
            pass  # TODO
        return True


class IntSchema(ConfigSchema):
    """對整數進行驗證"""

    def __init__(self,
                 maximum=None,
                 minimum=None,
                 exclusive_maximum=None,
                 exclusive_minimum=None,
                 multiple=None,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ic_cfg_type = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        @param maximum: 最大值
        @param minimum: 最小值
        @param exclusive_maximum: 最大值（不包含）
        @param exclusive_minimum: 最小值（不包含）
        @param multiple: 倍數
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        super().__init__(title, description, _comment, const, all_of, any_of, one_of, not_)
        self.type_ = s_int
        self.min_value = minimum
        self.max_value = maximum
        self.exclusive_min_value = exclusive_minimum
        self.exclusive_max_value = exclusive_maximum
        self.multiple = multiple

    def verify(self, other: ConfigKey):
        if not super().verify(other):
            return False
        if not self.able(other):
            return False
        value: int = other.value
        if self.min_value and value < self.min_value:
            return False
        if self.max_value and value > self.max_value:
            return False
        if self.exclusive_min_value and value <= self.exclusive_min_value:
            return False
        if self.exclusive_max_value and value >= self.exclusive_max_value:
            return False
        if self.multiple and value % self.multiple != 0:
            return False
        return True


class FloatSchema(ConfigSchema):
    """
    對浮點數進行驗證
    """

    def __init__(self,
                 maximum=None,
                 minimum=None,
                 exclusive_maximum=None,
                 exclusive_minimum=None,
                 multiple=None,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ic_cfg_type = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        @param maximum: 最大值
        @param minimum: 最小值
        @param exclusive_maximum: 最大值（不包含）
        @param exclusive_minimum: 最小值（不包含）
        @param multiple: 倍數
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        super().__init__(title, description, _comment, const, all_of, any_of, one_of, not_)
        self.type_ = s_float
        self.min_value = minimum
        self.max_value = maximum
        self.exclusive_min_value = exclusive_minimum
        self.exclusive_max_value = exclusive_maximum
        self.multiple = multiple

    def verify(self, other: ConfigKey):
        if not super().verify(other):
            return False
        if not self.able(other):
            return False
        value: float = other.value
        if self.min_value and value < self.min_value:
            return False
        if self.max_value and value > self.max_value:
            return False
        if self.exclusive_min_value and value <= self.exclusive_min_value:
            return False
        if self.exclusive_max_value and value >= self.exclusive_max_value:
            return False
        if self.multiple and value % self.multiple != 0:
            return False
        return True


class BoolSchema(ConfigSchema):
    def __init__(self,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ic_cfg_type = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        super().__init__(title, description, _comment, const, all_of, any_of, one_of, not_)
        self.type_ = s_bool

    def verify(self, other: ConfigKey):
        if not super().verify(other):
            return False
        if not self.able(other):
            return False
        return True


class DictSchema(ConfigSchema):
    """
    對於給定Dict類型進行驗證
    """

    def __init__(self,
                 properties: dict[str, ConfigSchema],
                 pattern_properties: dict[str, ConfigSchema] = None,
                 additional_properties: bool | ConfigSchema = True,
                 required: list[str] = None,
                 min_properties: int = None,
                 max_properties: int = None,
                 property_names: ConfigSchema = None,
                 dependent_required: dict[str, list[str]] = None,
                 dependent_schemas: dict[str, dict[str, ConfigSchema]] = None,
                 if_: ConfigSchema = None,
                 then: ConfigSchema = None,
                 else_: ConfigSchema = None,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ConfigTree | ConfigKey = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        字典模式匹配，用於驗證k-v格式
        @param properties: 對象的屬性，對於給定的鍵使用給定的模式驗證
        @param pattern_properties: 匹配驗證，對於匹配k的屬性使用給定的模式驗證
        @param additional_properties: 附加屬性，如果為假，則允許存在properties和pattern_properties中不存在的鍵，當指定
        config schema的時候，則所有附加的鍵都必須與給定的config schema進行驗證
        @param required: 指定必須的k
        @param min_properties: 最少的屬性數量
        @param max_properties: 最多的屬性數量
        @param property_names: 只驗證名稱而不管它們的值
        @param dependent_required: 需求列表，儅k存在時，list中指定的所以k都必須存在
        @param dependent_schemas: 关键字要求当给定的属性存在时，有条件地应用子模式
        @param if_:
        @param then:
        @param else_:
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        super().__init__(title, description, _comment, const, all_of, any_of, one_of, not_)
        self.else_ = else_
        self.then = then
        self.if_ = if_
        self.dependent_schemas = dependent_schemas
        if property_names and property_names.type_ != s_str:
            raise ValueError("property_names must be string")
        self.dependent_required = dependent_required
        self.property_names = property_names
        self.max_properties = max_properties
        self.min_properties = min_properties
        self.required = required
        self.additional_properties = additional_properties
        self.pattern_properties = pattern_properties
        self.type_ = s_dict
        self.properties = properties

    def __find_additional_properties(self, other: ConfigTree) -> dict:
        k_set: dict = {}
        for k, v in other.items():
            if k in self.properties.keys():
                k_set[k] = v
            if any([re.match(dk, k) for dk, dv in self.pattern_properties]):
                k_set[k] = v
        return k_set

    def verify(self, other: ConfigTree):
        if not super().verify(other):
            return False
        if not self.able(other):
            return False
        value_: list = other.items()
        # 最小值和最大值
        if (self.min_properties
                and len(value_) < self.min_properties):
            return False
        if (self.max_properties
                and len(value_) > self.max_properties):
            return False
        # 检查需求
        if (self.required
                and not all([True if k in self.required else False for k, v in value_])):
            return False
        if (self.property_names
                and not any([self.property_names.verify(v) for k, v in value_ if k in self.properties.keys()])):
            return False
        # 验证模式匹配
        if (self.pattern_properties
                and not all([any([dv.verify(v)
                                  for dk, dv in self.pattern_properties if re.match(dk, k)])
                             for k, v in value_])):
            return False
        if self.additional_properties and isinstance(self.additional_properties, bool):
            if not all([any([dv.verify(v)
                             for dk, dv in self.properties if k == dk])
                        for k, v in value_]):
                return False
        # TODO
        # 附加
        if ((self.additional_properties and self.pattern_properties
             and isinstance(self.additional_properties, ConfigSchema)
             and not any(
                        [self.additional_properties.verify(v)
                         for k, v in value_ if k not in self.properties.keys()
                                               or k not in [k for dk, dv in self.pattern_properties.items()
                                                            if re.match(dk, k)]])) or
                (self.additional_properties and not self.pattern_properties
                 and isinstance(self.additional_properties, ConfigSchema)
                 and not any(
                                [self.additional_properties.verify(v)
                                 for k, v in value_ if k not in self.properties.keys()
                                 ]))):
            return False
        elif self.additional_properties:
            pass
        else:
            if (not all([k in self.properties.keys() for k, v in value_])
                    or not all([k in [k for dk, dv in self.pattern_properties.items() if re.match(dk, k)]
                                for k, v in value_])):
                return False
        return True


class ListSchema(ConfigSchema):

    def __init__(self,
                 items: list[ABConfigSchema] | ABConfigSchema = None,
                 min_items: int = None,
                 max_items: int = None,
                 unique_items: bool = None,
                 title: str = "",
                 description: str = "",
                 _comment: str = "",
                 const: ConfigTree | ConfigKey = None,
                 all_of: list["ABConfigSchema"] = None,
                 any_of: list["ABConfigSchema"] = None,
                 one_of: list["ABConfigSchema"] = None,
                 not_: list["ABConfigSchema"] = None,
                 ):
        """
        列表模式匹配，用於驗證k-v格式
        @param items: 對象的屬性
        @param min_items: 最多包含的物件的數量
        @param max_items: 最少包含物件的數量
        @param unique_items: 需求的物件的數量
        @param title: 標題
        @param description: 描述
        @param _comment: 注釋
        @param const: 常量，代表如果傳入的配置必須和const完全一致
        @param all_of: 必須對所有子模式都有效
        @param any_of: 必须对任何子模式有效
        @param one_of: 必须对恰好一个子模式有效
        @param not_: 不能对给定的模式有效
        """
        super().__init__(title, description, _comment, const, all_of, any_of, one_of, not_)
        self.type_ = s_list
        self.items = items
        self.min_items = min_items
        self.max_items = max_items
        self.unique_items = unique_items

    def verify(self, other: ConfigTree):
        if not super().verify(other):
            return False
        if not self.able(other):
            return False
        value_: list = other.items()
        if (self.min_items
                and len(value_) < self.min_items):
            return False
        if (self.max_items
                and len(value_) > self.max_items):
            return False
        if (self.unique_items
                and len(value_) != len(set(value_))):
            return False
        if not all([self.items[i].verify(v) for i, v in enumerate(value_)]):
            return False
        return True


def __get_type_default__(type_: type):
    """
    獲取類型的默認值，支持str，boo，int，float，其他的樹形結構請使用ConfigTree
    :param type_: 類型
    :return: 默認值
    """
    if type_ == str or type_ == bool or type_ == int or type_ == float:
        return type_()
    else:
        raise ValueError(f"Unsupported type: {type_},may be you can use ConfigTree to build a tree")
