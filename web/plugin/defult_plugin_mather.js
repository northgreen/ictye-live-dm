define(
    function($) {
        console.log("defult plugin mather is ready");

        var ok = function (){console.log("debug:defult_ok")}; //测试用函数

            //计算弹幕存在时间
        var make_time = function (content = ""){return content.message_body.time === void 0 ? content.message_body.time : content.message_body.msg.length * 5;}

            //添加弹幕
        var __add_element = function (content = "",msg_time){

                let id = Math.round(Math.random() * 1000000000);

                /*创建元素到dom*/
                let dm = document.createElement("div");
                dm.innerHTML = content
                let body = document.getElementsByClassName("danmuji")[0];
                body.appendChild(dm);
        }

        //处理info消息
        var _create_info = function (msgbody) {
                /*创建消息*/
                msgbody = ms.message_body;
                let msg = `<div class="special-info">
                            <img src="./usrico.png" class="infousrico">
                                <div class="info-text" class="rightimg">
                                   ${msgbody.msg} 
                                </div>
                                <div class="rightimg-nobother">
                                    <img src="./小花花.png.png" class="rightimg">
                                </div>
                        </div>`;

                let time = make_time(msgbody.msg)
                __add_element(msg,time)

        }

        //处理弹幕消息
        var _create_dm = function (msgbody) {
                 /*创建普通弹幕*/
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

                 let usr;

                 switch (msgbody.who.usr_type) {
                         case 0:
                                 usr = "ptrect"
                                 break
                         case 1:
                                 usr = "fstrect"
                                 break
                         case 2:
                                 usr = "jzrect"
                                 break
                         case 3:
                                 usr = "tdrect"
                                 break
                         case 4:
                                 usr = "zdrect"
                                 break
                         case 5:
                                 usr = "glyrect"
                                 break
                         case 6:
                                 usr = "zbrect"
                                 break
                         default:

                 }

                 msg = `<div class="danmu">
                           <div class="dmlaft">
                               <div class="lbox" >
                                   <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="33" height="31">
                                       <rect width="100%" height="100%" class={usr}/>
                                   </svg>
                               </div>

                               <div class="pname">
                                   ${msgbody.who.name}
                               </div>
                           </div>

                       <div class="dmright">
                           ${msgbody.msg}
                       </div>
                   </div>`;

                 let time = make_time(msgbody.msg)
                 __add_element(msg,time)

        }

        //用于弹幕回调，可以处理
        var create_dm = function (msg) {


                if (ms.message_class === "default"){
                        if(ms.msgtype === "dm"){
                                _create_dm(msg.message_body)
                        }
                        else if (ms.msgtype === "info"){
                                _create_info(msg.message_body)
                        }
                        else {
                                msg = "ok2";
                        }
                }
        };


        // 暴露接口
        return {
                ok: ok,
                create_dm: create_dm
        };
}
)