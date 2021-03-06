Slug: django-learning-notes
Tags: django
Date: 20190405

[TOC]


## Beginning

一开始先介绍下Djanog项目的基本文件夹结构，还有一些基本的命令操作和一些基本的常识性东西。

首先是新建一个项目：

### 新建项目
```
django-admin startproject project-name
```

这个命令将创建一个文件夹，文件夹的名字就是这里设置的project-name，然后文件夹里面有一个manage.py文件，这个文件的主要作用就是挂载django的配置（一般是settings.py这个文件，当然你也可以修改为其他比如dev_settings.py文件）。

然后还有一个文件夹，里面有settings.py 、 urls.py 和 wsgi.py 文件。

settings.py 控制django的全部配置管理；

urls.py 控制django的路径分发主入口，这个在配置中可以修改的。

wsgi.py 是你用apache或者uwsgi挂载的时候的控制入口。


这样最简单的初始项目就是可以运行的了：


### 开启服务器

```
python manage.py runserver localhost:8080
```

后面控制服务器监听的localhost或者外网0.0.0.0，然后就是端口号。



### 新建一个app

```
python manage.py startapp app_name
```

这里顺便说一下，有一些项目你可能找不到 manager.py 这个文件了，其实这个文件就是一个便捷入口罢了，所有的命令一样都可以通过 django-admin 命令来运行的。



### 数据库操作

定义模型之后，你需要运行:

```
python manage.py makemigrations app_name
```

这个过程就是创建每个app下的migrations文件夹下面的一些迁移python脚本文件，有的时候某些情况你可能需要手工修改这些迁移文件。

```
python manage.py migrate
```
这个命令就是实际执行那些迁移python脚本。




### 交互式环境

进入python交互环境，这个和纯python交互环境的区别就是里面可以直接使用django里面的一些东西了，比如你定义的模型对象就可以直接使用了。这个对你开发进行测试工作非常有用！

```
python manage.py shell
```


或者进入sql实现的交互环境:

```
python manage.py dbshell
```



### 创建超级用户
最开始创建的项目就把admin url挂上去了，你可以去 \verb+/admin+ 这个url下看一下，但要登录除了做一下上面的数据库表格创建工作外，还需要创建一个超级用户用于登录。

```
python manage.py createsuperuser
```




## apps.py

通过快捷命令创建的app模块是没有这个文件的，但是我看到某些例子里面其有这个文件，后来了解到这个文件是有特殊含义的：这是django项目用来存放app 一些相关配置信息的地方。

一个基本的例子如下：

```python
from django.apps import AppConfig

class RockNRollConfig(AppConfig):
    name = 'rock_n_roll'
    verbose_name = "Rock ’n’ roll"
```



其中name定义了本app的名字和完整名字，然后你需要在本app的 `__init__.py` 文件下加入：

```
default_app_config = 'rock_n_roll.apps.RockNRollConfig'
```

来引入这个配置文件。

有什么用？well，最简单的用处就是本app实际在 `INSTALLED_APPS ` 哪里不是默认的文件夹名字了，而是你这里定义的名字。

另外一个高级用法就是定制 `ready` 方法，来初始化本app的一些信号设置。	



## url分发

web框架的一个核心功能就是完成url分发工作，我们先来看下django的这块内容。

基本过程是在你的 project 的 `urls.py` 那里定义好整个项目的url分发规则。默认的内容如下:

```python
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

读者有兴趣可以先看下那个admin页，在 `/admin` 那边。请确认已经执行前面的数据库操作 `makemigrations` 和 `migrate` 了，然后已经创建超级用户了 `createsuperuser` 。这样你就可以看到django默认自动创建的admin支持页面了。

然后接下来就是类似这样的在这里插入你自己的 app的 各个 urls定义。一般如下简单写上即可:

```python
from django.urls import include, path
    ....
    path('app_name/', include('app_name.urls')),
    ....
```

在确定没有特殊url分发需求的情况下，都推荐如上使用django官方教程推荐的这种url分发写法。

在某个app下的 `urls.py` 将进一步定义url分发规则:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```



上面的讨论是根据django的官方教程来的，应该是推荐的写法风格。



### url上带参数

```python
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^add/([\d]+)/([\d]+)$', views.add, name='add'),
]
```

这里参数将逐个传递个视图函数，唯一值得一提的是django的视图函数默认第一个函数是传递进去的 `request` 参量。在 `views.py` 里面的内容如下:

```python
from django.http import HttpResponse

def add(request, a, b):
    res = int(a) + int(b)
    return HttpResponse(str(res))
```

上面这种正则表达式的写法是老式的django的url写法，一般没有特别的需求的话，应该按照django官方教程，采用下面的推荐写法：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('add/<int:a>/<int:b>', views.add, name='add'),
]
```





### url定义name

`name` 这个参量大体类似于flask的 `endpoint` 的概念，然后django还有的 `reverse` 函数，其大体类似于flask的 `url_for` 的概念。

比如上面视图函数的 add 对应的url我们可以如下获得:

```
from django.core.urlresolvers import reverse
reverse('add',args=(1,2))
```

然后在模板中有:

```
<a href="{% url 'add' 1 2 %}">link</a>
```

### 获取full-url

上面提到的reverse函数返回的url字符串还不是完整的url，而只是相对url。如果我们要获取全站的完整url则可以使用 `request.build_absolute_uri(location)` ，如果不指定location则默认是当前的url。



## 请求和响应

### request

是的，我们的APIView的一些特殊含义的方法，都会接收一个 request对象，这个对象有：

- query_params 获得GET传过来的参数
- data 获得POST PUT PATCH 传过来的参数，这还没完，传过来的文件，表单都支持。
- user 如果请求经过认证了会返回相应的用户记录，你编写auth类的时候会知道的，如果没有认证，那么返回 `AnonymousUser`



### Response

也就是一些特殊含义的方法的返回对象，其第一个参数是data，字典值，会自动封装成为json友好的格式。实际上我们经常看到的就是这个套路：

```
return Response(serializer.data)
```

然后 serializer 有个 `is_valid` 方法，用来序列化类输出前的预热。这两点在后面序列化的讨论中会涉及。其他一些我们看一下吧：

```
Response(data, status=None, template_name=None, headers=None, content_type=None)
```

headers http协议响应头，status http状态码等等。

整个过程套路，很多高级视图的套路都类似于下面这个例子，多看几遍吧。

```python
class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

urls.py那边加上的是:

```
url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
```

这里正则表达式 `(?P<pk>[0-9]+)` 的意思是收集某一串数字，这一串数字被命名为 `pk` 。





