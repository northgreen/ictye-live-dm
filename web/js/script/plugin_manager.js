define(
    function (){
        console.info("plugin system is ready")
        let plugin_load = function (){
            //TODO:插件加载
        }

        let message_hader = function (plugin_list) {
            //TODO:消息处理器
        }

        return {
            plugin_load: plugin_load,
            message_halders: message_hader
        }
    }
)