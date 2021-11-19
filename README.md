# Lit-Report
洛阳理工学院健康管控平台自动上报。  

封装了健康管控平台的常用[方法](##平台方法)。你可以将代码部署在**服务器**并使用crontab等任何你喜欢的方式设置定时任务。  

又或许你**没有可用的服务器**，那么我也很乐意帮助你完成这项任务，你要做的只是调用下面的[接口](##接口)。  



## 接口  
暂未开放



## 平台方法  


> **注意**，以下所有的方法都可以单独调用，即你不需要为了调用`firstReport`方法而特意在此之前调用`login`方法。`firstReport`方法在调用时会自动检测登录状态。


- 登录
```python
UserAPI(User).login()
```



- 获取最近一次上报的信息
```python
UserAPI(User).getLast()
```



- 第一次上报
```python
UserAPI(User).firstReport()
```



- 第二次上报
```python
UserAPI(User).secondReport()
```



- 第三次上报
```python
UserAPI(User).thirdReport()
```
