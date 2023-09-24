define(["../lib/dm_writer"],
    function(dm_writer) {
        console.log("defult plugin mather is ready")

        var plugin_init = function () {
                console.log("debug:defult_ok")
        }

        var dm_halder = function (message) {
                if(ms.msgtype === "dm"){
                        dm_writer.create_dm(msg.message_body)
                }
                else if (ms.msgtype === "info"){
                        dm_writer.create_info(msg.message_body)
                }
                else {
                        return msg
                }
        }


        // 暴露接口
        return {
                dm_halder: dm_halder,
                plugin_init:plugin_init
        }
}
)