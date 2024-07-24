import pytest
from ictye_live_dm.depends.config_registrar import ConfigKey,ConfigTree


def test_init_default_none():
    with pytest.raises(ValueError):
        ConfigKey()


def test_init_with_default_value():
    key = ConfigKey(default=5)
    assert key.get_default() == 5
    assert not key.is_optional()
    assert key.get() == 5


def test_init_with_optional_true():
    key = ConfigKey(optional=True, value="test v1")
    assert key.is_optional()
    assert key.get_default() == ""
    assert key.get() == "test v1"


def test_init_with_options():
    key = ConfigKey(default=True, option=[True, False])
    assert key.has_option()
    assert True in key.get_options()
    assert False in key.get_options()


def test_set_value():
    key = ConfigKey(value=5)
    key.set(10)
    assert key.is_set()
    assert key.get() != 5
    assert key.get() == 10
    assert key.get_type() is int


def test_set_value_with_type_conversion():
    key = ConfigKey(default=10)
    key.set('20')
    assert key.get() == 20
    assert key.get_type() is int


def test_set_value_out_of_options():
    key = ConfigKey(default=True, option=[True, False])
    with pytest.raises(ValueError):
        key.set('other')


def test_merge_with_non_empty_default():
    key1 = ConfigKey(default=10)
    key2 = ConfigKey(value=20)
    key2.merge(key1)
    assert key2.get_default() == 10


def test_merge_with_options():
    key1 = ConfigKey(option=[1, 2], value=1)
    key2 = ConfigKey(option=[3, 4], value=2)
    key1.merge(key2)
    with pytest.raises(ValueError):
        key1.merge(key2)
    assert 3 in key1.get_options()
    assert 4 in key1.get_options()


def test_merge_with_optional():
    key1 = ConfigKey(optional=False, value=True)
    key2 = ConfigKey(optional=True, value=True)
    key1.merge(key2)
    assert key1.is_optional()


def test_eq():
    key1 = ConfigKey(default=5)
    key2 = ConfigKey(default=5)
    assert key1 == key2


def test_repr():
    key = ConfigKey(default=5, optional=True, option=[1, 2], value=10)
    expected_repr = "ConfigKey(dfault=5, is optional=True, options=[1, 2], value=10)"
    assert repr(key) == expected_repr


# Additional tests for __int__, __float__, __bool__, and __str__
def test_int_conversion():
    key = ConfigKey(default=10)
    assert int(key) == 10


def test_float_conversion():
    key = ConfigKey(default=10.5)
    assert float(key) == 10.5


def test_bool_conversion():
    key_true = ConfigKey(default=True)
    key_false = ConfigKey(default=False)
    assert bool(key_true)
    assert not bool(key_false)


def test_str_conversion():
    key = ConfigKey(default="test")
    assert str(key) == "test"


class TestConfigTree:

    def test_init_dict(self):
        # 测试以字典形式初始化
        config = ConfigTree(build_dict={'key1': 'value1', 'key2': {'subkey': 'subvalue'}})
        assert 'key1' in config._ConfigTree__content
        assert 'key2' in config._ConfigTree__content
        assert isinstance(config._ConfigTree__content['key2'], ConfigTree)

    def test_init_list(self):
        # 测试以列表形式初始化
        config = ConfigTree(is_list=True, build_list=[ConfigKey('value1'), {'subkey': 'subvalue'}])
        assert isinstance(config._ConfigTree__list_content[0], ConfigKey)
        assert isinstance(config._ConfigTree__list_content[1], ConfigTree)

    def test_get(self):
        # 测试获取值
        config = ConfigTree(build_dict={'key': ConfigKey('value')})
        assert config.get('key').get() == 'value'

    def test_set(self):
        # 测试设置值
        config = ConfigTree()
        config.set('key', ConfigKey('value'))
        assert config.get('key').get() == 'value'

    def test_iter(self):
        # 测试迭代
        config = ConfigTree(is_list=True, build_list=[ConfigKey('value1'), ConfigKey('value2')])
        values = [value.get() for value in config]
        assert values == ['value1', 'value2']

    def test_to_dict(self):
        # 测试转换为字典
        config = ConfigTree(build_dict={'key1': ConfigKey('value1'), 'key2': ConfigKey('value2')})
        result_dict = config.to_dict()
        assert result_dict == {'key1': 'value1', 'key2': 'value2'}

    def test_to_list(self):
        # 测试转换为列表
        config = ConfigTree(is_list=True, build_list=[ConfigKey('value1'), ConfigKey('value2')])
        result_list = config.to_list()
        assert result_list == ['value1', 'value2']

    def test_merge_dict_with_dict(self):
        # 测试合并两个字典
        config1 = ConfigTree(build_dict={'key1': ConfigKey('value1')})
        config2 = ConfigTree(build_dict={'key2': ConfigKey('value2')})
        config1.merge(config2)
        assert 'key1' in config1._ConfigTree__content
        assert 'key2' in config1._ConfigTree__content

    def test_merge_list_with_list(self):
        # 测试合并两个列表
        config1 = ConfigTree(is_list=True, build_list=[ConfigKey('value1')])
        config2 = ConfigTree(is_list=True, build_list=[ConfigKey('value2')])
        config1.merge(config2)
        assert len(config1._ConfigTree__list_content) == 2

    def test_merge_incompatible_types(self):
        # 测试合并不同类型引发异常
        config1 = ConfigTree(build_dict={'key1': ConfigKey('value1')})
        config2 = ConfigTree(is_list=True, build_list=[ConfigKey('value2')])
        with pytest.raises(TypeError):
            config1.merge(config2)


# 使用pytest运行测试
if __name__ == "__main__":
    pytest.main()
