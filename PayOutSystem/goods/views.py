import json
import os
import random
import sys
import threading
import hashlib

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from user.models import User
from goods.models import Goods, Status, Files
from user.utils import check_login,md5
from tests import img_resize,video_resize
import time as t

# Create your views here.

'''
    查看工单主页
    method : GET
    url : goods/
'''


@check_login
def goods(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.session.get('username'))

        # 查询工单详情
        goods_all = Goods.objects.all()

        # 按权限划分
        if user.level == '1':
            goods_all = goods_all.filter(c_user=user)
        elif user.level == '2':
            goods_all = goods_all.filter(t_user=user)

        goods_init = {
            # 待接取工单数
            'wait' : len(goods_all.filter(status_id=1)),
            # 待完成工单数
            'now' : len(goods_all.filter(status_id__in=[3,5])),
            # 已超时工单数
            'timeout' : len(goods_all.filter(status_id=4)),
            # 已完成工单数
            'done' : len(goods_all.filter(status_id=2)),
            # 全部工单数
            'all' : len(goods_all.filter(is_active=True)),
            # 已删除工单数
            'del' : len(goods_all.filter(is_active=False))
        }

        return render(request, 'goods/goods.html', locals())


'''
    ajax 获取工单接口
    method: GET
    url : get_goods/
    参数：
        status : 工单状态
        # start : 开始索引
        # len : 获取长度
        page : 页数
        sort_name : 排序字段名
        sotr_method : 默认升序，若值为'desc'则为降序
        
'''


@check_login
def get_goods(request):
    user = User.objects.get(username=request.session.get('username'))

    goods = Goods.objects.all()
    status = request.GET.get('status')
    sort_name = request.GET.get('sort_name')
    sort_method = request.GET.get('sort_method')
    filter_name = request.GET.get('filter_name')
    filter_val = request.GET.get('filter_val')

    # 过滤
    # 根据状态过滤订单
    if status == '已删除':
        goods = goods.filter(is_active=False)
    elif status == '正在处理':
        goods = goods.filter(is_active=True, status_id__in=[3,5])
    elif status != None and status != 'None':
        goods = goods.filter(status=Status.objects.get(status=status), is_active=True)
    else:
        goods = goods.filter(is_active=True)

    # 排序
    # 根据排序关键字对数据进行排序
    if sort_name != None and sort_name != 'None':
        if sort_method == 'desc':
            goods = goods.order_by('-' + sort_name)
        else:
            goods = goods.order_by("createtime")

    # 搜索
    # 根据 字段值 搜索工单
    if filter_name != None and filter_val != 'None':
        if filter_name == 'username':
            goods = goods.filter(clent_name=filter_val)
        elif filter_name == 'number':
            goods = goods.filter(number=filter_val)
        elif filter_name == 'goods_number':
            goods = goods.filter(wuliu_number=filter_val)

    # 按权限过滤
    # 按照 用户等级 过滤工单
    if user.level == '1' and status != '未处理':
        goods = goods.filter(c_user=user)
    elif user.level == '2':
        goods = goods.filter(t_user=user)

    # 获取分页页数，若没有则显示第一页
    page_num = int(request.GET.get('page', 1))
    # 初始化分页对象，设置每页数据10条
    pa = Paginator(goods, 10)
    # 如果页数超出范围
    if (page_num > pa.num_pages or page_num < 1):
        return HttpResponse('页数超出范围', 404)

    # 获取对应页面对象
    page = pa.page(page_num)

    # 调整工单属性
    if page != None:
        # 将时间单位从 s 转换为 小时
        for i in range(0, len(page)):
            page[i].time = int(page[i].time / 3600);

    # # 输出日志
    # print("用户：", user.username)
    # print("请求参数：", request.GET)
    # print("过滤结果：", page.object_list)

    return render(request, 'goods/filter_goods.html', locals())


'''
    ajax 搜索工单接口
    url : filter_goods/type/val
    
'''


@check_login
def filter_goods(request, f_type, f_val):
    user = User.objects.get(username=request.session.get('username'))

    goods = Goods.objects.all()

    # 按照用户等级过滤工单
    if user.level == '1':
        goods = goods.filter(c_user=user)
    elif user.level == '2':
        goods = goods.filter(t_user=user)

    # 按照搜索条件过滤工单
    if f_type == 'username':
        goods = goods.filter(clent_name=f_val, is_active=True)
    elif f_type == 'number':
        goods = goods.filter(number=f_val, is_active=True)
    elif f_type == 'goods_number':
        goods = goods.filter(wuliu_number=f_val)
    else:
        goods = None

    # 调整工单属性
    if goods != None:
        goods_length = len(goods)
        for item in goods:
            item.time = int(item.time / 3600)

    return render(request, 'goods/filter_goods.html', locals())




'''
    添加工单
    url :  add_goods/
'''


