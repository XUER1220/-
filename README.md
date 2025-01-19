项目名称：人脸马赛克网页

开发人员：蔡逸雪、豆一帆、梁雅雯、林俞芊

项目说明：

# 一.项目结构（主要）

+ .idea文件夹：存储IntelliJ IDEA项目的配置信息。

+ assets文件夹：存储上传及保存的图片和视频。
    + uploads文件夹：上传的图片及视频。
    + photo文件夹：打码处理后，保存的图片。
    + video文件夹：打码处理后，保存的视频。

+ static文件夹：前端文件
    + script.js
    + styles.css

+ templates文件夹：前端文件
    + index.html

+ app.py：图片和视频的上传、处理和保存系统

+ photo.py：用于处理图片文件

+ video.py：用于处理视频文件


# 二.项目使用流程：
## 1.准备
打开并运行app.py，进入http://127.0.0.1:5000， 您可以看到欢迎界面。

## 2.上传图片或视频
从欢迎界面向下翻页后，您可以看到操作界面。

点击“选择文件”按钮并选择您想处理的图片或视频。

点击“上传”按钮后，您就可以对文件中的人脸进行打码操作。

## 3.打码
系统会识别文件中的人脸并允许您选择需要打码的人脸。

您可以通过点击人脸区域进行添加或取消打码。当人脸未被选择时框选住人脸的框架为红色，当人脸被选择并被马赛克时框选住人脸的框架为绿色。

## 4.保存
您可以实时查看处理效果，点击“保存”按钮，即可把您处理的文件保存下来，方便您未来的使用。

# 三.声明：

隐私保护：本团队承诺，将严格遵守相关法律法规，保护用户隐私。

免责声明：人脸马赛克网页提供的处理仅供参考，不构成任何法律或其他专业建议。

适用法律：本声明适用于人脸马赛克网页的所有服务，适用中华人民共和国法律。

争议解决：如因使用人脸马赛克网页产生争议，双方应友好协商解决。
