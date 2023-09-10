define(
    function($) {
        console.log("ok");
        var ok = function ok(){
                console.log("debug:defult_ok")
        };
        var create_dm = function create_dm(msg) {

                function get_dm(ms) {
                        let msg
                        if (ms.message_class === "default"){
                                if(ms.msgtype === "dm"){
                                        const msgbody = ms.message_body
                                        /*
                                        * 身份等级：
                                        * 0 ：观众
                                        * 1 ：粉丝团/赞助用户
                                        * 2 ：舰长/普通付费用户
                                        * 3 ：提督/中级付费用户
                                        * 4 ：总督/高级付费用户
                                        * 5 ：管理员/房管
                                        * 6 ：主播
                                        */


                                        msg = `<div class="danmu">
                                                    <div class="dmlaft">
                                                        <div class="lbox" >
                                                            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="33" height="31">
                                                                <rect width="100%" height="100%" class="ptrect"/>
                                                            </svg>
                                                        </div>

                                                        <div class="pname">
                                                            ${msgbody.who.name}
                                                        </div>
                                                    </div>

                                                <div class="dmright">
                                                    ${msgbody.msg}
                                                </div>
                                            </div>`
                                }
                                else if (ms.msgtype === "info"){

                                }

                        }
                        else {
                                msg = "ok2"
                        }

                        return msg
                }

                let dm = document.createElement("div");
                dm.innerHTML = get_dm(msg)
                let body = document.getElementsByClassName("danmuji")[0];
                body.appendChild(dm)


        };

        window.onload = function (){

        };

        // 暴露接口
        return {
                ok: ok,
                create_dm: create_dm
        };
        // TODO:添加弹幕的方法
}
)