@check_login
def add_goods(request):
    user = User.objects.get(username=request.session.get('username'));

    if request.method == 'GET':
        return render(request, 'goods/add_goods.html', locals())
    elif request.method == 'POST':
        try:
            gnumber = t.strftime('G%Y%m%d%H%M%S', t.localtime())
            cname = request.POST.get('clent_name')
            gname = request.POST.get('goods_name')
            gc = request.POST.get('goods_count')
            gt = request.POST.get('goods_time')
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            other = request.POST.get('other')
            time = request.POST.get('time')
            files = request.FILES.getlist('files')

            # 根据问题类型处理数据
            type = request.POST.get('type')
            if (type == '物流问题'):
                gn = request.POST.get('goods_number')
                goods = Goods.objects.create(clent_name=cname,
                                             number=gnumber,
                                             goods_name=gname,
                                             goods_count=gc,
                                             goods_type=type,
                                             wuliu_number=gn,
                                             buy_date=gt,
                                             title=title,
                                             content=detail,
                                             other=other,
                                             time=time
                                             )
                # 指定创建人员信息
                goods.t_user = user
                # 设置工单状态
                goods.status = Status.objects.get(status="未处理")
                goods.save()
            elif (type == '货物问题'):
                goods = Goods.objects.create(clent_name=cname,
                                             number=gnumber,
                                             goods_name=gname,
                                             goods_count=gc,
                                             goods_type=type,
                                             buy_date=gt,
                                             title=title,
                                             content=detail,
                                             time=time,
                                             other=other)



                # 循环提取上传的文件
                for file in files:
                    isimg = not file.name.split('.')[1] == 'mp4'
                    # 替换文件名中的空格
                    file_name = str(file.name).replace(' ', '_')
                    print(file_name.split('.'))

                    # 存储文件到数据库
                    newf = Files.objects.create(filename=file_name, isimg=isimg, file=file, goods=goods)
                    print("文件名：", str(newf.file))

                    # 压缩图片
                    if isimg:

                        class img_info:
                            def __init__(self, file):
                                self.file = file

                        # 采用异步执行压缩图片
                        def re_img():

                            img = img_info(newf)

                            # 线程锁
                            lock = threading.Lock()
                            lock.acquire()
                            try:
                                # 压缩图片并返回新图片的路径
                                out_path = img_resize.compress_img('media/'+str(img.file.file))
                                print("新文件名：",out_path)
                                # 删除原文件(防止新旧文件名一致误删)
                                if out_path != 'media/'+str(img.file.file):
                                    os.remove('media/'+str(img.file.file))

                                # 将新文件的路径保存至数据库
                                img.file.file = out_path.replace("media/", '')
                                img.file.save()
                            finally:
                                lock.release()

                        # 创建子线程执行图片压缩
                        thr = threading.Thread(target=re_img)
                        thr.start()
                    # 压缩视频
                    else:
                        # 采用异步执行压缩视频
                        def re_vadio():
                            cpv = video_resize.Compress_Pic_or_Video('./media/updataFiles/', newf.filename, "ismin_"+newf.filename)
                            cpv.SaveVideo()
                            # 删除原文件
                            os.remove("media/"+str(newf.file))
                            # 存储新文件到数据库
                            newf.file = 'updataFiles/ismin_'+newf.filename
                            newf.save()

                        # 创建子线程执行视频压缩
                        thr = threading.Thread(target=re_vadio)
                        thr.start()

                goods.t_user = user
                goods.status = Status.objects.get(status="未处理")
                goods.save()
            elif (type == '单号问题'):
                goods = Goods.objects.create(clent_name=cname,
                                             number=gnumber,
                                             goods_name=gname,
                                             goods_count=gc,
                                             goods_type=type,
                                             buy_date=gt,
                                             title=title,
                                             content=detail,
                                             time=time,
                                             other=other)
                goods.t_user = user
                goods.status = Status.objects.get(status="未处理")
                goods.save()

            else:
                return HttpResponse('<script>alert("提交失败，未知的工单问题类型！");location.href = ""</script>')
        except Exception as e:
            print("工单添加失败：\n%s" % sys.exc_info())
            return HttpResponse('<script>alert("提交失败，数据错误！");location.href = ""</script>')
        else:
            return HttpResponse('<script>alert("工单添加成功!");location.href = ""</script>')


'''
    伪删除工单
    url : delete_goods/id
'''


@check_login
def delete_goods(request, id):
    user = User.objects.get(username=request.session.get('username'))

    # 只有管理员能删除工单
    if user.level == '0':
        try:
            good = Goods.objects.get(id=id)
        except:
            return HttpResponse('<script>alert("删除失败,没有这个工单!");location.href = "/goods"</script>')
        else:
            good.is_active = False
            good.status = Status.objects.get(status='已删除')
            good.save()
            return HttpResponse('<script>alert("删除成功!");location.href = "/goods"</script>')
    else:
        return HttpResponse('<script>alert("删除失败,无权限!");location.href = "/goods"</script>')


'''
    真删除工单
    url : real_delete_goods/id
'''


