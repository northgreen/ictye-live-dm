require.config({
    baseUrl: "/js/plugin/"
})
define(
    function (){
        console.info("plugin system is ready")
        //消息插件获取
        let plugin_load = function (){
            let get_plugin = new XMLHttpRequest()
            let plugin_list = []

            get_plugin.open("get","/api/plugin_list",false)
            //回调
            get_plugin.onreadystatechange = function () {
                if (get_plugin.readyState === XMLHttpRequest.DONE && get_plugin.status === 200) {
                    let req = JSON.parse(get_plugin.responseText)
                    plugin_list = req.list
                }
            }
            get_plugin.send()
            return plugin_list
        }

        let plugin_list = plugin_load()
        //消息插件列表
        let plugin_message_handler = {}
        //消息插件注册
        for (let x in plugin_list){
            require([plugin_list[x]],function (plugin){
                plugin_message_handler[plugin.message_class] = plugin.dm_halder
            })
        }

        /*消息回调*/
        let message_handler = function (message) {
           if (Object.keys(plugin_message_handler).length !== 0){
               plugin_message_handler[message.message_class](message)
           }
        }

        return {
            plugin_load: plugin_load,
            message_handlers: message_handler,
            plugin_list: plugin_list
        }
    }
)