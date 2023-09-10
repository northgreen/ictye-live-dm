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

function websockt(ura){
    if("WebSocket" in window)
    {
        var socket = new WebSocket(ura);
        socket.addEventListener("message",function(event){
            console.log('Message from server ', event.data);
        });

        socket.onopen=function(){
            socket.send('{"code":200,"msg":"ok"}');
        }


    }
    else
    {
        alert("err! your bloser is not sopported!!!")
    }
}

function create_dm(type,content){
    document.getElementsByClassName("danmuji").innerHTML =  document.getElementsByClassName("danmuji").innerHTML + ``;

}

function create_info(type,img_path,content){

}



        window.onload=main();