## 模型的定义和使用

django的模板和sqlalchemy还是有很多地方类似的。

### settings那边的配置

- **INSTALLED\_APPS:** 你需要加上你新加入的 app 的名字，不加的话是不能通过 `makemigrations` 来管理数据库的。
- **DATABASES:** 默认会创建一个sqlite3数据库，也能满足基本的需求了，如果你想要使用mysql等数据库，则参考样例修改这里的配置。比如连接mysql的样例是:

```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': "database_name",
            'USER': "root",
            'PASSWORD': "",
            'HOST': "localhost", 
            'PORT': "3306",
            'OPTIONS': {
                'charset': 'utf8'
            }
        }
    }
```

一般会加上 charset 是 utf8这个选项，当然mysql那边你也需要设置好字符编码。有的时候如下设置init_command 来设置字符编码可以让你获得更好的字符编码兼容性。

```
    'OPTIONS': {
        'init_command': 'SET character_set_database=utf8 ,\
        character_set_server=utf8,\
        character_set_connection=utf8,\
        collation_connection=utf8_unicode_ci',
        'charset': 'utf8'}
```

### 使用多个数据库

有的时候你需要使用多个数据库，最常见的情况是某个单独的app使用另外一个数据库。

首先你需要再加上另外一个数据库的定义：

```
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "database_name",
        'USER': "root",
        'PASSWORD': "",
        'HOST': "localhost",
        'PORT': "3306",
        'OPTIONS': {
            'charset': 'utf8'
            }
        },
        'youapp': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'youapp',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {'charset': 'utf8'}
        },
    }
```

然后在你的app那边新建一个dbrouter文件，里面定义一个YourRouter类。

```
DATABASE_ROUTERS = ['youapp.dbrouter.YourRouter']
```

在这个类里面如下定义一些数据库选择行为：

**NOTICE: 在这个app中定义的模型记得都要加上app_label这个meta属性。**

```
class YourRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'youapp':
            return 'youapp'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'youapp':
            return 'youapp'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'youapp' or \
            obj2._meta.app_label == 'youapp':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'youapp':
            return db == 'youapp'
        return None
```



## 定义模型

好了，开始实际定义自己的模型了。首先基本语法如下:

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
```

这个熟悉sqlalchemy的对这段代码不会很陌生，下面进一步了解一些细节吧。

### 字段类型

- **IntegerField:** 整型
- **BigIntegerField:** 大整数
- **BinaryField:** raw data
- **BooleanField:** bool 值
- **CharField:** 定义字符串类型，比如设置最大长度 `max_length` 这个属性。
- **TextField:** 大段文字用这个。
- **DateField:** 对应python中的 `datetime.date` 对象。
- **DateTimeField:** 对应python中的 `datetime.datetime` 对象。

一个有用的基类:

```python
class BaseModel(models.Model):
    class Meta:
        abstract = True

    updated_at= models.DateTimeField(auto_now=True)
    created_at= models.DateTimeField(auto_now_add=True)
```

后面的模型都可以继承自该基类，基类是不会创建表格的，因为其Meta设置了 `abstract=True` 。DateTimeField加上 `auto_now=True` ，那么该模型每次 `save` 操作都会自动更新最新日期。 然后 `auto_now_add=True` 即该记录第一次创建时设置最新的日期。然后如果DateTimeField使用了 auto_now 或者 auto_now_add 这两个选项了就不要使用default选项了，还有就是自动插入的默认的时间是由 `django.utils.timezone.now()` 获得的。

比如后面你想获得六个小时之前的所有记录那么可以如下查询：

```
    checktime = timezone.now() - timedelta(hours=6)
    result = result.exclude(created_at__gt= checktime)
```

### 通用选项

字段声明控制中有一些通用可选项:

- **default:** 设置该字段的默认值，注意default还可以接受一个函数对象。
- **null:** 设置为True，则该自动会自动填充sql中的NULL值，字符串类型字段最好默认空字符。
- **blank:** 如果设置为True，则空值也是允许的，其和null的区别是null是说数据库那边的，而blank是说显示那边的。
- **db\_column:** 设置该字段具体在数据库中对应的表格的名字。
- **db\_index:** 设置为 `True` 则表示该字段开启索引。
- **primary\_key:** 主键 。
- **unique:** 唯一
- **unique\_for\_date:** 比如title字段设置:

```
    unique_for_date="pub_date"

```

则 title字段和 pub\_date 字段都不能相同。也就是在某个日期内某个title只能有唯一值。可以看作一种 `unique_together` 的应用。

### 数据库中的关系

**ForeignKey:** 外键引用，如果该字段的名字是user，那么实际存储在表格中的名字是user\_id，你可以通过 `db_column` 来实际控制该表格的名字。- 

我们通常说的onetomany关系就是通过定义ForeignKey来获得的。比如：

```
class City(models.Model):
     name = models.CharField(max_length=60)
     state = models.CharField(max_length=40)
     zipcode = models.IntegerField()

class Address(models.Model):
     number = models.IntegerField()
     street = models.CharField(max_length=100)
     city = models.ForeignKey(City)

```

一个city有多个address，但是一个address只能有一个city，也就是一个外键映射到city那边。所以我觉得ForeignKey更确切的表示是manytoone关系，当某个模型有一个外键属性是，也就是可以有多个记录指向同一个它物 [参阅了这篇文章](https://chrisbartos.com/articles/how-to-implement-one-to-many-relationship-in-django/)。

**OneToOneField**
OneToOneField 比较简单，就是一个记录只有一个对应的属性，通常在用户管理的时候会用到。

**ManyToManyField**

ManyToManyField 读者请参阅我写的 [sqlalchemy模块](http://www.cdwanze.work/articles/python/sqlalchemy-module.html#orm_2) 一文， 那里写得比较详细。



关于模型定义的字段，更多的内容请参看官方文档。



### 多字段组合唯一

参考了 [这个网页](https://stackoverflow.com/questions/28712848/composite-primary-key-in-django) ，具体就是在 `Meta`  那里定义 `unique_together` 属性。

```
    ...
    title = models.CharField(max_length=255)
    gzh_id = models.CharField(max_length=255, null=True, blank=True)
    ...
   class Meta:
        db_table = 'article'
        unique_together = ("title","gzh_id")

```



## 定义模型中的元类数据

```
    ...
    class Meta:
        db_table = 'table_name'