@check_login
def real_delete_goods(request, id):
    user = User.objects.get(username=request.session.get('username'))

    if user.level == '0':
        try:
            good = Goods.objects.get(id=id)
        except:
            return HttpResponse('<script>alert("删除失败,没有这个工单!");location.href = "/goods_all"</script>')
        else:
            try:
                # 先将订单关联的附件删除
                files = good.files_set.all()
                for file in files:
                    os.remove(os.path.join("media", str(file.file)))
            except Exception as e:
                print("工单删除出错：\n%s" % e)

            # 再删除工单
            good.delete()
            return HttpResponse('<script>alert("此订单已被彻底删除!");location.href = "/goods"</script>')
    else:
        return HttpResponse('<script>alert("删除失败,无权限!");location.href = "/goods_all"</script>')


'''
    查看工单详情
        url : check_goods/id
'''


@check_login
def check_goods(request, id):
    if request.method == 'GET':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        try:
            goods = Goods.objects.get(id=id)
            files = goods.files_set.all()
        except:
            return HttpResponse('<script>alert("数据错误，无此工单信息!");location.href = "/goods_all"</script>')

        if user.level == '2' and goods.t_user.username != username:
            return HttpResponse('<script>alert("错误，无权限查看此工单信息!");location.href = "/goods_all"</script>')
        else:
            yq_time = int(goods.time / 3600)
            return render(request, 'goods/check_goods.html', locals())
    else:
        return HttpResponse('<script>alert("错误的请求方式!");location.href = "/goods_all"</script>')


'''
    开始处理工单
        url : start_goods/id
'''


@check_login
def start_goods(request, id):
    try:
        user = User.objects.get(username=request.session.get('username'))
        goods = Goods.objects.get(id=id)
        if user.level == '2':
            return HttpResponse('<script>alert("错误，申报员无权限处理工单!");history.back()</script>')
        elif goods.status.status in ['未处理', '已超时']:
            goods.status = Status.objects.get(status='正在处理')
            goods.c_user = user
            goods.save()
            print('用户%s，开始处理工单：%s' % (user.name, goods.number))
            return HttpResponseRedirect('/check_goods/%s' % goods.id)
        else:
            return HttpResponse('<script>alert("错误，此工单已经在处理中!");history.back()</script>')
    except:
        return HttpResponse('<script>alert("数据错误，无此工单信息!");location.href = "/goods_all"</script>')


'''
    延时订单
        url : add_goods_time/id
'''


@check_login
def add_goods_time(request, id):
    try:
        user = User.objects.get(username=request.session.get('username'))
        goods = Goods.objects.get(id=id)

        if user.level == '2':
            return HttpResponse('<script>alert("错误，申报员无权限处理工单!");history.back()</script>')
        elif goods.status.status not in ['未处理', '处理完成']:
            goods.time = goods.time + 86400
            goods.status = Status.objects.get(status='延时处理')
            goods.save()
            print('用户%s，延时了订单：%s' % (user.name, goods.number))
            return HttpResponse('<script>alert("订单延时成功！");location.href = "/check_goods/%s"</script>' % goods.id)
        else:
            return HttpResponse('<script>alert("错误，未处理或处理完成的订单无法延时。");history.back()</script>')
    except Exception as e:
        print(e)
        return HttpResponse('<script>alert("数据错误，无此工单信息!");location.href = "/goods_all"</script>')


'''
    完成订单
    url : end_goods/id
'''


@check_login
def end_goods(request, id):
    try:
        user = User.objects.get(username=request.session.get('username'))
        goods = Goods.objects.get(id=id)

        if user.level == '2':
            return HttpResponse('<script>alert("错误，申报员无权限处理工单!");history.back()</script>')
        elif goods.status.status not in ['未处理', '处理完成']:
            goods.comment = request.POST.get('comment')
            goods.status = Status.objects.get(status='已处理')
            goods.save()
            print('用户%s，延时了订单：%s' % (user.name, goods.number))
            return HttpResponse('<script>alert("订单处理完成！");location.href = "/check_goods/%s"</script>' % goods.id)
        else:
            return HttpResponse('<script>alert("错误，本单是未处理或处理完成的订单。");history.back()</script>')

    except Exception as e:
        return HttpResponse('<script>alert("数据错误，无此工单信息!");location.href = "/goods_all"</script>')


'''
    下载全部工单单信息为 csv 文件
    url : download_all_goods/
'''


@check_login
def download_all_goods(request):
    import csv
    user = User.objects.get(username=request.session.get('username'))
    if user.level == '0':
        # 设置响应体类型
        response = HttpResponse(content_type='text/csv')
        # 设置响应体文件名
        response['Content-Disposition'] = 'attachment;filename="all_goods.csv"'
        # 查询工单数据
        goods = Goods.objects.filter(is_active=True)
        # 设置数据据写入响应体，生成writer对象
        writer = csv.writer(response)
        # 逐行写入数据
        for good in goods:
            writer.writerow(
                [good.number, good.status, good.createtime, good.c_user, good.endtime, good.t_user, good.time,
                 good.title, good.content])

        return response


'''
    ajax 查询超时工单
    url : search_timeout/
'''


@check_login
def search_timeout_view(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.session.get('username'))
        goods = Goods.objects.filter(is_active=True, status=Status.objects.get(status='已超时'))
        data = {"length": len(goods)}
        return HttpResponse(content=json.dumps(data), content_type='text/json', status=200)
    else:
        return HttpResponse("错误的请求方式",404)