### 启动一个镜像容器
```bash
$ docker run <image_name>
```
如果这个 image 并不存在，docker 会自动下载。
可以加上 变量 `-i`（interactive 交互）和`-t`（tty 命令行）进入到镜像命令行模式。

还可以加上 变量`--name` 添加名字，可用以区分同一image中不同的 **容器**。(PS：举个例子，你可能想在同一个 ubuntu 镜像中发展成两个以上的系统，不同命名就很好区分。若不命名，docker 会自动为你分配一个名字。)

也可以加上 变量`--rm`可以终止其他正在进行的容器。

### 切换状态

在交互式命令行中按住`control`+`p`+`q`可以回到我们真实机器地址下面，但这个时候，容器 是在运行的。当察看状态时，还可以看到此 容器 的状态
```bash
$ docker ps
```
可以通过以下命令回到虚拟交互环境中
```bash
$ docker attach <name>
```
### 终止容器
```bash
$ exit()
```
### 查看现有的镜像
```bash
$ docker images
```
### 删除容器
```bash
$ docker rm -f <container_name>
```
变量`-f`代表`force`，强制删除的意思。

### 删除镜像
```bash
$ docker rmi -f <image_name>
```
其中`rmi`代表`remove image`
