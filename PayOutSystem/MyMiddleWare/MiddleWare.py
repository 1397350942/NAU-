import time

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core import mail
import traceback


class MMWE(MiddlewareMixin):

    # 配置视图异常时推送邮件到管理员邮箱
    def process_exception(self, request, exception):
        print("---------------服务错误，发送异常邮件------------------")
        message = """
            time：
                %s
                
            user_ip：
                %s
                
            url：
                %s
                
            request：
                %s
                
            method:
                %s
                
            request_GET_body:
                %s
                
            request_POST_body:
                %s
                
            error_message：
                %s
                
            error_trace_back：
                %s
            """ % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            request.META.get("REMOTE_ADDR"),
            request.path_info,
            request,
            request.method,
            request.GET,
            request.POST,
            exception,
            traceback.format_exc(),
        )
        mail.send_mail(
            subject='售后系统异常警告',
            message=message,
            from_email='1294992675@qq.com',
            recipient_list=['1294992675@qq.com']
        )

        print(exception)
        print(traceback.format_exc())

        # 视图异常时调用
        return HttpResponse('当前服务器忙，请稍后再试..  ')
