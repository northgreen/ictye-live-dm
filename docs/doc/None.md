# 想要实现但是没有实现的功能
`pluginsystem.py`

```python
# TODO:修不起这个bug了，谁爱修谁修。。。。。。。。。。。。。。。

for plugin_file in confi["plugins"]["others_plugin"]:
    plugin_name = plugin_file
    try:
        if plugin_file is not None:
            mlogger.info(f"loading plugin{plugin_file}")
            path = os.path.normpath(plugin_file)
            if os.path.isdir(plugin_name):
                spec = importlib.util.spec_from_file_location(os.path.dirname(path), "__init__.py")
            else:
                spec = importlib.util.spec_from_file_location(os.path.dirname(path), os.path.basename(path))
            if spec is None:
                mlogger.error(f"no modle on {path}")
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # 检查是否实现了主方法
            if not hasattr(module, "PluginMain"):
                raise plugin_errors.NoMainMather("函数未实现主方法或者主方法名称错误")
            plugin_main_class: plugin_main.PluginMain = module.PluginMain

            # 获取插件类型
            if plugin_main_class.plugin_type() == "message":
                self.message_plugin_list.append(plugin_main_class)
            elif plugin_main_class.plugin_type() == "analyzer":
                self.analyzer_plugin_list.append(plugin_main_class)
            else:
                raise plugin_errors.PluginTypeError("未知的插件类型，该不会是插件吃了金克拉了吧？")

            # 注册插件cgi
            if plugin_main_class.sprit_cgi_support:
                if plugin_main_class.sprit_cgi_path:
                    self.plugin_cgi_support[plugin_main_class.sprit_cgi_path] = plugin_main_class.cgi_face
                else:
                    raise

            # 注册js脚本
            if plugin_main_class.plugin_js_sprit_support:
                self.plugin_js_support[plugin_main_class.plugin_name] = plugin_main_class.plugin_js_sprit
    except ImportError as e:
        mlogger.error(f"failed to import plugin {plugin_name:{str(e)}}")

```