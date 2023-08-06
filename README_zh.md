# Django Authorization

[English](README.md) | 中文



Django-authorization是一个适用于于Django框架的授权库。

[![tests](https://github.com/pycasbin/django-authorization/actions/workflows/release.yml/badge.svg)](https://github.com/pycasbin/django-authorization/actions/workflows/release.yml) [![Coverage Status](https://coveralls.io/repos/github/pycasbin/django-authorization/badge.svg)](https://coveralls.io/github/pycasbin/django-authorization) [![Version](https://img.shields.io/pypi/v/django-authorization.svg)](https://pypi.org/project/django-authorization/) [![Download](https://img.shields.io/pypi/dm/django-authorization.svg)](https://pypi.org/project/django-authorization/) [![Discord](https://img.shields.io/discord/1022748306096537660?logo=discord&label=discord&color=5865F2)](https://discord.gg/S5UjpzGZjN)

Django-authorization基于[Casbin](https://github.com/casbin/pycasbin)和[Django-casbin](https://github.com/pycasbin/django-casbin)制作，支持ACL、RBAC、ABAC等多种访问模式。

![image](https://user-images.githubusercontent.com/75596353/188881538-a6a99cb1-c88b-4738-bf4f-452be4fb7c2d.png)

- [Django Authorization](#django-authorization)
  
  * [安装和配置](#安装和配置)
  
  * [使用方法](#使用方法)
    
    + [一些基本概念](#一些基本概念)
    + [使用鉴权中间件](#使用鉴权中间件)
    + [使用鉴权装饰器](#使用鉴权装饰器)
    + [使用命令行修改权限模型](#使用命令行修改权限模型)
    
  * [许可证](#许可证)
  
    

## 安装和配置

```
pip install django-authorization
```

我们建议首先配置用于能够将鉴权策略持久化存储到数据库的适配器，比如说[django-orm-adapter](https://github.com/pycasbin/django-orm-adapter)

将adapter集成到项目中后继续配置django-authrization

```python
# 1. Add the app to INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dauthz.apps.DauthzConfig",	# add this app to INSTALLED_APPS
]

# 2. Add configure of dauthz
DAUTHZ = {
    # DEFAULT Dauthz enforcer
    "DEFAULT": {
        # Casbin model setting.
        "MODEL": {
            # Available Settings: "file", "text"
            "CONFIG_TYPE": "file",
            "CONFIG_FILE_PATH": Path(__file__).parent.joinpath("dauthz-model.conf"),
            "CONFIG_TEXT": "",
        },
        # Casbin adapter .
        "ADAPTER": {
            "NAME": "casbin_adapter.adapter.Adapter",
            # 'OPTION_1': '',
        },
        "LOG": {
            # Changes whether Dauthz will log messages to the Logger.
            "ENABLED": False,
        },
    },
}
```

为了更好地介绍django-authorization的配置方法，我们搭建了一个基于django-authorization的django应用，您可以在这里[django-authorization-example](https://github.com/pycasbin/django-authorization-example)查看

## 使用方法

### 一些基本概念

django-authorization基于casbin开发，相关术语（例如enforcer, adapter等）可以到[casbin website](https://casbin.org/)官网查阅文档

### 使用鉴权中间件

```python
# Install middleware for django-authorization as required
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dauthz.middlewares.request_middleware.RequestMiddleware",	# add the middleware 
]
```

可以通过API自由设置中间件的enforcer：set_enforcer_for_request_middleware(enforcer_name)和set_enforcer_enforcer_middleware(enforcer_name)。

### 使用鉴权装饰器

请求装饰器将检查用户、路径、方法的授权状态，例如：

```python
# use request decorator
@request_decorator
def some_view(request):
    return HttpResponse("Hello World")
```

Enforcer装饰器将检查用户、对象、编辑的授权状态， 例如：

```python
# use enforcer decorator
# sub: user in request obj: "artical" act: "edit"
@enforcer_decorator("artical", "edit")
def some_view(request):
    return HttpResponse("Hello World")
```

### 使用命令行修改权限模型

命令行操作允许你直接对执行者的数据库进行操作。有三组命令可用：策略命令、组命令和角色命令。

```shell
Add/Get policy, usage: 
python manage.py policy [opt: --enforcer=<enforcer_name>] add <sub> <obj> <act>
python manage.py policy [opt: --enforcer=<enforcer_name>] get <sub> <obj> <act>

Add/Get role to user, usage: 
python manage.py role [opt: --enforcer=<enforcer_name>] add <user> <role>
python manage.py role [opt: --enforcer=<enforcer_name>] get <user>

Add/Get group policy, usage:
python manage.py group [opt: --enforcer=<enforcer_name>] add <user> <role> [opt:<domain>]
python manage.py group [opt: --enforcer=<enforcer_name>] get <user> <role> [opt:<domain>]
```

## 许可证

本项目的许可证遵循：[Apache 2.0 license](https://github.com/php-casbin/laravel-authz/blob/master/LICENSE).
