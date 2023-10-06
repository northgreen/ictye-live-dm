require.config({
    baseUrl: "/js/plugin/"
})
define(
    function (){
        console.info("plugin system is ready")
        let plugin_list = plugin_load()

        let plugin_load = function (){
            let get_plugin = new XMLHttpRequest()
            let plugin_list = []

            get_plugin.open("get","/api/plugin_list",false)

            get_plugin.onreadystatechange = function () {
                if (get_plugin.readyState === XMLHttpRequest.DONE && get_plugin.status === 200) {
                    let req = JSON.parse(get_plugin.responseText)
                    plugin_list = req.list
                }
            }
            get_plugin.send()
            /*
            for(let a in plugin_list){
                let plugin
                require([plugin_list[a]],function (plug) {
                    plugin = plug
                })
                plugins[plugin_list[a]] = plugin
            }
            console.info("az")
            * */
            console.info(plugin_list)

            return plugin_list
            // TODO :剩余工作
        }

        let message_hader = function (plugin_list) {
            //TODO:消息处理器
        }

        return {
            plugin_load: plugin_load,
            message_halders: message_hader,
            plugin_list: plugin_list
        }
    }
)