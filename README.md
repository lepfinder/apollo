## 书香馆

### 介绍
书香馆是一个基于flask开发的P2P图书分享应用。效果图：
![](http://7xo9p3.com1.z0.glb.clouddn.com/markdown/1451891670154.png?imageMogr2/thumbnail/!50p/quality/100!)


### 运行

```
git clone git@github.com:lepfinder/apollo.git
cd apollo
virtualenv venv
. venv/bin/activate

pip install -r requirements.txt

修改apollo/config.cfg文件，配置数据库url

python manager.py runserver
```


### 设计思路


### TODO

- 图书标签
- 日志体系
- 异常处理
- 接入第三方登录
- 优化分享流程
- 添加社交属性


