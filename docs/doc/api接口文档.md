# 统一封装
## 连接认证

客户端向服务端发送：
 ``` json
 {"code":200,"msg":ok}
```
服务端返回（msg.ConnectOk）：
``` json
{"code":200,"msg":connect ok}
```
无加密和客户端防伪，但是这些功能希望在以后加入到服务器
# 弹幕接口
## 消息封装
也是json格式，具体如下：
- root：
	- msgtype：消息类型，暂时设有弹幕（Danmku）和消息（Info）
	- message body：消息主题，具体如下

## 消息主体
### dm类型：

- root：
	- msg：消息主体
	- who：消息发送者

注意，这表示消息发送者的身份需要在前端实现

### info类型：

- root：
	- msg：消息内容
	- who：消息的主体人
	- pic url：图片url
	- pic style：图片显示风格，border：边框，irregular：不规则的