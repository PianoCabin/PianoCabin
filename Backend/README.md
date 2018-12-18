# 配置指南

## Windows

* 安装Redis：前往https://github.com/MicrosoftArchive/redis/releases下载相关msi文件点击安装
* 安装MySQL：前往https://dev.mysql.com/downloads/mysql/下载安装MySQL Server
* 配置MySQL数据库：
  * 打开MySQL CommandLine应用，输入密码
  * 输入`create database piano_cabin;`
* 根据本地数据库情况及小程序信息等配置configs.json文件，置于Backend目录中
* 打开PowerShell，运行`python manage.py makemigrations`，再运行`python manage.py migrate`

## Ubuntu

- 安装Redis：命令行输入`sudo apt-get install redis-server`
- 安装MySQL：参考http://www.cnblogs.com/zhuyp1015/p/3561470.html
- MySQL需要修改默认字符集为Unicode，
- 配置MySQL数据库：
  - 命令行输入`mysql -u root -p`
  - 输入`create database piano_cabin;`
- 根据本地数据库情况及小程序信息等配置configs.json文件，置于Backend目录中
- 打开PowerShell，运行`python manage.py makemigrations`，再运行`python manage.py migrate`