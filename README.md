# 雨课堂答题提醒工具
本工具适用于网页版荷塘雨课堂(普通雨课堂应该也可以，但是需要改一些代码)线上上课过程中，老师发送题目时播放提示音

有两种方法使用，分别为：

1. 用编译器跑python代码，适合懂代码的人
2. 下载release中的exe文件直接运行，适合图方便或不懂代码的人

步骤1、步骤2两种方法都相同

---

## 步骤1
获取Chrome浏览器软件(直接上网搜之后下载安装)

获取ChromeDriver：在[ChromeDriver官方下载](https://chromedriver.chromium.org/downloads)网站上下载与所安装Chrome浏览器版本相同的文件，解压到任意文件夹

  > 本人所选文件夹为Chrome安装文件夹，典型如："C:\Program Files\Google\Chrome\Application"
  
将上述解压得到的chromedriver.exe所在文件夹添加到系统环境变量PATH中

## 步骤2
编辑"user_data.txt"文件：
* 以字符串形式填入自己的账号密码

---

## 方法1

### 步骤3
下载release中的exe文件，放到与"user_data.txt"文件相同的文件夹中，直接运行即可

## 方法2

### 步骤3
配置python环境，python版本要大于等于3.8

安装requirements.txt中的包，使用命令：

* `pip install -r requirements.txt`

### 步骤4
直接运行"main.py"文件

