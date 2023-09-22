require.config({
    baseUrl:"/"
})
define(["js/plugin/default_plugin_mather","js/script/plugin_manager"],
    function ($){
    function main()
    {
                console.log("lod ready");
                //请求ws地址
                req = new XMLHttpRequest();

                req.open("get","/websocket",true);

                req.onreadystatechange=function(){
                    if(req.readyState === XMLHttpRequest.DONE && req.status === 200){
                        websockt(JSON.parse(req.responseText).local);
                    }

                }
                req.send();

    }

    let connect_ok = void 0

    function websockt(ura){
        if("WebSocket" in window) {
            var socket = new WebSocket(ura);
            socket.addEventListener("message",function(event){
                console.log('Message from server ', event.data);
                if (event.data === "{\"code\": 200, \"msg\": \"connect ok\"}"){
                    console.info("connect to seriver success")
                    connect_ok = 1
                }else if (connect_ok === 1) {
                    let data;
                    data = $.create_dm(event.data) //处理标准消息
                    if (!data) {
                        //TODO:处理非标准消息
                    }
                }
            });
            socket.onopen=function(){
                socket.send('{"code":200,"msg":"ok"}');
            }
        }
        else {
            alert("err! your bloser is not sopported!!!")
        }
    }

    window.onload=main();
    }
)