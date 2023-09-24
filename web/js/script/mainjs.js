require.config({
    baseUrl:"/"
})
define(["js/plugin/default_plugin_mather","js/script/plugin_manager"],
    function ($){
    function main()
    {
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
                req = new XMLHttpRequest()

                req.open("get","/get_websocket",true)

                req.onreadystatechange=function(){
                    if(req.readyState === XMLHttpRequest.DONE && req.status === 200){
                        //websockt(`ws://${window.location.host}/websocket`)
                        websockt(JSON.parse(req.responseText).local)
                    }

                }
                req.send()

    }

    let connect_ok = void 0

    function websockt(ura){
        if("WebSocket" in window) {
            var socket = new WebSocket(ura)
            socket.addEventListener("message",function(event){
                console.log('Message from server ', event.data)
                if (event.data === "{\"code\": 200, \"msg\": \"connect ok\"}"){
                    console.info("connect to seriver success")
                    connect_ok = 1
                }else if (connect_ok === 1) {
                    let data
                    data = $.create_dm(event.data) //处理标准消息
                    if (!data) {
                        //TODO:处理非标准消息
                    }
                }
            })
            socket.onopen=function(){
                socket.send('{"code":200,"msg":"ok"}')
            }
        }
        else {
            alert("err! your bloser is not sopported!!!")
        }
    }

    window.onload=main()
    }
)