```

- db_table 具体指定实际创建的table表格的名字。
- abstract 将不会创建表格，该模型为抽象模型。
- 

## 模型的使用

模型的使用最核心的部分就是查询操作，至于修改记录，则具体查询获得目标记录了，修改属性然后save即可。

### 新建记录

```
from people.models import Person
Person.objects.create(name="WeizhongTu", age=24)

```

但是要注意如果你插入一条记录出现主键重复问题了，那么程序是会返回异常的。一般推荐使用 `get_or_create` 方法：

```
obj, created = Person.objects.get_or_create(first_name='John', last_name='Lennon',
                  defaults={'birthday': date(1940, 10, 9)})

```

上面这个语句有查询的效果也有新建记录的效果。写的这些属性首先将进行get操作，大体是如下的加强版：

```
try:
    obj = Person.objects.get(first_name='John', last_name='Lennon')
except Person.DoesNotExist:
    obj = Person(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
    obj.save()

```

而如果单纯使用get方法，如果记录不存在那么会抛出 **DoesNotExist** 异常；如果找到多个记录，会抛出 **MultipleObjectsReturned ** 异常。 get_or_created 方法如果找到多个记录也会抛出  **MultipleObjectsReturned ** 异常。

这样 `get_or_created ` 方法将确保总是插入一条记录或者取得记录。其中created=True则表明target是新建的记录。

然后是如何理解 defaults 这样选项，defaults里面定义的属性不会参与get查询过程，其参与的是在没有找到记录的情况下，设置某些值。

### 查询记录

首先说一下获取所有的记录：

```
result = Person.objects.all()

```

其返回的是 QuerySet 对象，QuerySet对象可以继续进行下一步的查询操作。比如下面可以继续：

```
result = result.filter(name="abc")

```

当然就上面的例子来说直接使用filter方法即可：

```
result = Person.objects.filter(name="abc")

```



### 排序

QuerySet对象可以进一步排序：

```
result = result.order_by('what')

```

### reverse

```
result = result.reverse()

```

### exclude

排除某些记录，下面是排除created_at这个字段值大于某个时间的值：

```
result = result.exclude(created_at__gt= checktime)

```

### offset and limit

```
result = result[offset: offset+limit]

```



### 删除某个记录

找到目标记录的instance，然后调用 `delete` 方法即可。

### 确定某记录是否存在

前面已经谈到了一些查询操作，而如果读者只是单纯的想确定某记录是否存在，那么使用 `exists` 方法是最快和最简便的。参考了 [这个网页](https://stackoverflow.com/questions/2690521/django-check-for-any-exists-for-a-query) 。



```
if Article.objects.filter(unique_id= unique_id).exists():
    ...

```

### 关系的使用

OnetoOne关系的使用非常简单， `a.b` 或者 `b.a` 都是可以的。

ManytoOne关系也就是由 ForeignKey 定义的关系，如果是引用外键的那个对象，那么直接 `a.b` 即可，如果是反向onetomany那种，则最好你在定义的时候就定义好 `related_name` ，（参考了 [这个问题](https://stackoverflow.com/questions/19799955/django-get-the-set-of-objects-from-many-to-one-relationship) ）那么引用如下：

```
b.related_name

```

具体使用细节还是请查看文档的 [这里](https://docs.djangoproject.com/zh-hans/2.0/topics/db/examples/many_to_one/) 。





## 序列化

### 理解序列化过程

django restframework的序列化类类似于django的表单类，不同的是django的表单类是用于沟通django的Model和网页form之间的桥梁；而序列化类是用于沟通django的Model类和JSON数据格式之间的桥梁。

```
注: Model -> Serializer （其data挂载的是python的dict字典值了）

serializer = SnippetSerializer(snippet)
serializer.data
# {'pk': 2, 'title': u'', 'code': u'print "hello, world"\n', 'linenos': False, 'language': u'python', 'style': u'friendly'}
```

上面这个过程通常是在视图类特殊方法下，进行一些数据库操作之后获取数据库的目标Model的记录，然后送入序列化类，然后目标类的 `.data` 属性就是字典值了，送入Response哪里就可以作为HTTP响应的结果值了。



然后还有下面这种用法，将某个字典data送入序列化类的data属性中，

```
serializer = SnippetSerializer(data=data)
```

调用序列化类的save方法来进一步完成相应的数据库操作。

```
serializer.save()
```

这个save方法具体行为依赖于你进一步定义序列化类里面的 `create` 和 `update` 方法。如下所示：

```
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance
```

某些情况下你可能想直接定义save方法。



### ModelSerializer

类似于django的表单类，可以利用 `ModelSerializer` 类来更快地创建序列化类。

```python
from rest_framework import serializers

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
```

为了证明这种简便写法对于上面的任务（包括create和update方法都会自动实现的）是完全应付得过来的。上面在shell里的代码再撸一遍。

```
>>> from snippets.models import Snippet
>>> snippet = Snippet(code='print "hello, world2"\n')
>>> from snippets.serializers import SnippetSerializer
>>> snippet.save()
>>> serializer = SnippetSerializer(snippet)
>>> serializer.data
{'language': 'python', 'linenos': False, 'id': 3, 'title': '', 'code': 'print "hello, world2"\n', 'style': 'friendly'}
```



### is_valid 方法

```
serializer.is_valid(raise_exception=True)
```

你可以定义 `validate` 方法来进行目标对象的验证行为，或者定义 `validate_<fieldname>` 来定义字段级别的验证行为。

```python
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```



### 在序列化类里面引用request.user

参考了 [这个问题](https://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer) ，在序列化类里面需要通过 `self.context['request']` 来获取 request 对象，进而获取 user对象。

```
user =  self.context['request'].user

```



## 模板基本概念

模板基本的样子如下，下面有模板继承，block ，循环，过滤，之类的。熟悉jinja2模板的同学稍微看下大致是个什么意思就已经清楚了。

```django
{% extends "base_generic.html" %}
{% block title %}{{ section.title }}{% endblock %}
{% block content %}
<h1>{{ section.title }}</h1>
{% for story in story_list %}
<h2>
  <a href="{{ story.get_absolute_url }}">
    {{ story.headline|upper }}
  </a>
</h2>
<p>{{ story.tease|truncatewords:"100" }}</p>
{% endfor %}
{% endblock %}

```

### django如何查找模板的

在django的settings.py哪里有：

```
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES=[
{
'BACKEND':'django.template.backends.django.DjangoTemplates',
'DIRS':[
os.path.join(PROJECT_DIR,'templates'),
],
```

默认是在每个app下的templates文件里都会递归遍历查找的，这里DIRS加上了另外一个文件夹，也就是现在settings.py所在的那个文件夹下如果有templates文件夹也会去遍历的。



模板文件最后都会合并的，所以就存在模板的覆盖机制了，为了避免无谓的覆盖，一般模板原则上推荐的结构是在templates下面，不管是那个app下面，都再新建一个目标app的名字，再新建模板文件。当然对于稍小的项目直接扔在templates下面问题不大。



比如你想覆盖django自带的admin界面，就要在templates下面新建一个admin文件夹，具体什么模板文件，你要研究下django的源码了。







### django的变量怎么传给javascript

**NOTICE: 现在不推荐这种写法了，推荐走ajax通道传数据。**



django的视图函数在render的时候通过context字典值，里面的各个字段的值将传给django的模板里的变量，这个我们是知道的了，那么django的变量怎么进而传递给javascript呢。本小节参考了 [这个网页](https://stackoverflow.com/questions/7165656/passing-objects-from-django-to-javascript-dom) 。

首先要传递的字段建议如下json封装下：

```
from django.core.serializers.json import DjangoJSONEncoder
{
	what : json.dumps(data['content_images'], cls=DjangoJSONEncoder)
}
```

然后在javascript那边：

```
var what = JSON.parse("{{ what | safe | escapejs }}")
```

注意 `safe` 和 `escapejs` 过滤器。



## 扩展用户模型

本小节主要参考了这篇 [不错的文章](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html) 。一般扩展django自带的用户模型，最常见的就下面两种情况，实际上这两种情况你可能都会使用到。第一种是 User 模型 和 Profile 模型的分开，然后User用来存放登录相关信息，而Profile用来存放更多的用户资料信息，一般User 和 Profile 是 onetoone 关系，这个时候我们会考虑建立一个signals文件来保证没创建一个User就会跟着创建一个Profile：

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Profile

from .models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

然后你可能对django默认的auth机制，比如session cookies等不太满意，那么推荐你直接建立自己的 User 模型， 继承自 AbstractBaseUser ，我大概看了一下 AbstractBaseUser 的源码，其做的工作都是围绕着 password这个字段来的，而且只要你在settings里面定义好了:

```
AUTH_USER_MODEL = ...
```

就都是可以正常工作的。继承之后定义自己的字段这是不多用多说的，然后推荐进一步继承 `PermissionsMixin` 这个类。

```
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
```

`PermissionsMixin` 这个类定义了一些群组信息还有什么的。

然后这三个字段属性有特殊含义，都是可以自己设置的：

```
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
```

然后你需要写好 objects 这个 UserManager ，其继承自 `BaseUserManager` ，你可以做其他一些定制，这个是个什么东西？这个就是之前我们看到的 `Model.objects.what` 之类的这种用法。在这里你需要根据自己的情况定义好： 

- create_user
- create_superuser

这两个方法即可。就用这两个方法来控制用户的创建行为。其中 `create_superuser` 主要负责把 

- is_superuser
- is_staff 

设为True。



## 基于类的视图

首先我们从django哪里初步了解了下基于类的视图的概念，就是如下代码：

```python
from django.http import HttpResponse

def my_view(request):
    if request.method == 'GET':
        # <view logic>
        return HttpResponse('result')
```

变为更简洁的：

```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')
```

然后依赖类的继承，引入Minxin类，可以让我们在http的很多restful风格请求上，总是一次又一次出现的那些套路，实现代码复用。其基本知识就是python的类的继承，我们可以直接从django restframework 这个模块直接用手来见识这种DRY理念的实现。

### APIView

django restframework的 APIView 继承自 django 的 View，然后针对restful api 进行了很多优化，在某些情况下可能你编写的视图，就继承自APIView就是合适的，后面介绍的通用视图和其他高级视图等等，都是在某些情况下特别合适和让你少写代码，好用就用，仅此而已。如果不合适，那么自己定义 get post put 等等方法也是很方便的。



### 视图再升级

在某些情况下使用 APIView 类和 Mixin 可能是最合适不过的，下面谈谈django restframework 提供的高级通用视图类。这些类都是继承自 `GenericAPIView` ，他们都有一个特点，那就是有点类似于 Serializer -> ModelSerializer 的升级过程，如果你的视图类方法主要操作对象是基于数据库Model的各个操作，那么推荐视图类继承自 `GenericAPIView` 。

### GenericAPIView

GenericAPIView 继承自 django restframework 的 APIView 类，其提供的一个很重要的特性是 `queryset` ，你设定 queryset属性或者实现 `get_queryset` 方法，该视图类的很多方法都是围绕着`queryset` 来展开的。

具体 CRUD 数据操作有对应的 Minxin类，然后和GenericAPIView 组合出了很多高级的视图类。

一个好的建议对于这块，看源码，源码都很简单的，看懂了，发现符合自己的需要那就使用它，让自己少写点代码。如果有额外的定制需求，那就重写对应的某个方法就是了。



## 权限管理

### 认证

在视图类里定义 `authentication_classes` 来确定目标视图类的认证行为，如果没有则采取默认的认证管理类行为。

### 自定义身份认证

写自己的身份认证类，继承自 `BaseAuthentication` ，然后重写 `authenticate(self, request)` 方法，认证成功则返回 `(user, auth)` ，否则返回None。request.user 是当前登录的用户实例， request.auth 是当前登录auth的信息。

某些情况下身份认证失败你可能想要抛出 `AuthenticationFailed` 异常。

### 权限

在视图类里定义 `permission_classes` 来确定目标视图类的权限管理行为，如果没有则采用默认的权限管理类行为。

认证完了就会进去权限管理，也就是权限检查的时候 `request.user`  `request.auth` 已经是可以调用的了。

最简单的权限管理类就是 `IsAuthenticated` ，允许通过身份验证的用户访问，拒绝没通过的用户访问。

`IsAuthenticatedOrReadOnly` 类的意思是通过身份认证的用户完全访问，没有通过身份验证的用户只能进行只读访问。

### 自定义权限管理类

自定义权限管理类，继承自 `BasePermission` ，然后实现下面一个两个方法：

- has_permission(self, request, view)
- has_object_permission(self, request, view, obj)

如果请求被授予权限，则返回True，如果没有权限则返回False。

自定义权限管理类还可以加上 `message` 属性，用户权限没通过抛出 `PermissionDenied` 异常的额外显示信息。





## 日志管理

django使用python的logging模块来作为的自己的日志系统，所以django项目日志管理的深入学习离不开对于logging模块的深入学习。

## logging模块中级教程

logging模块的中级使用需要了解如下几个词汇：loggers, handlers, filters, and formatters。

### loggers 

记录器 之前我们运行logging.info，就是调用的默认的记录器，然后一般我们会针对每个python的模块文件创建一个记录器。

```
logger = logging.getLogger(__name__)
```

这个 `__name__` 只是一种简便的命名方法，如果你勤快或者某种情况下有需要的话完全可以自己手工给记录器取个名字。

然后这个 `getLogger` 函数如果你后面指定的名字之前已经定义了（这通常是指在其他第三方模块下定义了），那么你通过这个 `getLogger` 然后指定目标名字就会得到对应的该记录器。这通常对于DIY某个第三方模块的日志记录器有用。

记录器可以挂载或者卸载某个处理器对象或过滤器对象：

- logger.addHandler()
- logger.removeHandler()
- logger.addFilter()
- logger.removeFilter()

记录器通过 `setLevel()` 方法来设置最小记录级别，这个和后面的Handler级别是协作关系。

### handlers 

处理器负责分发日志信息到目标地去。这里主要介绍这几个Handler类：

- StreamHandler 将信息以流的形式输出，这通常指输出到终端
- FileHandler 将信息写入到某个文件中去
- RotatingFileHandler 将信息写入某个文件，如果文件大小超过某个值，则另外新建一个文件继续写。
- TimeRotatingFileHandler 将信息写入某个文件，每隔一段时间，比如说一天，就会自动再新建一个文件再往里面写。

处理器对象也有 `setLevel` 方法，这个前面也提及了，和记录器的 `setLevel` 是协作关系，更详细的描述是，信息先记录器处理并分发给对应的处理器对象，然后再处理器处理再分发到目的地。

处理器可以挂载 格式器 对象和 过滤器 对象。

- handler.setFormatter()
- handler.addFilter()
- handler.removeFilter()



### filters 

过滤器

### formatters 

格式器，具体信息的格式定义。

### 字典统一配置

django的setting.py就会有这样的配置，具体含义还是很明显的，就是定义处理器，格式器，记录器等。

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "%(asctime)s %(name)s [%(levelname)s] %(thread)d %(module)s %(funcName)s %(lineno)s: %(message)s"
        }
    },
    'handlers': {
        'log_file': {
            'class': 'sdsom.common.log.DedupeRotatingAndTimedRotatingFileHandler',
            'filename': config.get('web', 'log_path'),
            'when': 'midnight',
            'maxBytes':int(config.get('web','log_max_bytes')),
            'interval': 1,
            'backupDay': int(config.get('web', 'log_backup_days')),
            'dedupetime': int(config.get('web', 'log_dedupe_time')),
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['log_file'],
            'level': config.get('web', 'log_level'),
            'propagate': True,
        },
    }
}
```



## 自定义命令

在目标app下面新建一个 `management` 文件夹，然后新建一个 `commands`  文件夹，注意这两个文件夹都要带上 `__init__.py` 文件。

然后commands文件夹里面就可以定义一些python脚本了，这些脚本成为命令可以直接如下调用：

```
python manage.py command_name
```

你可以通过：

```
python manage.py help
```

来查看目前已经有的命令列表。

一个基本的命令模块如下所示：

```python
from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
```



## django和celery

django-crontab这个模块我试过的，还是很便捷的，不过其还是基于系统的crontab，而如果我们将django和celery组合起来，celery灵活的消息分发机制，无疑将给未来开发带来更多的可能性。celery的官方文档在 [这里](http://docs.celeryproject.org/en/latest/index.html) ，本文主要讲一下celery的基本概念和django的集成问题，更多celery的知识请参阅官方文档。



### celery的核心概念

- broker  任务队列服务提供者，celery推荐使用redis或者rabbitmq作为broker。
- task 具体执行的任务，其实就是定义的一些函数。
- backend 用来存储任务之后的输出结果
- worker celery的启动就是开启一个worker。



### django内文件安排

本小节参考了 [这篇文章](https://medium.com/@yehandjoe/celery-4-periodic-task-in-django-9f6b5a8c21c7) 和 [这篇文章](http://geek.csdn.net/news/detail/128791) 。需要提醒读者的是，django和celery集成现在并不需要额外安装什么插件了，而且下面讲的配置实际上就是一个单独的celery app大部分都是类似的，只是多了一些细节上的处理和优化。

#### celeryconfig.py 

首先推荐在你的django app `settings.py` 旁新建个 `celeryconfig.py` 文件，有的教程让设置这个配置文件名字为 `celery.py` ，这样很不好，文件名和某个模块名字重复有时会出问题的。里面的内容如下：

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

app = Celery('project_name')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

这个下面新建的任务不过是方便测试罢了，然后上面几行配置基本上死的。最值得讲的就是这两行：

```
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

第一行是从django的配置对象中读取配置，特别注意的就是那个 `namespace='CELERY'` ，这样只有 `CELERY_` 开头的配置才会读取，而且对应原celery配置的关系是：

```
CELERY_BROKER_URL  -> BROKER_URL
```

我那次就是 `CELERY_BEAT_SCHEDULE` 写成了 `CELERYBEAT_SCHEDULE` 然后老实发现周期性程序启动不起来。

第二行也是一个优化细节，从函数名字也可以看到，就是自动发现任务。在你的django的其他app里面新建一个 `tasks.py` ，celery会自动发现你定义的任务。



#### `__init__.py` 

还是你的django项目的project `settings.py` 那个文件夹里面，`__init__.py` 推荐写上这几行内容：

```
from .celeryconfig import app as celery_app

__all__ = ('celery_app',)
```

#### settings.py

具体celery的一些配置就统一写在 `settings.py` 文件里面，上面也提到了，都要 `CELERY_` 开头，大体如下所示：

```
CELERY_BROKER_URL = 'redis://localhost:6379'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'
#CELERY_ACCEPT_CONTENT = ['application/json']
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
# schedules
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'crawl_juhe_every_one_hour': {
         'task': 'wxarticles.tasks.crawl_juhe',
         'schedule': crontab(minute=0, hour='*/3'),
    },
    'every_miniute_for_test': {
        'task': 'wxarticles.tasks.test_celery',
        'schedule': crontab(),
    },
}


```

#### 定义任务

好了，定义任务，实际上就是定义一个函数，比如下面这个简单的打印函数来确认celery周期程序是工作着的：

```
from celery import shared_task

@shared_task()
def test_celery():
    print('celery is working.')
```

celery的crontab功能很强大，比如上面的 `crontab()` 就是每分钟执行一次。具体请参看 [官方文档](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) 之。

#### 启动任务

和celery其他操作都是一样的，就是启动worker：

```
celery -A project_name worker -l info
```

`-A` 选项跟着 celery app的名字，在这里也就是django项目的名字。 `-l` 选项设置日志打印级别。

你还可以加上 `-B` 来同时启动周期性任务。

或者另外开个命令：

```
celery -A project_name beat -l info
```





------

其他制作脚本啊，制作后台程序，制作服务啊，使用supervisor啊，实际上和celery关系已经不大了，可以不在这里说了。



#### 手工启动一次任务

参考了 [这个网页](https://stackoverflow.com/questions/12900023/how-can-i-run-a-celery-periodic-task-from-the-shell-manually) 。

```
$ python manage.py shell
>>> from myapp.tasks import my_task
>>> eager_result = my_task.apply()

```



## 翻译

django的翻译其实已经很便捷了，因为我关注于后台api的编写，所以实际上很多教程说的：

```
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'django.template.context_processors.i18n',
            ],
        },
    },
]
```

这个配置只和模板输出的翻译有关，有需要再加上。

然后MIDDLESWARES 哪里要加上：

```
    'django.middleware.locale.LocaleMiddleware',
