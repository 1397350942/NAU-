import hashlib

# 用于密码加密
from django.http import HttpResponse

from user.models import User


def md5(s):
    s = s.encode("utf8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


# 装饰器函数，用于检查登录状态
def check_login(fn):

    def wrap(request, *args ,**kwargs):
        # 先判断有没有登录状态
        if 'username' not in request.session:
            return HttpResponse('<script>alert("您还未登录，请先登录！");location.href = "/"</script>')
        else:
            uname = request.session.get('username')
            user = User.objects.get(username=uname)
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

        return fn(request, *args, **kwargs)

    return wrap
