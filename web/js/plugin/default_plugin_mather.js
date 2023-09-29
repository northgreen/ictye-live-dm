define(["../lib/dm_writer"],
    function(dm_writer) {
        console.log("defult plugin mather is ready")

        var plugin_init = function () {
                console.log("debug:defult_ok")
        }

        var dm_halder = function (ms) {
                if(ms.msg_type === "dm"){
                        dm_writer.create_dm(ms.message_body)
                        console.debug("creating dm"+ms.message_body)
                }
                else if (ms.msg_type === "info"){
                        dm_writer.create_info(ms.message_body)
                        console.debug("creating dm"+ms.message_body)
                }
                else {
                        return ms
                }
        }


        // 暴露接口
        return {
                dm_halder: dm_halder,
                plugin_init:plugin_init
        }
}
)