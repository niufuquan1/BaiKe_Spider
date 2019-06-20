# BaiKe_Spider
#### 版本1：Spider1.py -u url -d deep -k keyword
#### 版本2：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  -s
#### 版本3：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  -s -t number
#### 版本4：剩下所有功能

---
### 版本1：
  
- 实现如下参数：-u url -d deep -k keyword 
- 默认不传递url，url默认入口是https://baike.baidu.com/
- -d 默认为 1
- 测试可用命令：`python Scheduler.py -k uestc `
---
### 版本2： 

- 实现如下参数：-u url -d deep -k keyword -l loglevel -f logfile -s
- -u为起始的url，建议不写，默认入口是https://baike.baidu.com/
- -d为爬取深度，默认为 1
- -f为日志名称，默认为BaiKeSpider
- -l为日志等级，默认为5；
- -s是判断是否进行自测，即doctest，添加该参数则进行，不添加不影响程序运行
- 测试可用命令：`python Scheduler.py -k uestc -d 2 -l 3 -f myLog -s`
---
### 版本3：
  
- 实现如下参数：-u url -d deep -k keyword -l loglevel -f logfile -s -t threadnumber
- url默认入口是https://baike.baidu.com/ 
- -d 默认为 1
- -f为日志名称，默认为BaiKeSpider
- -l为日志等级，默认为1；-s是判断是否进行自测，即doctest，添加该参数则进行，不添加不影响程序运行,但是添加后只进行自测！
- -t为线程池中维护线程的个数，默认为5
- 测试可用命令：`python BaiKeSpider.py -d 2 -t 3 -k uestc -l 4 -f mylogfile` 或者`python BaiKeSpider.py -s`
---
### 版本4：
- 实现如下参数：-u url -d deep -k keyword -l loglevel -f logfile -s -t threadnumber
- 因为存储的数据库是mongodb，在title一样的情况下，索引不一样，因此直接可以把多义词的信息存储在一个对应的词条中，故多义词的存储已经完成
- 同时修复了一些bug
- 目前除了每十秒打印进度信息未完成之外其他功能都已经完成

### 演示视频
- 首先演示了doctest
- 然后演示了版本4的正常爬取，特别选择了python，python存在多义，因此在mongoDB中可以发现一个python词条中的多义的内容
###演示下载地址
- 链接：`https://pan.baidu.com/s/1k23lCPbgi35wBpqZ0DtHPg`
- 提取码：4v8e 

## 感触 ##
> 这个题是周一给我的，我抽自己的空闲时间在做，以前没有做过这样的一个完整的爬虫的项目，因此对自己的要求高了很多，但是也逼着我自己学习了更多的知识。通过这个题，我已经了解了一个完整的爬虫架构，自己写自己的框架基本上是有思路的，只是实现的路径的问题。刚开始的起步是很慢的，首先自己做的是单线程的爬虫。在实现了url管理器、下载器、db(pipline)、parse、调度器之后，一个基本上齐全的爬虫已经构造好了。然后通过学习argparse，学会了用命令行传参。学习doctest，学会了一个简单的单元自测框架。之后又写了相关的日志模块logging。最让我头疼的是实现多线程池的部分，我发现自己之前实现的有些东西逻辑不太符合线程要求，因此自己又推倒重写，从重写的过程中，自己越来越明白了其中的逻辑关系，在写出更好的爬虫架构之后，自己当然是很激动的。目前，对实现每十秒钟报一次进度是有一些思路的（基于自己的理解，不知道标准的答案是什么-。-），但是一直存在一些问题，感觉自己的思路肯定是有某些漏洞的，但是鉴于6月17日周一 上午10:20 (3天前)我收到的题，我觉得应该先提交自己的答案，及时给HR以及技术大牛汇报自己的进度还是很重要的--（毕竟涉及自己的offer。。。），之后自己再去想想。
