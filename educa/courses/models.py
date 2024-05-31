from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

# Create your models here.
class Subject(models.Model):
    """课程主题的model class
    
    Attributes:
        model: 继承django model基类
    """
    title = models.SlugField(_("subject title"), max_length=200)
    slug = models.SlugField(_("subject slug"), max_length=200, unique=True)    

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass


class Course(models.Model):
    """课程model类
    Attributes:
        eggs: An integer count of the eggs we have laid.
    """
    owner = models.ForeignKey(User,
                              related_name='course_created',
                              verbose_name=_('courses user'),
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                verbose_name=_('course subject'),
                                on_delete=models.CASCADE)
    title = models.CharField(_("courses title"), max_length=200)
    slug = models.SlugField(_("course slug"), unique=True)
    overview = models.TextField(_("course describe"))
    created = models.DateTimeField(_("created"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass
        # return reverse("Course_detail", kwargs={"pk": self.pk})


class Module(models.Model):
    """课程模块model类
    
    Attributes:
        eggs: An integer count of the eggs we have laid.
    """
    course = models.ForeignKey(Course,
                                related_name='modules',
                                verbose_name=_("module courses"),
                                on_delete=models.CASCADE)    

    title = models.CharField(_("module title"), max_length=200)
    description  = models.TextField(_("description"), blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")
        ordering = ['order']
    def __str__(self):
        return f'{self.order}. {self.title}' 

    def get_absolute_url(self):
        pass
        # return reverse("Module_detail", kwargs={"pk": self.pk})

class Content(models.Model):
    """使用django contenttype

    Attributes:
        eggs: An integer count of the eggs we have laid.
    """
    module = models.ForeignKey(Module,
                               related_name='contents',
                               verbose_name=_("module"),
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={
                                        'model__in': (
                                            'text',
                                            'video',
                                            'image',
                                            'file'
                                        )
                                     })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])
    
    class Meta:
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")
        ordering = ['order']

    def __str__(self):
        return self.object_id

class ItemBase(models.Model):
    """module content 多态基础类
    Attributes:
        eggs: An integer count of the eggs we have laid.
    """
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(_("content title"), max_length=250)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        abstract = True
    def __str__(self):
        return self.title

class Text(ItemBase):
    # module Text 通过代理继承ItemBase基类
    content = models.TextField(_("module text"))

class File(ItemBase):
    file = models.FileField(_("module file"), upload_to='files')

class Image(ItemBase):
    file = models.FileField(_("module image"), upload_to='images')

class Video(ItemBase):
    url = models.URLField(_("module video"))
    
