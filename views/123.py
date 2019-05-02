# -*- coding=utf-8 -*-

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_django.settings')
django.setup()


from testdjangodb.models import Ospath


des = Ospath(upload_file_path='/root/test_django/UploadFile')
des.save()
Ospath(upload_file_path='/UploadFile').save()


if __name__ == '__main__':
    pass


