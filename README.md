# JLCS_code_val
小精灵数字验证码识别，目前可以多开，效果简单尝试过，勉强可行，利用通义千问API/字节跳动豆包API实现

# locate.py
实时显示鼠标坐标，显示某个元素的坐标
# request.py
主程序，因为我只有俩小号，目前main程序里头只有两个函数，如果有更多号的话，就把前面的val_first复制一份，把目标窗口名称换了就可以了。
# getname.py
打开这个文件，可以看到上面我定义了一个字符串名为“精灵传说”，如果你有4个号，那么启动这个程序，会显示这四个窗口的名称，这很重要。
# find.py
输入目标窗口的名称，显示这个窗口的坐标，请注意，窗口可以改为800*600分辨率，放置在前台，程序会自动激活窗口。
重要的事情说三遍
# 需要用管理员方式启动程序才可以执行request.py！
# 需要用管理员方式启动程序才可以执行request.py！
# 需要用管理员方式启动程序才可以执行request.py！
需要的配置：
1.安装pycharm，社区版专业版都可以

2.安装anaconda

3.根据程序中需要的库自行安装即可，请注意先安装python 3.7

4.启动request.py时可以用管理员启动终端或者右键管理员启动pycharm

5.API_KEY的获取方式见
https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key?spm=a2c4g.11186623.0.0.49e96b63wucOMt，
也可以选择使用字节跳动豆包，见
https://www.volcengine.com/docs/search?q=%E8%B1%86%E5%8C%85%E5%A4%A7%E6%A8%A1%E5%9E%8B

