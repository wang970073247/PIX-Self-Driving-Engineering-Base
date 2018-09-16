# Autoware 安装指南

## 安装 OpenCV
以 OpenCV2.4.10 为例，具体步骤如下：

### 安装依赖以及工具<br>
    在命令行中输入：
    ```bash
    $ sudo apt-get install build-essential
    $ sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
    $ sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
    ```
### 下载对应版本的 OpenCV
    ```bash
    $ sudo wget https://github.com/Itseez/opencv/archive/2.4.10.zip
    ```
### 编译 OpenCV
    ```bash
    $ sudo apt-get install cmake
    ```
    进入 `/opencv` 目录，新建 `/release` 文件夹，进入该目录，然后执行 `cmake `。
    ```bash
    $ mkdir release 
    $ cd release 
    $ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
    $ sudo make -j4 
    $ sudo make install
    ```
### 配置opencv的环境变量

    打开opencv.conf文件： 
    ```bash
    $ sudo gedit /etc/ld.so.conf.d/opencv.conf 
    ```
    在打开的opencv.conf文件中写入：
    ```bash
    $ /usr/local/lib 
    ```
    保存退出，执行：
    ```bash
    $ sudo ldconfig
    ```
### 测试是否安装成功
    直接在终端敲入命令: 
    ```bash
    $ pkg-config --modversion opencv 
    ```
    显示出版本号2.4.10,说明已经安装成功
## 安装 Qt5
- 通过命令行进行文件下载并进行安装：
    ```bash
    $ wget https://download.qt.io/official_releases/qt/5.11/5.11.1/qt-opensource-linux-x64-5.11.1.run
    $ sudo chmod +x qt-opensource-linux-x64-5.11.1.run
    $ ./qt-opensource-linux-x64-5.11.1.run
    ```
- 进去安装界面，根据提示安装
## 安装 ROS

请确认系统为 Ubuntu 16.04

### 安装 ROS Kinetic
```bash
$ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
$ sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
$ sudo apt-get update
$ sudo apt-get install ros-kinetic-desktop-full
$ apt-cache search ros-kinetic
$ sudo rosdep init
$ rosdep update
$ echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
$ sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential
```
### 测试：
```bash
$ roscore
```
无错误提示，并正在运行，安装成功

更多资料见 [官网](http://wiki.ros.org/kinetic/Installation/Ubuntu)。

## 安装 Autoware
以源码安装方式为例
### 安装依赖项
    ```bash
    $ sudo apt-get update
    $ sudo apt-get install -y python-catkin-pkg python-rosdep python-wstool ros-$ROS_DISTRO-catkin libmosquitto-dev
    ```
### 克隆源码
    ```bash
    $ cd ~
    $ git clone https://github.com/CPFL/Autoware.git --recurse-submodules
    ```
### 安装 Autoware
    ```bash
    $ cd ~/Autoware/ros/src
    $ catkin_init_workspace
    $ cd ..
    $ rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
    $ ./catkin_make_release
    ```
### 运行 Autoware
    ```bash
    $ cd Autoware/ros 
    $ ./run
    ```


当然，大家也可以使用 Docker 安装 Autoware。
更详细的安装教程，请登录 [官方教程](https://github.com/CPFL/Autoware/wiki/Installation)，并可以学习 [使用手册](https://github.com/CPFL/Autoware-Manuals/blob/master/en/Autoware_UsersManual_v1.1.md)。
