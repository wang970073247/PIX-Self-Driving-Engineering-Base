# Autoware 安装指南

## 安装 ROS kinetic
按照之前的 ROS 安装教程成功安装 ROS kinetic。
## 安装 OpenCV
以 OpenCV2.4.13 为例，具体步骤如下：
- 安装依赖以及工具<br>
    在命令行中输入：
    ```bash
    $ sudo apt install build-essential
    $ sudo apt install cmake git libgtk2.0-dev pkg-config
    $ sudo apt install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
    ```
- 下载对应版本的 OpenCV
    ```bash
    $ sudo wget https://github.com/Itseez/opencv/archive/2.4.13.zip
    ```
- 解压并编译文件
    ```bash
    $ sudo unzip opencv-2.4.13
    $ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
    $ make -j4
    $ sudo make install
    ```
## 安装 Qt5
- 通过命令行进行文件下载并进行安装：
    ```bash
    $ wget https://download.qt.io/official_releases/qt/5.11/5.11.1/qt-opensource-linux-x64-5.11.1.run
    $ sudo chrome +x qt-opensource-linux-x64-5.11.1.run
    $ ./qt-opensource-linux-x64-5.11.1.run
    ```
- 进去安装界面，根据提示安装
## 安装 Autoware
以源码安装方式为例
- 安装依赖项
    ```bash
    $ sudo apt-get update
    $ sudo apt-get install -y python-catkin-pkg python-rosdep python-wstool ros-$ROS_DISTRO-catkin libmosquitto-dev
    ```
- 克隆源码
    ```bash
    $ cd ~
    $ sudo git clone https://github.com/CPFL/Autoware.git --recurse-submodules
    ```
- 安装 Autoware
    ```bash
    $ cd ~/Autoware/ros/src
    $ catkin_init_workspace
    $ cd ../
    $ rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
    $ ./catkin_make_release
    ```
- 运行 Autoware
    ```bash
    $ cd Autoware/ros 
    $ ./run
    ```


当然，大家也可以使用 Docker 进行安装。
更详细的安装教程，请登录 [官方教程](https://github.com/CPFL/Autoware/wiki/Installation)，并可以学习 [使用手册](https://github.com/CPFL/Autoware-Manuals/blob/master/en/Autoware_UsersManual_v1.1.md)。
