from django.db import models
from django.utils import timezone


class Device(models.Model):
    # 名字,最大长度50,不能为空 (注意:并没有min_length这个控制字段)
    name = models.CharField(max_length=50, blank=False)

    # IP地址, 唯一键
    ip_address = models.GenericIPAddressField(blank=False, unique=True)

    # 只读Community,不能为空
    ro_community = models.CharField(max_length=50, blank=False)

    # 读写Community,可以为空
    rw_community = models.CharField(max_length=50, blank=True, null=True)

    # SSH用户名,不能为空
    username = models.CharField(max_length=50, blank=True, null=False)

    # SSH密码,可以为空
    password = models.CharField(max_length=50, blank=True, null=True)

    # enable密码,可以为空
    enable_password = models.CharField(max_length=50, blank=True, null=True)

    # 设备类型
    device_type_choices = (('firewall', 'firewall'), ('Router', 'Router'), ('Switch', 'Switch'))
    device_type = models.CharField(max_length=10, choices=device_type_choices)

    # 创建日期,自动添加日期项
    create_date = models.DateTimeField(auto_now_add=True)
    # create_date = timezone.now()

