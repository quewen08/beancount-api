# Beancount REST api 服务
`基于Python3.12和Flask Flask-RESTX创建的beancount的REST-api服务`

## 目录结构

```
beancount-api/
├── bapp/                            # 应用程序目录
│   ├── __init__.py                  # 初始化文件
│   ├── api/                         # API 模块目录
│   │   ├── __init__.py              # 初始化文件
│   │   ├── core.py                  # 核心 API 模块
│   │   ├── price.py                 # 多货币汇率 API 模块
│   │   ├── transaction.py           # 交易 API 模块
│   │   └── query.py                 # 查询 API 模块
│   ├── core/                        # 核心模块目录
│   │   ├── __init__.py              # 初始化文件
│   │   ├── exception.py             # 异常处理模块
│   │   └── storage.py               # 缓存模块
│   ├── app.py                       # 应用程序入口文件
├── Dockerfile                       # Dockerfile 文件（如果需要容器化部署）
├── .env                             # 环境变量文件（可选）
├── README.md                        # 项目的说明文件
└── data/                            # 存放 Beancount 数据文件的目录
    └── example.beancount            # 示例的 Beancount 数据文件
```

## 开发

1. 克隆项目到本地：
```shell
git clone 
```
---

2. 初始化环境，安装依赖：

> 本项目基于`python3.12`开发，建议使用`python3.12+`环境

```shell
cd beancount-api
python -m venv .venv

source .venv/bin/activate # 激活虚拟环境 for Linux/Mac OSX
.venv\Scripts\activate # 激活虚拟环境 for Windows

pip install -r requirements.txt
```

3. 启动服务：
```shell
python -m bapp.app -h localhost -p 5000 data example.beancount
```

4. 访问 API：http://localhost:5000
5. 贡献代码：
6. 提交 PR：