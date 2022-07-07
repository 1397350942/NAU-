import time

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,request
from user.models import User
from user import utils
from user.utils import check_login
from goods.models import Goods, Status

# Create your views here.

"""
    url : /
    用户登录视图函数
"""
def login(request):
    if request.method == 'GET':
        # 如果用户有登录记录则直接跳转到主页
        if request.session.get('remberme'):
            return HttpResponse('<h3>正在自动登录..</h3><script>setTimeout(function(e){location.href="/home"},1000)</script>')
        # 否则返回登录页面
        return render(request, 'home/login.html')
    elif request.method == 'POST':
        try:
            username = request.POST.get('une')
            password = request.POST.get('pwd')
            user = User.objects.get(username=username)

            # 判断是否是被禁用账户
            if user.is_active == False:
                # 清除账户登录状态
                try:
                    request.session.clear()
                    del request.session['username']
                    del request.session['remberme']
                    del request.session['level']
                except:
                    print("退出账户,清除所有session")
                return HttpResponse('<script>alert("此账户已被禁用！");location.href = "/"</script>')

            # 验证密码
            if utils.md5(password) == user.password:
                # 是否记住用户
                if request.POST.get('rber_me'):
                    request.session['remberme'] = True
                # 保存用户信息
                request.session['username'] = username
                request.session['level'] = user.level
                # 登陆成功，跳转至主页
                return HttpResponseRedirect('/home')
            else:
                return HttpResponse('<script>alert("账号或密码错误");location.href = "/"</script>')
        except:
            return HttpResponse('<script>alert("账号或密码错误");location.href = "/"</script>')
    else:
        return HttpResponse('错误的请求方式..', 404)

"""
    主页视图函数
    url : /home
"""
@check_login
def home(request):
    user = User.objects.get(username=request.session.get('username'))
    user_all = User.objects.filter(is_active=True)
    goods = Goods.objects.filter(is_active=True)

    # 筛选今日新增工单
    import datetime
    start_time = datetime.datetime(2022, 3, 11)
    end_time = datetime.datetime.now()

    # 更新已超时订单 (延时处理、未处理、正在处理)
    for g in goods.filter(status_id__in=(5, 1, 3)):
        # 计算订单从创建至今已过的时间
        diff = datetime.datetime.now().replace(tzinfo=None) - g.createtime.replace(tzinfo=None)
        # 如果间隔时间大于工单 预期时间 则标记为 已超时
        if diff.total_seconds() > g.time:
            g.status = Status.objects.get(id=4)
            g.save()

    goods_info = {
        'all': len(goods),
        'ok': len(goods.filter(status=Status.objects.get(status="已处理"))),
        'now': len(goods.filter(status=Status.objects.get(status="正在处理"))),
        'new': len(Goods.objects.filter(createtime__range=(start_time, end_time))),
        'wait': len(goods.filter(status=Status.objects.get(status="延时处理"))),
        'timeout': len(goods.filter(status=Status.objects.get(status="已超时"))),
        }
    user_info = {
        'all': len(user_all),
        'super': len(user_all.filter(level='0')),
        'shouhou': len(user_all.filter(level='1')),
        'shenbao': len(user_all.filter(level='2'))
    }
    # print(goods_info)
    return render(request,'home/home.html', locals())
