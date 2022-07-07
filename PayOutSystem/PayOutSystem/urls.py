"""PayOutSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as hv
from goods import views as gv
from user import views as uv
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录页
    path('', hv.login),
    # 主页
    path('home/', hv.home),
    # 所有工单列表
    path('goods/', gv.goods),
    # 过滤工单
    path('get_goods/', gv.get_goods),
    # 创建用户
    path('create_user/', uv.create_uesr),
    # 退出用户
    path('exit_user/', uv.exit_uesr),
    # 修改用户信息
    path('updata_user/<int:user_id>', uv.updata_user_view),
    # 添加工单
    path('add_goods/', gv.add_goods),
    # 伪删除工单
    path('delete_goods/<int:id>', gv.delete_goods),
    # 真删除工单
    path('real_delete_goods/<int:id>', gv.real_delete_goods),
    # 查看工单详情
    path('check_goods/<int:id>', gv.check_goods),
    # 接取工单
    path('start_goods/<int:id>', gv.start_goods),
    # 延时工单
    path('add_goods_time/<int:id>', gv.add_goods_time),
    # 完成工单
    path('end_goods/<int:id>', gv.end_goods),
    # 查询工单数据
    path('filter_goods/<str:f_type>/<str:f_val>', gv.filter_goods),
    # 查看所有用户
    path('all_users/', uv.all_users),
    # 禁用用户
    path('disable_user/<int:user_id>', uv.disable_user),
    # 启用用户
    path('enable_user/<int:user_id>', uv.enable_user),
    # 用户信息
    path('user_info/<int:user_id>', uv.user_info),
    # 用户信息
    path('me_info/<int:user_id>', uv.user_info),  # 自己的信息
    # 修改用户密码
    path('change_password/',uv.change_password_view),
    # 下载工单信息
    path('download_all_goods/', gv.download_all_goods),  # 自己的信息
    # 查询超时工单
    path('search_timeout/',gv.search_timeout_view)
]

# 将访问上传文件路由 与 访问文件存储路由绑定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
