<div align="center">
<img src="https://github.com/northgreen/ictye-live-dm/raw/dev/icon.png">
</img>
<h1 style="margin-top:0">Ictye Live Danmku(ictye-live-dm)</h1>
<img src="https://img.shields.io/badge/python-3.10-blue">
</img>
<img src="https://img.shields.io/badge/license-GPL-green">
</img>
</div>

一个简单而又全能的弹幕姬框架（其实就是一个web服务器加上websocket服务器），通过插件来实现弹幕功能

# 使用发行版
1. 到release里
2. 下载最新的版本
3. 如果是Windows用户则可以直接运行其中的启动脚本，Linux和mac用户可以根据requirements.txt配置环境后运行，建议是运行在venv环境中。

## 开始使用它

1. 部署ictye live Danmku：你只需要简单的解压它就好，默认情况的启动脚本是为Windows用户提供的，不过在非Windows操作系统上，你仍旧可以使用`requirement.txt`来配置环境并且使用`python -m ictye-live-Danmku`来启动项目
2. 配置项目：
   1. 这个软件是通过插件的形式来实现弹幕的获取，弹幕的分析和处理
   2. `/plugin`里放置python脚本插件，可以在后端提供弹幕，分析弹幕以及提供前端接口等待
   3. `/web/`里都是前端的资源，其中`/web/api`和`/web/cgi`是一个占位用的文件夹（方便开发。。。。。。。。。），`/web/js/`中是存放的前端的脚本，此外，你可以编辑style内的文件来定义你自己的样式

这个项目目前完全是我一个人开发（属实有点离谱），如果有想参加开发的可以联系我。。。。。。

剩余的工作：
- 找bug和打补丁。。。。。。。。。
- 稳定性校验