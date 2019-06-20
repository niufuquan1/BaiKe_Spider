# BaiKe_Spider
#### 版本1：Spider1.py -u url -d deep -k keyword
#### 版本2：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  -s
#### 版本3：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  -s -t number
#### 版本4：剩下所有功能

---
---
### 版本1：
  
  实现如下参数：-u url -d deep -k keyword 默认不传递url，url默认入口是https://baike.baidu.com/。-d 默认为 1
  
  测试可用命令：`python Scheduler.py -k uestc `
---
### 版本2：
  
  实现如下参数：-u url -d deep -k keyword -l loglevel -f logfile -s，url默认入口是https://baike.baidu.com/。 -d 默认为 1；-f为日志名称，默认为BaiKeSpider；-l为日志等级，默认为1；-s是判断是否进行自测，即doctest，添加该参数则进行，不添加不影响程序运行
  
  测试可用命令：`python Scheduler.py -k uestc -d 2 -l 3 -f myLog -s`
---
### 版本3：
  
  实现如下参数：-u url -d deep -k keyword -l loglevel -f logfile -s -t threadnumber,url默认入口是https://baike.baidu.com/。 -d 默认为 1；-f为日志名称，默认为BaiKeSpider；-l为日志等级，默认为1；-s是判断是否进行自测，即doctest，添加该参数则进行，不添加不影响程序运行,但是添加后只进行自测！-t为线程池中维护线程的个数，默认为5
  
  测试可用命令：`python BaiKeSpider.py -d 2 -t 3 -k uestc -l 4 -f mylogfile` 或者`python BaiKeSpider.py -s`
---
### 版本4：
  
  因为存储的数据库是mongodb，title一样的情况下，索引不一样，因此直接可以把多义词的信息存储在一个对应的词条中，故多义词的存储已经完成。同时修复了一些bug。
  目前除了每十秒打印进度信息未完成之外其他功能都已经完成。
