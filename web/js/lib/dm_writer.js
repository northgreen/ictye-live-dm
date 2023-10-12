require.config({
  packages: [
        {
            name: 'crypto-js',
            location: 'https://cdn.bootcdn.net/ajax/libs/crypto-js/4.1.1/',
            main: 'index'
        }
    ]
});
define(["crypto-js/md5"],
    function (md5) {
        let ok = function (){console.log("debug:defult_ok")}; //测试用函数

            //计算弹幕存在时间
        let make_time = function (content = ""){return  content.length}

            //添加弹幕
        let __add_element = function (content = "",msg_time){

                let id = md5(Math.round(Math.random() * 1000000000).toString() + content)
                console.log("id:"+id)

                /*创建元素到dom*/
                let dm = document.createElement("div")
                dm.setAttribute("id",id)
                dm.innerHTML = content
                let body = document.getElementsByClassName("danmuji")[0]
                body.appendChild(dm)
                
                setTimeout(function (id = Number,element) {
                    dm.classList.add("faded_out")
                    dm.addEventListener("animationend",function () {
                        dm.parentElement.removeChild(dm)
                        console.info("removed "+id)
                    })
                },msg_time*1000,id,dm)
        }

        //处理info消息
         let create_info = function (msgbody) {
                /*创建消息*/
                let msg = `<div class="special-info">
                            <img src="${msgbody.who.face}" class="infousrico">
                                <div class="info-text" class="rightimg">
                                   ${msgbody.msg} 
                                </div>
                                <div class="${msgbody.pic.border?"rightimg-bother":"rightimg_noborder"}">
                                    <img src="${msgbody.pic.pic_url}" class="rightimg">
                                </div>
                        </div>`
                let time
                if ("time" in msgbody){
                    time = msgbody.time
                }else {
                    time = make_time(msgbody.msg)
                }
                __add_element(msg,time)

        }

        //处理弹幕消息
        let create_dm = function (msgbody) {
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
            let usr

            switch (msgbody.who.type) {
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
                    usr = "ptrect"

            }

                 msg = `<div class="danmu">
                           <div class="dmlaft">
                               <div class="lbox" >
                                   <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="33" height="31">
                                       <rect width="100%" height="100%" class=${usr} />
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
                let time
                 if ("time" in msgbody){
                     time = msgbody.time
                 }else {
                     time = make_time(msgbody.msg)
                 }
                 __add_element(msg,time)

        }

        return {
            create_info:create_info,
            create_dm:create_dm
        }
    }
)