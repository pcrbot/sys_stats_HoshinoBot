# sys_stats_HoshinoBot
检查bot服务器的硬件信息（适用于Linux和Windows）  

没什么技术含量，都是直接调库读取的，在linux下也可以直接读文件，但我搞不太来，写好发我（）

之前看到了[pcrbot/advance_check_hoshinobot](https://github.com/pcrbot/advance_check_hoshinobot)，想用一下，发现[SYoung](https://github.com/Soung2279)大佬是用wmi库写的，这个库在linux下不太好使，就摸了一个linux版的（其实win也能用，我是现在win写好再去服务器加linux功能的）

需要以下库
```
psutil
distro
```
手动pip install吧，懒得弄requirements了。

# 安装和使用方法
1. 在hoshino/modules下clone本仓库`git clone https://github.com/pcrbot/sys_stats_HoshinoBot.git`  
2. 在hoshino/config/\_\_bot\_\_.py中加入
```
MODULES_ON = {
...
'sys_stats_HoshinoBot',  # 硬件信息
}
```
3. 重启hoshino

在群内发送`@bot check` `@bot 自检` `@bot 鲁大师`即可。

# 效果
bot会发送如下内容：  
```
System Info:
平台:
 运行平台: CentOS Linux 7.9.2009
 机器类型: x86_64
cpu:
 内核数: 2
 逻辑CPU: 2
 基准速度: 2.60 GHz
 利用率: 4.9 (在0.2秒内)
物理内存:
 总物理内存: 3.7G
 已使用: 2.2G (67.8%)
 剩余: 1.2G
swap
 swap总大小: 1024.0M
 已使用: 128.5M (12.5%)
 剩余: 895.5M
 累计I/O: 25.1M / 175.4M
硬盘:
 标识: /dev/vda1 挂载点: / 总空间: 58.9G 已使用: 35.1G (62.2%) 剩余: 21.3G
```

# 日志
2022/03/25 摸了。  
2022/03/27 fix WinServer存在一个CD驱动器导致读取硬盘信息报错 [#1](https://github.com/pcrbot/sys_stats_HoshinoBot/issues/1)  
2022/03/27 在windows下取消输出swap的累计I/O（恒为0）