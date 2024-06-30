from typing import TypeVar, Generic

T = TypeVar('T')


def __get_type_default__(type_: type):
    if type_ == str:
        return ""
    elif type_ == bool:
        return False
    elif type_ == int:
        return 0
    elif type_ == float:
        return 0.0
    elif type_ == list:
        return []
    elif type_ == dict:
        return {}
    elif type_ == tuple:
        return ()
    elif type_ == set:
        return set()
    elif isinstance(type_, type(None)):
        return None
    else:
        raise ValueError(f"Unsupported type: {type_}")


class ConfigKey(Generic[T]):
    """
    A config key that can be registered to the ConfigRegistrar.
    """

    def __init__(self, default: T = None, optional: bool = False, option: list[T] = None, value: T = None):
        self.default = __get_type_default__(type(value)) if default is None else default
        self.optional = optional
        self.option = option
        self.value = value

    def get_default(self):
        return self.default

    def is_optional(self):
        return self.optional

    def is_option(self):
        return self.option is not None

    def get_option(self):
        return self.option

    def set(self, value):
        if self.option is not None and value not in self.option:
            raise ValueError(f"Invalid value for option: {value}")
        self.value = value

    def isset(self):
        return self.value is not None

    def get(self):
        return self.value if self.value is not None else self.default


class ConfigRegistrar:
    """
    A config registrar that can be used to register config keys.
    """

    def __init__(self):
        self.config = {}

    def register(self, key, value=None, default=None, optional: bool = False, option: list = None):
        """
        Register a config key.
        @param key: key name
        @param value: config value
        @param default: config default value, if not provided, will use the value type's default value
        @param optional: is this config key optional
        @param option: list of valid options for this config key
        """
        if key in self.config:
            raise ValueError(f"Config key '{key}' already registered")
        self.config[key] = ConfigKey(default, optional, value=value, option=option)

    def set(self, key, value):
        """
        Set the value of a config key.
        @param key: key name
        @param value: config value
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        self.config[key].set(value)

    def get(self, key):
        """
        Get the value of a config key.
        @param key: key name
        @return: config value
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config[key].get()

    def is_optional(self, key):
        """
        Check if a config key is optional.
        @param key: key name
        @return: True if optional, False otherwise
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config[key].is_optional()

    def get_option(self, key):
        """
        Get the valid options for a config key.
        @param key: key name
        @return: list of valid options
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config[key].get_option()

    def is_option(self, key):
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config[key].is_option()

    def isset(self, key):
        """
        Check if a config key is set.
        @param key: key name
        @return: True if set, False otherwise
        """
        if key not in self.config:
            raise ValueError(f"Config key '{key}' not registered")
        return self.config[key].isset()

    def to_dict(self):
        """
        Convert the config registrar to a dictionary.
        @return: dictionary representation of the config registrar
        """
        return {key: self.config[key].get() for key in self.config}

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

    def items(self):
        return self.config.items()

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()

    def __len__(self):
        return len(self.config)
