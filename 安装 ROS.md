## 安装ROS

系统为 Ubuntu 16.04

安装 ROS Kinetic
``` linux
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
测试：
```linux
$ roscore
```
无错误提示，并正在运行，安装成功

更多资料见 [官网](http://wiki.ros.org/kinetic/Installation/Ubuntu)。