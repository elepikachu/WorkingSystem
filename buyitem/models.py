from django.db import models

# Create your models here.
from django.db import models


class Item(models.Model):
    id = models.IntegerField('编号', primary_key=True)
    name = models.CharField('姓名', max_length=50, default='')
    group = models.CharField('单位全称', max_length=50, default='')
    phone = models.CharField('联系电话', max_length=50, default='')
    num = models.CharField('课题编号', max_length=50, default='')
    good = models.CharField('商品名称', max_length=50, default='')
    brand = models.CharField('品牌型号', max_length=50, default='')
    quantity = models.IntegerField('数量', default=0)
    unit = models.IntegerField('单位', default=0)
    info = models.CharField('采购说明', max_length=20, default='')
    detail = models.CharField('商品编号', max_length=100, default='')
    finish = models.BooleanField('是否完成', default=0)


class ItemLog(models.Model):
    id = models.IntegerField('操作编号', primary_key=True)
    ip = models.CharField('操作ip', max_length=50, default='')
    date = models.DateTimeField('操作时间')
    cmd = models.CharField('操作类型', max_length=50, default='')
    other = models.CharField('备注', max_length=70, default='')
