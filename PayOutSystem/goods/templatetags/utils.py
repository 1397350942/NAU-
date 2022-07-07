from django import template

register = template.Library()

@register.filter()
def rows(row,page):
    '''
    自定义模板函数，根据行号和页数计算当前行的序号。

    :param row: 行号，从1开始
    :param page: 页数，从1开始
    :return: (page-1)*10+row
    '''
    return (page-1)*10+row