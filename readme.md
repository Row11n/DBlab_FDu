## 此项目用于2022春季学期FDu数据库期中实验
#### 所用django版本为4.0.4，python版本为3.8.10
##### 代码目录说明

database_midlab

│── media/avatar：用于存储用户头像图片

│

│── Sales_system：主应用程序目录，这里用来调控整个项目

│　　├── **__pycache__**：缓存文件夹，不用在意

│　　├── **__init__**.py：初始化文件，不用在意

│　　├── asgi.py：控制网关接口，与实验无关

│　　├── settings.py：这是整个项目的设置文件，比较重要

│　　├── urls.py：url接口文件，这里控制所有url访问

│　　├── wsgi.py：控制网关接口，与实验无关

│　　　　　

│── ss_env：这个文件夹用于创建虚拟环境，方便部署到服务器上，与实验无关

│　　　　

│── static：静态文件文件夹，用于存储所有静态文件

│　　├── css：css文件目录

│　　├── images：图片目录

│　　　　　

│── system：系统应用程序目录，这里实现了所有系统相关页面及其功能

│　　├── **__pycache__**：缓存文件夹，不用在意

│　　├── migrations：迁移数据文件夹，用于将建好的模型迁移至数据库，使数据库创建相应table

│　　├── templates/system：页面目录，所有系统相关html文件都在这里

│　　　　　├── about.html：网站介绍页面

│　　　　　├── base.html：导航栏

│　　　　　├── books_display.html：书库页面

│　　　　　├── bookshop.html：书城页面

│　　　　　├── finance.html：财务页面

│　　　　　├── home.html：主页

│　　　　　├── info_detail：书籍详情页面

│　　　　　├── new_book_for_stock.html：进货时新建图书页面

│　　　　　├── new_book.html：新建图书页面

│　　　　　├── stock.html：进货页面

│　　　　　└── stockbills.html：货单页面

│　　├── **__init__**.py：初始化文件，不用在意

│　　├── admin.py：管理网站注册页面，在这里注册管理网站的模型，与实验无关

│　　├── apps.py：应用程序文件，本项目没有用到

│　　├── forms.py：表单文件，这里创建了需要使用到的表单模型

│　　├── models.py：模型文件，这里定义了数据库模型，在迁移后数据库会根据模型建表

│　　├── tests.py：测试文件，本项目没有用到

│　　└── views.py：视图文件，这里编写了所有页面对应的后端视图，后端代码的处理都在这个地方

│　　　　　

│── Userinfo：用户应用程序目录，这里实现了所有用户相关页面及其功能

│　　├── **__pycache__**：缓存文件夹，不用在意

│　　├── migrations：迁移数据文件夹，用于将建好的模型迁移至数据库，使数据库创建相应table

│　　├── templates：页面目录，所有用户相关html文件都在这里

│　　　　　├── registration

│　　　　　   ├── logged_out.html：登出页面

│　　　　　├── Userinfo

│　　　　　   ├── login.html：登录页面

│　　　　　   ├── register_for_staff：创建管理员页面

│　　　　　   ├── register.html：一般用户注册页面

│　　　　　   └── userinfo.html：用户信息管理页面

│　　├── **__init__**.py：初始化文件，不用在意

│　　├── admin.py：管理网站注册页面，在这里注册管理网站的模型，与实验无关

│　　├── apps.py：应用程序文件，本项目没有用到

│　　├── forms.py：表单文件，这里创建了需要使用到的表单模型

│　　├── models.py：模型文件，这里定义了数据库模型，在迁移后数据库会根据模型建表

│　　├── tests.py：测试文件，本项目没有用到

│　　└── views.py：视图文件，这里编写了所有页面对应的后端视图，后端代码的处理都在这个地方

│　　　　　

│── .gitignore：略

│── manage.py：主管理文件，项目运行的接口

│── Procfile：web进程文件，用于服务器部署，与实验无关

│── readme.md: 此文件

│── requirements.txt: 此项目需要安装的包

│── runtime.txt: python版本，用于服务器部署，与实验无关