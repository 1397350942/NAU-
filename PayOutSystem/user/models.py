from django.db import models

# Create your models here.

class User(models.Model):
    # 用户名
    username = models.CharField('用户名', max_length=20, unique=True)
    # 密码，存储的密码通过md5加密处理
    password = models.CharField('密码', max_length=32)
    # 姓名
    name = models.CharField('姓名', max_length=11)
    # 手机号
    number = models.CharField('手机号', max_length=11)
    # 权限级别 0:管理员 1：售后人员 2：申报人员
    level = models.CharField('级别', max_length=1, default=1)
    # 是否活跃
    is_active = models.BooleanField('激活', default=True)
    # 头像路径
    head_photo = models.FileField(upload_to='headPhoto', default='/headPhoto/bdd.jpg')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updata_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{username：%s, name：%s, level：%s, is_active：%s}' % (self.username, self.name, self.level, self.is_active)

    class Meta():
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