```

然后就是这些配置：

```
LANGUAGE_CODE = 'zh-Hans'

USE_I18N = True
```

设置好你的语言代码，这是没有问题的。

我看了一下 django restframework 的翻译管理相关，发现大体这样配置就可以了，很多教程说的设置 `LOCALE_PATHS` 变量觉得没必要，默认的每个app下面的locale文件夹够用了。

然后就是目标py文件下的 字符串 如下装饰之：

```
from django.utils.translation import ugettext_lazy as _
...

        if username is None:
            raise TypeError(_('Users must have a username.'))
```

Model字段定义的名字可以加上，verbose_name 可以加上，然后异常信息可以加上等等。

加完了之后运行：

```
django-admin makemessages -l zh_Hans 
```

app下面没有locale文件夹的创建个就是了，某些文件你不想管，比如 manage.py ，那么加上 `--ignore` 选项即可。

windows下不是很方便，推荐在linux服务器下创建了目标 django.po 文件，然后再修改文件即可。其中po文件的头部有些东西，估计：

```
"Language: zh-Hans\n"
```

已经是必填的，其他有时间也填上吧。

然后运行:

```
django-admin compilemessages 
```

如果不出意外的，翻译就已经生效了。





## 创建可复用的app

创建可复用的app会极大的降低你的目标django项目的复杂度，如果可能，将你的app打造成可复用的风格总是首选。

### 制作django-what的pypi包

有关pypi包的制作就不赘述了，下面主要在官方文档 [这里](https://docs.djangoproject.com/en/1.11/intro/reusable-apps/) 的基础上讨论一些问题。

### 测试问题

我试着如下安装测试过程：

```
python setup.py sdist
pip install dist/what.tar.gz
```

然后安装官方文档，在INSTALL_APPS那里设置好。app是可以正常使用的。但在安装测试过程中，这实在有点繁琐了。推荐还是将整个app文件夹复制到你的测试webapp那边去，然后一边修改一边看。测试好了再把内容同步到pypi安装包那边去。

### migrations问题

官方文档之所以选择制作sdist和用pip install tar包这种风格是有原因的，经测试egg包在访问上很成问题，只有用pip安装这种方法，在site-packages那边你安装才是文件夹风格而不是那种egg文件。这样你等下执行：

```
python manage.py makemigrations app_name
```

才会成功。

而且实际生成的迁移文件就放在site-packages那里的目标文件夹下的。所以你制作pypi包的时候不要把migrations文件夹里面的其他迁移文件包含进去了，要包含就包含 `__init__.py` 文件即可。

当然就算你不是制作django的目标pypi包，其他django项目在 `.gitignore` 文件上加上这一行总是不错的：

```
*/migrations/*
```

PS: 我知道stackoverflow那边都认为应该加上，还有人专门写了长篇大论认为应该加上。我确定的只有一点：早期测试开发过程，所有的migrations文件夹里面都只有 `__init__.py` 这个空白文件，保持代码整洁，在测试开发阶段不花精力在这上面，这是没有争议的。



## 部署

这里所谓的部署就是用apache或nginx这样的web服务器来对接django项目，说的再具体一点就把django作为一个wsgi程序服务起来。

本文关于apache的部署讲解较为成熟。

### apache

上例子吧：

```
<IfModule !wsgi_module>
    LoadModule wsgi_module modules/mod_wsgi.so
</IfModule>

WSGIPythonHome "/home/wanze/venv"
WSGIPythonPath "/home/wanze/venv/webapp"

<VirtualHost *:80>
    ServerName api.cdwanze.work
	
    WSGIScriptAlias / /home/wanze/venv/webapp/webapp/wsgi.py
	
    <Directory /home/wanze/venv/webapp >
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order deny,allow
            Allow from all
        </IfVersion>
    </Directory>

	Alias "/static" "/home/wanze/venv/webapp/static"
    
    <Directory  /home/wanze/venv/webapp/static >
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order deny,allow
            Allow from all
        </IfVersion>
    </Directory>
    
</VirtualHost>
```

- 首先是检测wsgi模块加载了没有，没有把它加载上。
- WSGIPythonHome 这个设置你的python的虚拟环境的所在目录，比如上面的例子 venv/bin下面就是python可执行脚本。
- WSGIPythonPath 这个设置你的Django项目目录所在
- WSGIScriptAlias 这个设置你的WSGI文件所在
- Alias 和下面Directory 设置是服务你的项目的静态文件的。

### 关于静态文件

关于静态文件再补充下，上面服务的静态文件是在项目目录下的static文件夹下，这里所谓的静态文件主要是djano和djangorestframwork等框架带的静态文件，其通过  `python manage.py collectstatic` 命令来生成这些内容。

你需要在settings那里设置 `STATIC_ROOT` 值。

```
STATIC_ROOT= os.path.join(BASE_DIR, 'static')
```



### 多django站点部署问题

多个django站点都通过 `mod_wsgi` 来部署是不能继续像前面那样写： 

```
WSGIScriptAlias / /path/to/mysite.com/mysite/wsgi.py
WSGIPythonHome /path/to/venv
WSGIPythonPath /path/to/mysite.com
```

而必须每个通过deamon模式来（参考了 [这个网页](https://stackoverflow.com/questions/14923083/multiple-sites-in-django) ）：

```
<VirtualHost *:80>
    ServerName api.cdwanze.work
    WSGIDaemonProcess cdwanze_api  processes=1 python-path=/home/wanze/venv/myapi python-home=/home/wanze/venv/ threads=10	
    WSGIProcessGroup cdwanze_api
    WSGIScriptAlias / /home/wanze/venv/myapi/myapi/wsgi.py process-group=cdwanze_api
    ...
```

其中 `WSGIProcessGroup` 目前来看名字是随意的，但必须写。然后在定义daemon进程的时候 `python-path` 是定义到你的django project那里， `python-home` 是定义到你的python虚拟环境那里。



### 文件权限问题

除了上面设置好 Directory 之外，你可能还会遇到其他某些文件的读写权限问题，在查看日志的时候发现提示说那个文件没有权限读写了。这个时候首先要明确httpd的执行User和Group是谁，然后在看目标文件夹或文件的具体权限。

Django项目的wsgi文件是需要有执行权限的。还有Django项目操纵数据库，比如sqlite3这种文件数据库，你可能也会遇到读写权限问题。

还有值得一提的是如果某个母文件夹没有可执行权限，那么里面的所有文件都是不可见的。

### nginx

nginx要对接wsgi接口需要uwsgi这个模块将wsgi接口服务起来。

```
pip install uwsgi
```

更多细节请参看uwsgi的 [官方文档](http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html) 。

ngnix的配置如下：

```
upstream django {
    server 127.0.0.1:8001; 
}

server {
    location / {
        uwsgi_pass  django;
        include     /path/to/your/mysite/uwsgi_params; 
    }
}
```



#### nginx serve 静态文件

```
server {
    listen      80;
    ......
 
    client_max_body_size 75M;
 
    location /media  {
        alias /path/to/media;
    }
 
    location /static {
        alias /path/to/static;
    }
    
    ......
}
```



更多nginx配置细节请参看我写的关于nginx配置的专门的文章。



## 对外部署必看

django项目如果对外部署的话，因为python是一个动态脚本语言，所以会有很多安全性的问题需要检查，否则你的项目对外会很不安全。本文主要参看官方文档的 [这里](https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/) 。

第一当然首先是确保 `DEBUG=False` ，对外开着 `DEBUG=True` 那简单是开玩笑了。

然后是运行：

```
python manage.py check --deploy
```

### settings.py 里密钥外置

settings.py 文件里面不要有任何密钥信息，包括 `SECRET_KEY` 你的数据库连接信息或者其他密钥等等，所有这些信息都应该作为环境变量引入或者从某个配置文件中读取出来。

### ALLOWED_HOSTS

要某是限定好域名，要某是你的nginx服务器那边对入口请求已经做好了限定，凡是不认识的域名HOST请求都抛出444错误：

```
server {
    listen 80 default_server;
    return 444;
}
```



## API设计

首先讲一下这里讨论的API设计和网络上流行的Restful风格的API设计都只是一般性原则，并不是强制性的要求。然后API还分为内部使用和对外的API，如果对外的API那么接口最好遵循无惊讶原则，遵循大家都通用的一些写法风格，但如果是内部使用的API，那么很多情况下，还要考虑自己内部使用的便捷性要求。

### url设计

目前url域名都推荐使用 api.what.com 这样的风格，然后关于API的版本，在URL上加上版本号，并不是一个很好的主意。在当前前后端分离的大背景下，这给前端和后端的代码都带来了一些额外的复杂度。

版本号按照 [阮一峰的这篇文章](http://www.ruanyifeng.com/blog/2011/09/restful.html) ，推荐使用 Accept 字段：

```
Accept: vnd.example-com.foo+json; version=2.0
```

url的第一个字段我喜欢使用django的app的名字，然后接下来的第二个字段推荐按照 Restful 风格写上目标资源的名字，并不一定要强制写上名词的复数形式，不过如果有两个url，一个是操纵目标资源集，一个是定向操纵某个目标资源，那么尾缀写上s区分是推荐的风格。

然后针对某个资源或者目标资源集的一些额外的动作，这里所谓的额外的动作是指除了常规的Restful风格的那些增删查改动作之外的额外的动作需求，在上面讨论的Restful风格url基础上加上第三个字段，第三个字段是额外动作的名字是个不错的风格。

### 方法设计

方法通用的 GET POST ，GET用于查询获取资源信息，POST用于创建或修改信息这是没有疑问的。

虽然Restful风格还推荐的DELETE，PATCH等方法，但似乎大家实际编写都只是使用GET和POST方法。

### 参数设计

查询操作如果针对的是目标资源集合，有以下参数是推荐加上的：

- limit 返回个数
- offset 偏移值，可以通过它来实现分页效果
- sort 或者sortby等，总之一个排序的参数
- reverse 排序是否反转的参数

### 状态码设计

具体请参看HTTP的各个状态码。

### 返回内容结构设计

我喜欢使用这种风格：

1. 成功则直接返回各个结果：

```
{
    'a':1
}
```

有些人会说成功之后也应该加上code:200的代码，可是这是完全没有必要的，如果你需要获取数据，那么拿就是了，如果你怕数据不存在，那么加个针对目标数据的判断即可。加个code:200，但是目标数据字段还是不存在，程序不一样也会报错？

2. 失败则必须带上code错误码和msg错误信息

```
{
    'code': 10001,
    'msg': 'your error msg'
}
```

错误码软件系统内部应该有一个统一的规范，常见的错误类型有：

- 资源没有找到
- 找到多个资源
- 未知错误
- 输入缺少参数

### 编写良好的文档

这是当然。



## 其他技巧

### 模型python2兼容性

为了提高模型python2兼容性，推荐模型定义上加个如下装饰器。

```
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible 
class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text
```

以前不加这个装饰器，python2之前用的是 `__unicode__` 方法。

### 重置migrations

一般的方法把migrations文件删掉，把表格删掉并不能成功，因为他们忽视了django_migrations这个表格里面的数据（参考了 [这个网页](https://stackoverflow.com/questions/23755523/how-to-reset-migrations-in-django-1-7)）。

如果你把 `django_migrations` 里面的对应app的迁移数据删掉，然后再makemigrations和migrate，那么就更重新开始的一样。

```
python manage.py makemigrations app_name
python manage.py migrate app_name
```

### 处理列表对象

我们需要自定义一个model的新Field对象来解决这个问题，具体就叫做ListField。

```
def parse_to_python(value):
    try:
        value = ast.literal_eval(value)
        return value
    except Exception as e:
        rasie ValidationError


class ListField(models.TextField):
    """
    存储python列表对象
    """
    description = _("Stores a python list")

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            value = value

        if isinstance(value, list):
            return value

        return parse_to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        value = six.text_type(value)
        return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value

        return parse_to_python(value)

```

- `from_db_value` 当数据从数据库里面读取出来，总会调用这个方法。包括（including in aggregates and [`values()`](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.query.QuerySet.values) calls。 所以这是最重要最核心的一个定制方法，其含义是很明显的，不用多说了。

  ------

这四个方法大体如下流程：

```
python  <- to_python  <-   from_db_value<- database

python ->value_to_string -> get_prep_value -> database

```

**NOTICE** 上图主要是方便读者理解，实际上django并不是这样逐个处理的。按照官方文档的说法 `to_python` 和django的反序列（deserialization ）有关，其还必须处理好三种情况：None，目标对象，字符串情况。

`value_to_string` 和序列化有关，和`to_python` 是相对的。`get_prep_value` 和我们在输入get(what='20170809') 执行查询是有关，讲过其转化成为sql实际查询中用到的字符串（比如说datetimefield）就做了一些额外的处理工作。 



### 多数据库处理

一个django项目里面可能因为某些原因，某些app需要单独操作另外的数据库，这种情况你首先在 `settings` 那里定义好数据库的配置：

```
    DATABASES = {
        'default': {
			...
        },
        'newdb': {
            'ENGINE': 'django.db.backends.mysql',
			...
        },
```

然后加上这个dbroute对象：

```
DATABASE_ROUTERS = ['articles.dbrouter.ArticlesRouter']
```

然后在你的app那里定义好dbroute对象：

```django
class ArticlesRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'articles':
            return 'articles'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'articles':
            return 'articles'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'articles' or \
            obj2._meta.app_label == 'articles':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'articles':
            return db == 'articles'
        return None
```

从上面的代码可以看出来，你定义的模型 `Meta` 那里必须定义好 `app_label` 属性。更多信息请参看官方文档的 [这里](https://docs.djangoproject.com/en/1.11/topics/db/multi-db) 。

### 如何根据django的模型对象来获取其对应的表格的名字

参看 [这个网页](http://stackoverflow.com/questions/233045/how-to-read-the-database-table-name-of-a-model-instance) 。

答: 

```
model_instance._meta.db_table
```

### 如何使用好django的ImageField

参考了 [这篇文章](http://gregblogs.com/django-saving-an-image-using-imagefield-explain-a-little/) 。

ImageField和FileField很类似，除了还多了 `width` 和 `height` 属性，然后就是在上传的时候确保文件是图片文件。

具体在模型文件中的定义如下:

```
banner = models.ImageField(upload_to=game_2048_images, blank=True,
                           storage=OverwriteStorage(), default="placeholder.jpg")

```

上面的 `upload_to` 是控制图片在计算机中的保存路径，可以直接指定一个文件夹路径，但这通常不够灵活，这里通过一个函数来实现更加灵活的路径指定:

```
def game_2048_images(instance, filename):
    """
    where image upload to.
    """
    return 'game/2048/images/{}/{}'.format(instance.user.username, filename)

```

这里具体路径是根据你在 `settings` 里面指定的 `MEDIA_ROOT` 而来，然后再指定里面的具体的文件夹路径。我们看到函数还可以接受具体模型对应的实例，从而建立自动根据user用户名来分配不同的文件夹路径。

`storage=OverwriteStorage()` 实现了如果文件名重复则覆盖的逻辑:

```
class OverwriteStorage(FileSystemStorage):
    '''
    存储文件或图片，如果文件名重复则覆盖。
    '''

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

```

ImageField 可以和rest\_framework的序列化类形成很好的联动，最后序列化之后返回的是文件路径url字符串，测试的时候我们可以如下用django来挂载这些静态资源文件，实际运营的时候则推荐用nginx怎么设置一下url分发。

```
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static('/data/', document_root=settings.MEDIA_ROOT)

```

在保存传过来的图片文件的时候，常规构建form对象也是可行的:

```
form = Game2048InfoForm(
    request.POST, request.FILES, instance=target_info)

if form.is_valid():
    new_game_info = form.save()
else:
    logger.warning('form invalid')

```

否则你需要通过:

```
request.FILES['imgfield']

```

这样的语法来获取图片内容。

### django的messages系统

本小节主要参看了 [这个网页](https://www.webforefront.com/django/setupdjangomessages.html) 。

使用django的messages系统，首先需要如下所示在settings里面进行一些配置：

```
INSTALLED_APPS = [
    'django.contrib.messages',
    ......

MIDDLEWARE_CLASSES = [
    'django.contrib.messages.middleware.MessageMiddleware',
    ......

TEMPLATES = [
    {
         'OPTIONS': {
            'context_processors': [
                'django.contrib.messages.context_processors.messages',
                ......

```

然后在views那边，使用 `messages.add_message()` 来往django信息系统里面发送一个信息，此外还有如下的这些快捷方法：

- messages.debug()
- messages.info()
- messages.success()
- messages.warning()
- messages.error()

你还可以如下设置每个request请求下的信息系统级别：

```
from django.contrib import messages
messages.set_level(request, messages.DEBUG)

```

下面我定义了一个简单的flash函数

```python
def flash(request, title, text, level='info'):
    """
    利用django的message系统发送一个信息，对接模板的sweetalert。
    """
    level_map = {
        'info': messages.INFO,
        'debug': messages.DEBUG,
        'success': messages.SUCCESS,
        'warning': messages.WARNING,
        'error': messages.ERROR
        }

    level = level_map[level]

    messages.add_message(request, level, text, extra_tags=title)
    return 'ok'
```

之所以做这样的封装是为了更好地对接sweetalert这个javascript库，然后模块加入如下内容从而从而实现信息的具体弹出行为。

```
{% if messages %}
<script src="{% static 'js/sweetalert.min.js' %}"></script>
<script>
{% for msg in messages %}
    sweetAlert({
        title: '{{msg.extra_args}}',
        text: '{{ msg.message }}',
        type: '{{ msg.level_tag }}',
      })
{% endfor %}
</script>
{% endif %}
```

### csrf认证失败

一般提到的表单那边加上：

```
<form method="post">{% csrf_token %}
```

但后来我还是遇到csrf认证失败问题，最后参考 [这个问题的答案](https://stackoverflow.com/questions/38841109/csrf-validation-does-not-work-on-django-using-https) 如下设置才可以。

```
CSRF_TRUSTED_ORIGINS = ['www.cdwanze.work']
```

