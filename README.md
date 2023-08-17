# Django Authorization

English | [中文](README_zh.md)



Django-authorization is an authorization library for Django framework.

[![tests](https://github.com/pycasbin/django-authorization/actions/workflows/release.yml/badge.svg)](https://github.com/pycasbin/django-authorization/actions/workflows/release.yml)
[![Coverage Status](https://coveralls.io/repos/github/pycasbin/django-authorization/badge.svg?branch=master)](https://coveralls.io/github/pycasbin/django-authorization?branch=master)
[![Version](https://img.shields.io/pypi/v/django-authorization.svg)](https://pypi.org/project/django-authorization/)
[![Download](https://img.shields.io/pypi/dm/django-authorization.svg)](https://pypi.org/project/django-authorization/)
[![Discord](https://img.shields.io/discord/1022748306096537660?logo=discord&label=discord&color=5865F2)](https://discord.gg/S5UjpzGZjN)

Based on [Casbin](https://github.com/casbin/pycasbin) and [Django-casbin ](https://github.com/pycasbin/django-casbin) (middleware, light weight of this plugin), an authorization library that that supports access control models like ACL, RBAC, ABAC.

![image](https://user-images.githubusercontent.com/75596353/188881538-a6a99cb1-c88b-4738-bf4f-452be4fb7c2d.png)


- [Django Authorization](#django-authorization)
  * [Installation and Configure](#installation-and-configure)
  * [Usage](#usage)
    + [Some Important Concepts:](#some-important-concepts-)
    + [Middleware Usage](#middleware-usage)
    + [Decorator Usage](#decorator-usage)
    + [Command Line Usage](#command-line-usage)
  * [License](#license)



## Installation and Configure

```
pip install django-authorization
```

We recommend that you first configure the adapter for persistent storage of the policy, such as: 

[django-orm-adapter](https://github.com/pycasbin/django-orm-adapter), After integrating it into the project continue with the configuration of django-authrization

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

to better prompt the configure method of django-authorization, we made a django-app based on django-authorization, you can see it in [django-authorization-example](https://github.com/pycasbin/django-authorization-example)

## Usage

### Some Important Concepts:

such as .conf file, policy, sub, obj, act, please refer to the [casbin website](https://casbin.org/)

### Middleware Usage

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

You can freely set the casbin enforcer for the middleware via API: set_enforcer_for_request_middleware(enforcer_name) and set_enforcer_for_enforcer_middleware(enforcer_name)

### Decorator Usage

Request decorator will check the authorization status of user, path, method

```python
# use request decorator
@request_decorator
def some_view(request):
    return HttpResponse("Hello World")
```

Enforcer decorator will check the authorization status of user, obj, edit. example: 

```python
# use enforcer decorator
# sub: user in request obj: "artical" act: "edit"
@enforcer_decorator("artical", "edit")
def some_view(request):
    return HttpResponse("Hello World")
```

### Command Line Usage

The command line operation allows you to operate directly on the enforcer's database. Three sets of commands are available: policy commands, group commands and role commands.

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

### Backend Usage

You can integrate Pycasbin with [Django authentication system](https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization). For more usage, you can refer to `tests/test_backend.py`. To enable the backend, you need to specify it in `settings.py`.

```python
AUTHENTICATION_BACKENDS = [
    "dauthz.backends.CasbinBackend",
    "django.contrib.auth.backends.ModelBackend", 
    ]
```

Note that you still need to add permissions for users with pycasbin `add_policy()` due to the mechanism of the django permission system.

## License

This project is licensed under the [Apache 2.0 license](https://github.com/php-casbin/laravel-authz/blob/master/LICENSE).
