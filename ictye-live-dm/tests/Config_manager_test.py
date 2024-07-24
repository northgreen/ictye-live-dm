import pytest
from ictye_live_dm.depends.config_registrar import ConfigRegistrar, ConfigTree, ConfigKey


@pytest.fixture
def registrar():
    return ConfigRegistrar()


def test_init(registrar):
    assert isinstance(registrar.config, ConfigTree)


def test_register_scalar_value(registrar):
    registrar.register('key1', 'value1')
    assert 'key1' in registrar.config
    assert isinstance(registrar.config['key1'], ConfigKey)


def test_register_dict_value(registrar):
    registrar.register('key2', {'nested': 'value2'})
    assert 'key2' in registrar.config
    assert isinstance(registrar.config['key2'], ConfigTree)
    assert registrar.config['key2']['nested'].get() == 'value2'


def test_register_list_value(registrar):
    registrar.register('key3', ['item1', 'item2'])
    assert 'key3' in registrar.config
    assert isinstance(registrar.config['key3'], ConfigTree)
    assert registrar.config['key3'].is_list
    assert registrar.config['key3'].to_list() == ['item1', 'item2']


def test_register_with_default(registrar):
    registrar.register('key4', default='default_value')
    assert registrar.config['key4'].get_default() == 'default_value'


def test_register_with_option(registrar):
    registrar.register('key5', value="opt1", option=['opt1', 'opt2'])
    assert registrar.config['key5'].get_options() == ['opt1', 'opt2']


def test_set(registrar):
    registrar.register('key1', 'initial_value')
    registrar.set('key1', 'new_value')
    assert registrar['key1'] == 'new_value'


def test_dump(registrar):
    registrar.dump({'key6': 'value6'})
    assert 'key6' in registrar.config
    assert registrar.config['key6'] == 'value6'


def test_dump_default(registrar):
    registrar.register('key7', default='default')
    assert registrar.config['key7'].get_default() == 'default'


def test_get(registrar):
    registrar.register('key1', 'value1')
    assert registrar.get('key1') == 'value1'


def test_is_optional(registrar):
    registrar.register('key1', value="test1", optional=True)
    assert registrar.is_optional('key1')


def test_get_option(registrar):
    registrar.register('key1', value="test1", option=['opt1', 'opt2'])
    assert registrar.get_option('key1') == ['opt1', 'opt2']


def test_is_option(registrar):
    registrar.register('key1', value="test1", option=['opt1', 'opt2'])
    assert registrar.is_option('key1')


def test_isset(registrar):
    registrar.register('key1', 'value1')
    assert registrar.isset('key1')


def test_items(registrar):
    registrar.register('key1', 'value1')
    registrar.register('key2', 'value2')
    assert dict(registrar.items()) == {'key1': 'value1', 'key2': 'value2'}


def test_keys(registrar):
    registrar.register('key1', 'value1')
    registrar.register('key2', 'value2')
    assert list(registrar.keys()) == ['key1', 'key2']


def test_values(registrar):
    registrar.register('key1', 'value1')
    registrar.register('key2', 'value2')

    assert registrar.get('key1') == "value1"
    assert registrar.get('key2') == "value2"


def test_to_dict(registrar):
    registrar.register('key1', 'value1')
    registrar.register('key2', 'value2')
    assert registrar.to_dict() == {'key1': 'value1', 'key2': 'value2'}


def test_get_config_tree(registrar):
    assert isinstance(registrar.get_config_tree(), ConfigTree)


def test_getitem(registrar):
    registrar.register('key1', 'value1')
    assert registrar['key1'] == 'value1'


def test_setitem(registrar):
    registrar.register('key1', 'initial_value')
    registrar['key1'] = 'new_value'
    assert registrar['key1'] == 'new_value'


def test_contains(registrar):
    registrar.register('key1', 'value1')
    assert 'key1' in registrar


def test_iter(registrar):
    registrar.register('key1', 'value1')
    registrar.register('key2', 'value2')
    for i, v in registrar:
        if i == 'key1':
            assert v == 'value1'
        if i == 'key2':
            assert v == 'value2'


def test_repr(registrar):
    registrar.register('key1', 'value1')
    assert 'ConfigRegistrar' in repr(registrar)


def test_len(registrar):
    registrar.register('key1', 'value1')
    registrar.register('key2', 'value2')
    assert len(registrar) == 2
