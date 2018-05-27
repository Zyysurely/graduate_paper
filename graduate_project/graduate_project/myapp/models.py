from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class message(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    Authority = models.BooleanField(default=False)
    # 1是管理员身份


class task(models.Model):
    user = models.ForeignKey(message, null=True, blank=True, on_delete=models.SET_NULL)
    task_id = models.CharField(max_length=20)
    already = models.IntegerField()
    start_date = models.DateTimeField('开始时间', default=timezone.now)
    end_date = models.DateTimeField('结束时间', null=True, blank=True, default=None)
    algorithm = models.CharField(max_length=300, null=True, blank=True, default=None)  # 对应的算法参数
    # 0: 未启动，1：未完成 2：已完成


class dataset(models.Model):
    dataset_name = models.CharField(max_length=20)
    url = models.CharField(max_length=100)    # dataset的路径
