'''
    初始化数据库数据，
'''
import os
import django
import sys

pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(pwd)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PayOutSystem.settings")
django.setup()

from goods.models import Goods, Status, Files
from user.utils import md5
from user.models import User

def init():
    # 初始化订单状态数据
    s1 = Status.objects.create(id=1, status='未处理')
    s2 = Status.objects.create(id=2, status='已处理')
    s3 = Status.objects.create(id=3, status='正在处理')
    s4 = Status.objects.create(id=4, status='已超时')
    s5 = Status.objects.create(id=5, status='延时处理')
    s6 = Status.objects.create(id=6, status='已删除')

    # 初始化用户数据
    user = User.objects.create(id=1,
                               username='Admin',
                               password=md5('password'),
                               name='Admin',
                               number='88888888',level='0')

    # 初始化工单数据
    goods1 = Goods.objects.create(id=1,
                                 createtime='2022-3-12 12:00:00',
                                 number='test001', title='测试工单1',
                                 content='这是一个测试工单，若系统正式运行，建议删除此工单。',
                                 goods_type='物流问题',
                                 other='备注内容备注内容备注内容备注内容备注内容',
                                 clent_name='张三',
                                 goods_name='牛奶',
                                 goods_count='100',
                                 buy_date='2022-3-5',
                                 status=s1,
                                 time=86400,
                                 t_user=user
                                 )
    goods2 = Goods.objects.create(id=2,
                                 createtime='2022-3-12 12:00:00',
                                 number='test002', title='测试工单2',
                                 content='这是一个测试工单，若系统正式运行，建议删除此工单。',
                                 goods_type='货物问题',
                                 other='备注内容备注内容备注内容备注内容备注内容',
                                 clent_name='张三',
                                 goods_name='牛奶',
                                 goods_count='100',
                                 buy_date='2022-3-5',
                                 status=s1,
                                 time=86400,
                                 t_user=user,
                                 )
    goods3 = Goods.objects.create(id=3,
                                 createtime='2022-3-12 12:00:00',
                                 number='test003', title='测试工单3',
                                 content='这是一个测试工单，若系统正式运行，建议删除此工单。',
                                 goods_type='物流问题',
                                 other='备注内容备注内容备注内容备注内容备注内容',
                                 clent_name='张三',
                                 goods_name='牛奶',
                                 goods_count='100',
                                 buy_date='2022-3-5',
                                 status=s1,
                                 time=86400,
                                 t_user=user,
                                 wuliu_number='123123321'
                                 )

    # 初始化上传文件数据
    file = Files.objects.create(id=1,
                                filename='test.jfif',
                                isimg=True,
                                goods_id=2,
                                file='/media/updataFiles/test.jfif'
                                )

if __name__ == '__main__':
    init()

