# -*- coding=utf-8 -*-

from django.shortcuts import render
from testdjangodb.models import UploadFile, Ospath
import hashlib
import os
from django.http import StreamingHttpResponse
from django.utils.http import urlquote

file_os_path = Ospath.objects.get(id=1).upload_file_path


def upload(request):
    if request.method == 'POST':  # 如果请求method为POST, 上传文件都是用POST
        messages = []  # 由于并不是所有的文件都能成功上传, 所以这里做了一个给客户回显每一个文件上传状态信息的清单messages
        files_list = request.FILES.getlist('files[]')  # 得到多个文件的清单
        for file in files_list:
            # file.name 文件名
            # file.content_type 文件类型
            # file.size 文件大小(可以考虑对文件大小进行限制)

            # 通过测试发现doc和docx的文件类型都是"application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # 把此文件的错误信息, 放入messages清单, 并使用continue跳过此文件
                messages.append(file.name + ":文件格式并不是doc或者docx!")
                continue

            # 读取二进制数据
            bit_file = file.file.read()
            # 产生HASH,用HASH作为写入OS的文件名
            file_hash_name = hashlib.sha3_256(bit_file).hexdigest()
            # 获取上传文件的文件名
            upload_file_name = file.name
            # 获取上传文件的扩展名
            upload_file_name_ext = os.path.splitext(upload_file_name)[1]
            # 写入OS的文件名, HASH 加上 上传文件的扩展名
            os_filename = file_hash_name + upload_file_name_ext
            # 写入文件
            checked_file = open(file_os_path + os_filename, 'wb')
            checked_file.write(bit_file)
            checked_file.close()

            # 保存到数据库
            s = UploadFile(upload_filename=upload_file_name,
                           os_filename=os_filename)
            s.save()
            messages.append(upload_file_name + ":上传成功!")
        return render(request, 'file_mgmt.html', {'messages': messages})

    else:  # 如果不是POST,就是GET,表示为初始访问, 显示表单内容给客户
        return render(request, 'file_mgmt.html')


def download(request, id):
    uploadfile = UploadFile.objects.get(id=id)
    uploadfile_bitfile = open(file_os_path + uploadfile.os_filename, 'rb')
    response = StreamingHttpResponse(uploadfile_bitfile)
    response['Content-Type'] = 'application/octet-stream'
    # 使用urlquote解决中文文件名问题, 是否火狐依然有问题
    response['Content-Disposition'] = 'attachment; filename={0}'.format(urlquote(uploadfile.upload_filename))
    return response

