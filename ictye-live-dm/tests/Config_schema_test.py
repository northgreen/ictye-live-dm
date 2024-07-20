import pytest

from ictye_live_dm.depends import config_registrar
from ictye_live_dm.depends.config_registrar import StringSchema, IntSchema, FloatSchema, BoolSchema, \
    DictSchema, ListSchema, ConfigTree, ConfigKey


# Fixtures to create some basic ConfigKey and ConfigTree instances
@pytest.fixture
def config_key_str():
    return config_registrar.ConfigKey('testss')


@pytest.fixture
def config_key_int():
    return config_registrar.ConfigKey(10)


@pytest.fixture
def config_key_float():
    return config_registrar.ConfigKey(10.5)


@pytest.fixture
def config_key_bool():
    return config_registrar.ConfigKey(True)


@pytest.fixture
def config_tree_dict():
    return config_registrar.ConfigTree(build_dict={'name': 'John', 'age': 30})


@pytest.fixture
def config_tree_list():
    return config_registrar.ConfigTree(is_list=True, build_list=['test1', 'test2'])


# Tests for StringSchema
def test_string_schema(config_key_str):
    schema = StringSchema(max_length=10, min_length=5, pattern=r'^\w+$')
    assert schema.verify(config_key_str) == True
    config_key_str.set('test')
    assert schema.verify(config_key_str) == False
    config_key_str.set('12345678901')
    assert schema.verify(config_key_str) == False


# Tests for IntSchema
def test_int_schema(config_key_int):
    schema = IntSchema(maximum=10, minimum=5, exclusive_maximum=False, exclusive_minimum=False)
    assert schema.verify(config_key_int) == True
    config_key_int.set(11)
    assert schema.verify(config_key_int) == False
    config_key_int.set(4)
    assert schema.verify(config_key_int) == False


# Tests for FloatSchema
def test_float_schema(config_key_float):
    schema = FloatSchema(maximum=10.5, minimum=5.5, exclusive_maximum=False, exclusive_minimum=False)
    assert schema.verify(config_key_float) == True
    config_key_float.set(11)
    assert schema.verify(config_key_float) == False
    config_key_float.set(4)
    assert schema.verify(config_key_float) == False


# Tests for BoolSchema
def test_bool_schema(config_key_bool):
    schema = BoolSchema()
    assert schema.verify(config_key_bool) == True


# Tests for DictSchema
def test_dict_schema(config_tree_dict):
    properties = {
        'name': StringSchema(),
        'age': IntSchema()
    }
    schema = DictSchema(properties)
    assert schema.verify(config_tree_dict) == True
    config_tree_dict['age'] = ConfigKey('30')
    assert schema.verify(config_tree_dict) == False


# Tests for ListSchema
def test_list_schema(config_tree_list):
    schema = ListSchema(items=[StringSchema()])
    assert schema.verify(config_tree_list) == True
    config_tree_list.append(123)
    assert schema.verify(config_tree_list) == False
