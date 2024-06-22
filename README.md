## pack
[django](https://pypi.org/project/Django/5.0/)
[python-dotenv](https://pypi.org/project/python-dotenv/1.0.0/)
[psycopg2](https://pypi.org/project/psycopg2/2.9.9/)
django-braces


# DOC
## Rendering and Caching Content 
在上一章中，你使用模型继承和通用关系创建了灵活的课程内容模型。你实现了一个自定义模型字段，并使用基于类的视图构建了一个课程管理系统。最后，你使用异步HTTP请求创建了JavaScript拖放功能，以便对课程模块及其内容进行排序。

在本章中，你将构建访问课程内容的功能，创建学生注册系统，并管理学生报名参加课程。同时，你还将学习如何使用Django缓存框架来缓存数据。

在本章中，你将会：
- 创建用于显示课程信息的公共视图
- 构建学生注册系统
- 管理学生报名参加课程
- 为课程模块呈现多样化内容
- 安装并配置Memcached
- 使用Django缓存框架缓存内容
- 使用Memcached和Redis缓存后端
- 在Django管理站点监控你的Redis服务器

让我们从为学生创建一个可以浏览已有课程并报名参加它们的目录开始吧。

### Displaying courses 
对于您的课程目录，您必须构建以下功能： 
- 列出所有可用课程，可选择按主题过滤
- 显示单个课程概述 
编辑课程应用程序的views.py文件并添加以下代码：
```python

```

这是`CourseListView`视图。它继承自`TemplateResponseMixin`和`View`。在此视图中，您执行以下任务： 
1. 使用 ORM 的 annotate() 方法和 Count() 聚合函数检索所有科目，以包含每个科目的课程总数。 
2. 您检索所有可用课程，包括每门课程中包含的模块总数。
3. 如果给出了主题 slug URL 参数，您将检索相应的主题对象并将查询限制为属于给定主题的课程。 
4. 使用 TemplateResponseMixin 提供的 render_to_response() 方法将对象渲染到模板并返回 HTTP 响应。
让我们创建一个详细视图来显示单个课程概述。将以下代码添加到views.py文件中：
```python

```
该视图继承自 Django 提供的通用 DetailView。您指定 model 和 template_name 属性。 Django 的 DetailView 需要主键 (pk) 或 slug URL 参数来检索给定模型的单个对象。该视图呈现 template_name 中指定的模板，包括模板上下文变量对象中的 Course 对象。 
编辑 educa 项目的主 urls.py 文件并向其中添加以下 URL 模式：
```python

```
You add the course_list URL pattern to the main urls.py file of the project because you want to display the list of courses in the URL http://127.0.0.1:8000/, and all other URLs for the courses application have the /course/ prefix.
Edit the urls.py file of the courses application and add the following URL patterns:
```python

```
You define the following URL patterns: 
- `course_list_subject`: For displaying all courses for a subject
- `course_detail`: For displaying a single course overview

Let`s build templates for the CourseListView and CourseDetailView views. Create the following file structure inside the templates/ courses/ directory of the courses application:
```shell

```
Edit the courses/ course/ list.xhtml template of the courses application and write the following code:
```html

```