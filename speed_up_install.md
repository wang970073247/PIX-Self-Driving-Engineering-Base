## `apt-get install` 
`apt-fast` 通过使用多线程下载来给 `apt-get` 提速。
  - 添加软件源并安装

  ```bash
  $ sudo add-apt-repository ppa:apt-fast/stable
  $ sudo apt-get update
  $ sudo apt-get -y install apt-fast
  ```
  在弹出的对话框中选择 `apt-get`。
  - 使用
  
  安装完成之后使用方法和 `apt-get` 是一样的。
  ```bash
  sudo apt-fast install <software>
  ```
更多详情，请登录这个项目的 [地址](https://github.com/ilikenwf/apt-fast)。

## `pip install` 
同样存在下载缓慢的问题，通过换国内的源解决。
  - 使用
  ```bash
  pip install <package> -i https://pypi.douban.com/simple
  ```
