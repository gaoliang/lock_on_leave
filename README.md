# 离开自动锁屏
迫于公司检查电脑锁屏。。 写了这么个玩意，检测不到我的脸的时候自动锁屏

## 环境配置
使用了 dlib 和 opencv，因此依赖大量的二进制程序，为了不污染本机环境，推荐使用 anaconda 虚拟环境。

0. 设置 mac 进入睡眠或者屏幕保护程序立即需要密码
1. 安装 anaconda ，创建一个 python3.7 的虚拟环境，并在这个虚拟环境里用 conda 安装 opencv.
2. 参照这个 [gist](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf) 里的教程，编译 dlib，注意最后一步使用 conda 虚拟环境里的 python3
3. 虚拟环境内 pip3 install -r requirements.txt
4. 先保持好姿势，跑一下 init_me.py 保存你的照片（只有第一次需要），然后运行 main.py 