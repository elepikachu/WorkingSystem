from django.db import models


class Item(models.Model):
    id = models.IntegerField('编号', primary_key=True)
    good = models.CharField('商品名称', max_length=50, default='')
    brand = models.CharField('品牌型号', max_length=50, default='')
    unit = models.CharField('单位', max_length=5, default=0)
    quantity = models.IntegerField('数量', default=0)
    name = models.CharField('姓名', max_length=50, default='')
    phone = models.CharField('联系电话', max_length=50, default='')
    num = models.CharField('课题编号', max_length=50, default='')
    info = models.CharField('采购说明', max_length=20, default='')
    detail = models.CharField('商品编号', max_length=100, default='')
    group = models.CharField('单位全称', max_length=50, default='')
    classif = models.CharField('物资分类', max_length=30, default='')
    company = models.CharField('公司', max_length=50, default='')
    date = models.DateField('提交日期')
    finish = models.BooleanField('是否完成', default=0)


class ItemLog(models.Model):
    id = models.IntegerField('操作编号', primary_key=True)
    ip = models.CharField('操作ip', max_length=50, default='')
    date = models.DateTimeField('操作时间')
    cmd = models.CharField('操作类型', max_length=50, default='')
    other = models.CharField('备注', max_length=70, default='')


class Suggestion(models.Model):
    id = models.IntegerField('建议编号', primary_key=True)
    ip = models.CharField('操作ip', max_length=50, default='')
    date = models.DateTimeField('提出时间')
    type = models.CharField('建议类型', max_length=30, default='')
    detail = models.CharField('建议', max_length=500, default='')
    finish = models.BooleanField('是否完成', default=False)