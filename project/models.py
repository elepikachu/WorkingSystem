from django.db import models


class Project(models.Model):
    id = models.IntegerField('项目编号', primary_key=True)
    name = models.CharField('项目名称', max_length=50, default='')
    date = models.DateField('起始时间')
    enddate = models.DateField('完成时间')
    group = models.CharField('项目组名称', max_length=50, default='')
    person = models.CharField('完成人', max_length=50, default='')
    classification = models.CharField('项目类别', max_length=20, default='')
    detail = models.CharField('项目备注', max_length=100, default='')
    finish = models.IntegerField('是否完成', default=0)


class ProjectLog(models.Model):
    id = models.IntegerField('操作编号', primary_key=True)
    ip = models.CharField('操作ip', max_length=50, default='')
    date = models.DateTimeField('操作时间')
    cmd = models.CharField('操作类型', max_length=50, default='')
    other = models.CharField('备注', max_length=70, default='')


