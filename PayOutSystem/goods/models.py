import time

from django.db import models
from user.models import User
import time as t

# Create your models here.
'''
    工单状态表
'''


class Status(models.Model):
    # 工单状态
    status = models.CharField('工单状态', default='未查看', max_length=5, unique=True)

    def __str__(self):
        return '{status：%s}' % self.status

    class Meta():
        db_table = 'goods_status'
        verbose_name = '工单状态'
        verbose_name_plural = verbose_name


'''
    工单表
'''


class Goods(models.Model):
    '''
    工单表
    '''

    '''
    自动生成字段
    '''
    # 创建时间
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    # 最后修改时间
    endtime = models.DateTimeField('最后修改时间',auto_now=True)
    # 工单编号
    number = models.CharField('工单编号', default=t.strftime('G%Y%m%d%H%M%S', t.localtime()), max_length=18, unique=True)

    '''
    问题相关
    '''
    # 问题标题
    title = models.CharField('标题', max_length=50)
    # 问题内容
    content = models.TextField('工单内容')
    # 问题类型
    goods_type = models.CharField('问题类型', max_length=10, default='物流问题')
    # 备注
    other = models.TextField('备注', default='无')
    # 处理时限
    time = models.IntegerField('处理时限(s)', default=60*60*72)

    '''
    订单相关
    '''
    # 收货人
    clent_name = models.CharField('收货人', max_length=20, default='无')
    # 物品名
    goods_name = models.CharField('物品名', max_length=100, default='无')
    # 下单数量
    goods_count = models.CharField('下单数量', max_length=20, default='未知')
    # 物流单号
    wuliu_number = models.CharField('物流单号', max_length=50, default='无')
    # 下单时间
    buy_date = models.DateField('下单日期', default='2000-1-1')

    '''
    处理相关
    '''
    # 处理意见
    comment = models.TextField('处理意见', default='暂无处理意见..')
    # 是否激活
    is_active = models.BooleanField('是否激活', default=True)

    '''
    外键
    '''
    # 工单状态
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    # 提交人员
    t_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='t_user')
    # 处理人员
    c_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='c_user')

    def __str__(self):
        return '{number：%s, title：%s, content：%s..., createtime：%s}' % (
        self.number, self.title, self.content[:20], self.createtime)

    class Meta():
        db_table = 'goods'
        verbose_name = '工单'
        verbose_name_plural = verbose_name


"""
    用户上传文件表
"""
class Files(models.Model):

    # 文件名
    filename = models.CharField('文件名',max_length=100)
    # 是否为图片  True 表示图片，Flase 表示视频
    isimg = models.BooleanField('是图片')
    # 文件
    file = models.FileField(upload_to='updataFiles', null=True)
    # 所属工单
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def __str__(self):
        return 'Files{name：%s, is_img：%s, goods：%s}' % (self.filename, self.isimg, self.goods.id)

    class Meta():
        db_table = 'files'
        verbose_name = '上传文件'
        verbose_name_plural = verbose_name