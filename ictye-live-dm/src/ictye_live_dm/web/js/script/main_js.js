require.config({
    baseUrl: "/"
})
define(["js/script/plugin_manager"],
    function (pm) {
        function main() {
            console.log("lod ready")
            //请求ws地址
            console.log(`
            __                         ___                                __                                      __          __  __  ______                                             ___             
 __        /\\ \\__                     /\\_ \\    __                        /\\ \\                                    /\\ \\        /\\ \\/\\ \\/\\__  _\\                                           /\\_ \\            
/\\_\\    ___\\ \\ ,_\\  __  __     __     \\//\\ \\  /\\_\\  __  __     __        \\_\\ \\    ___ ___       __  __  __     __\\ \\ \\____   \\ \\ \\ \\ \\/_/\\ \\/         ___    ___     ___     ____    ___\\//\\ \\      __   
\\/\\ \\  /'___\\ \\ \\/ /\\ \\/\\ \\  /'__\`\\     \\ \\ \\ \\/\\ \\/\\ \\/\\ \\  /'__\`\\      /'_\` \\ /' __\` __\`\\    /\\ \\/\\ \\/\\ \\  /'__\`\\ \\ '__\`\\   \\ \\ \\ \\ \\ \\ \\ \\        /'___\\ / __\`\\ /' _ \`\\  /',__\\  / __\`\\\\ \\ \\   /'__\`\\ 
 \\ \\ \\/\\ \\__/\\ \\ \\_\\ \\ \\_\\ \\/\\  __/      \\_\\ \\_\\ \\ \\ \\ \\_/ |/\\  __/     /\\ \\L\\ \\/\\ \\/\\ \\/\\ \\   \\ \\ \\_/ \\_/ \\/\\  __/\\ \\ \\L\\ \\   \\ \\ \\_\\ \\ \\_\\ \\__    /\\ \\__//\\ \\L\\ \\/\\ \\/\\ \\/\\__, \`\\/\\ \\L\\ \\\\_\\ \\_/\\  __/ 
  \\ \\_\\ \\____\\\\ \\__\\\\/\`____ \\ \\____\\     /\\____\\\\ \\_\\ \\___/ \\ \\____\\    \\ \\___,_\\ \\_\\ \\_\\ \\_\\   \\ \\___x___/'\\ \\____\\\\ \\_,__/    \\ \\_____\\/\\_____\\   \\ \\____\\ \\____/\\ \\_\\ \\_\\/\\____/\\ \\____//\\____\\ \\____\\
   \\/_/\\/____/ \\/__/ \`/___/> \\/____/     \\/____/ \\/_/\\/__/   \\/____/     \\/__,_ /\\/_/\\/_/\\/_/    \\/__//__/   \\/____/ \\/___/      \\/_____/\\/_____/    \\/____/\\/___/  \\/_/\\/_/\\/___/  \\/___/ \\/____/\\/____/
                        /\\___/                                                                                                                                                                           
                        \\/__/                                                                                                                                                                            
                `)

            //请求websocket
            let req = new XMLHttpRequest()
            req.open("get", "/get_websocket", true)
            req.onreadystatechange = function () {
                if (req.readyState === XMLHttpRequest.DONE && req.status === 200) {
                    //启动websocket
                    websocket(JSON.parse(req.responseText).local)
                }
            }


            req.send()
        }
        let connect_ok = void 0;
        function websocket(ura) {
            if ("WebSocket" in window) {
                let socket = new WebSocket(ura)
                socket.addEventListener("message", function (event) {
                    console.log('Message from server ', event.data)
                    if (event.data === "{\"code\": 200, \"msg\": \"connect ok\"}") {
                        connect_ok = 1
                    } else if (connect_ok === 1) {
                        console.info("cok is " + event.data)
                        let msg = JSON.parse(event.data)
                        //消息处理
                        pm.message_handlers(msg)
                    }
                })

                socket.onopen = function () {
                    // 获取浏览器get参数
                    let get_params = window.location.href
                    let params = new URLSearchParams(get_params)
                    let param = {}
                    params.forEach(function (value, key) {
                        param[key] = value
                    })
                    console.log("params:", param)
                    // 发送消息给服务器
                    socket.send(JSON.stringify({ "code": 200, "msg": "ok", "param": param }))
                }
            }
            else {
                alert("err! your browser is not supported!!!")
            }
        }
        main()
    })

