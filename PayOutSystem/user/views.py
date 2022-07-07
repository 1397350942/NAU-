from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from tests import img_resize
from .utils import check_login
from .models import User
from . import utils

# Create your views here.

'''
    创建用户
    url : create_user/
'''


@check_login
def create_uesr(request):
    user = User.objects.get(username=request.session.get('username'))

    if user.level == '0':

        if request.method == 'GET':
            return render(request, 'user/create_user.html', locals())
        elif request.method == 'POST':
            try:
                uname = request.POST.get('username')
                psd = request.POST.get('password2')
                psd = utils.md5(psd)
                name = request.POST.get('name')
                number = request.POST.get('number')
                level = request.POST.get('level')
                hp_file = request.FILES.get('headphoto')
                headphoto = hp_file if hp_file is not None else 'headPhoto/bdd.jpg'

                user = User.objects.create(username=uname, password=psd, name=name, number=number, level=level,
                                           head_photo=headphoto)
            except:
                return HttpResponse('<script>alert("注册失败, 用户名重复!");location.href = "/create_user"</script>')
            return HttpResponse('<script>alert("注册成功!");location.href = "/home"</script>')
    else:
        return HttpResponse('<script>alert("无用户管理权限!");location.href = "/home"</script>')


'''
    退出当前用户
    url : exit_uesr/
'''


@check_login
def exit_uesr(request):
    if request.method == 'GET':
        try:
            request.session.clear()
            del request.session['username']
            del request.session['remberme']
            del request.session['level']
        except:
            print("退出账户,清除所有session")
        return HttpResponseRedirect('/')


'''
    查看所有用户
    url : all_users/
'''


@check_login
def all_users(request):
    user = User.objects.get(username=request.session.get('username'))

    users = User.objects.filter(is_active=True).order_by('create_time')
    users_length = len(users)
    nousers = User.objects.filter(is_active=False)
    nousers_length = len(nousers)
    if user.level == '0':
        return render(request, 'user/users.html', locals())
    else:
        return HttpResponse('<script>alert("无查看权限!");location.href = "/home"</script>')


'''
    禁用用户
    url : disable_user/user_id
'''


@check_login
def disable_user(request, user_id):
    user = User.objects.get(username=request.session.get('username'))

    if user.level == '0':
        try:
            duser = User.objects.get(id=user_id)

            if user.id == duser.id:
                return HttpResponse('<script>alert("错误，不能禁用自己！");location.href = "/all_users"</script>')
            elif len(User.objects.filter(level='0')) == 1 and duser.level == '0':
                return HttpResponse('<script>alert("用户禁用失败，系统需要至少一个管理员！");location.href = "/all_users"</script>')

            duser.is_active = False
            duser.save()
        except Exception as e:
            print(e)
            return HttpResponse('<script>alert("用户禁用失败，数据错误！");location.href = "/all_users"</script>')

        return HttpResponse('<script>alert("用户禁用成功！");location.href = "/all_users"</script>')
    else:
        return HttpResponse('<script>alert("无权限！");location.href = "/home"</script>')


'''
    启用用户
    url : enable_user/user_id
'''


@check_login
def enable_user(request, user_id):
    user = User.objects.get(username=request.session.get('username'))
    if user.level == '0':
        try:
            duser = User.objects.get(id=user_id)
            duser.is_active = True
            duser.save()
        except:
            return HttpResponse('<script>alert("用户启用失败，数据错误。");location.href = "/all_users"</script>')

        return HttpResponse('<script>alert("用户已启用！");location.href = "/all_users"</script>')
    else:
        return HttpResponse('<script>alert("无权限!");location.href = "/home"</script>')


'''
    查看用户信息
    url : user_info/user_id
'''


@check_login
def user_info(request, user_id):
    user = User.objects.get(username=request.session.get('username'))

    # 管理员 或 本账号用户 才可查看信息
    if user.level == '0' or user_id == user.id:
        luser = User.objects.get(id=user_id)
        return render(request, 'user/userinfo.html', locals())
    else:
        return HttpResponse('<script>alert("无权限，你不能查看其他用户的信息!");location.href = "/home"</script>')


'''
    更新用户信息
    url : updata_user/user_id
'''

@check_login
def updata_user_view(request, user_id):
    if request.method == 'POST':
        my_user = User.objects.get(username=request.session.get('username'))
        try:
            up_uesr = User.objects.get(id=user_id)
            if my_user.level == '0' or my_user.id == up_uesr.id:
                headPhoto = request.FILES.get('headphoto')
                name = request.POST.get('name')
                number = request.POST.get('number')
                level = request.POST.get('level')
                if headPhoto:
                    up_uesr.head_photo = headPhoto
                    up_uesr.save()

                if name:
                    print(name)
                    up_uesr.name = name
                if number:
                    print(number)
                    up_uesr.number = number
                if level:
                    print(level)
                    up_uesr.level = level
                # 保存修改
                up_uesr.save()
                return HttpResponse('<script>alert("用户信息修改成功！");history.back()</script>')
            else:
                return HttpResponse('错误，无权限。', 404)
        except Exception as e:
            return HttpResponse('错误，无此用户。', 404)
    else:
        return HttpResponse('错误的请求方式。',status=404)

'''
    修改用户密码
    url : change_password
'''
@check_login
def change_password_view(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.session.get('username'))
        cuser = User.objects.get(id=request.POST.get('userid'))
        if user.level == '0' or user.id == cuser.id:
            psw = request.POST.get('password')
            psw_md5 = utils.md5(psw)
            cuser.password = psw_md5
            cuser.save()
            return HttpResponse('<script>alert("用户密码修改成功！");history.back()</script>')
        return HttpResponse('无权限', 404)
    else:
        return HttpResponse(content_type='text', content='错误的访问方式', status=404, charset='utf-8')