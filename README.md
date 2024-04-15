  #  统一表单系统

###  一、样式本地化

##### 1、生成 collect_static 文件

~~~shell
python manage.py collectstatic
~~~

##### 2、生成  collect_static  文件后，进入项目  settings.py  文件，在文件末尾添加以下代码。

~~~django
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "collect_static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
~~~

##### 3、更换  collect_static  文件下以下路径中的两个图片文件（替换的图片）

![1699688595706](C:\Users\lsheng\AppData\Local\Temp\1699688595706.png)

~~~django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8001
~~~

##### 4、运行项目（非debug模式）

~~~django
python manage.py runserver 0.0.0.0:8000 --insecure
~~~