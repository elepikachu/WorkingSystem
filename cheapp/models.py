from django.db import models


# Create your models here.
class SOFCTest(models.Model):
    id = models.IntegerField('编号', primary_key=True)
    grp = models.IntegerField('实验组', default=0)
    ns = models.IntegerField('电池数量', default=0)
    gas = models.CharField('气体名称', max_length=50, default='H2')
    tmp = models.DecimalField('温度', default=298.15, max_digits=5, decimal_places=2)
    prs = models.IntegerField('压力', default=101325)
    curv = models.DecimalField('输入流量', default=0, max_digits=7, decimal_places=2)
    cure = models.DecimalField('输入电流', default=0, max_digits=5, decimal_places=2)
    vlt = models.DecimalField('输入电压', default=0, max_digits=5, decimal_places=2)
