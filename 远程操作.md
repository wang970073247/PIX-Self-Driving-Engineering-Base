## 在 Ubuntu Terminal 中 输入：
```bash
$ sudo apt-get install openssh-server
```
## 用命令查找地址：
```bash
$ ifconfig
```
## 在 Mac 端 Terminal 输入：
```bash
$ ssh <name>@<ip_address>
```
## 远程登录 jupyter notebook
```bash
$ jupyter notebook --ip=0.0.0.0 --no-browser
```
然后 **复制** 屏幕显示`:`后面的端口以及 token
在 Mac 端浏览器 **粘贴**，在最前方输入 `<ip_address>`

## 传输数据
```bash
$ scp <path/file or folder> <name>@<ip_address>:<path/file or folder>
```
## 退出远程
```bash
$ exit
```

