# -*- coding=utf-8 -*-

from testdjangodb.models import Device
from testdjangodb.forms import DeviceForm
from django.shortcuts import render
from django.http import HttpResponseRedirect


def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把新添加的设备信息写入数据库
        if form.is_valid():
            s1 = Device(name=request.POST.get('name'),
                        ip_address=request.POST.get('ip_address'),
                        ro_community=request.POST.get('ro_community'),
                        rw_community=request.POST.get('rw_community'),
                        username=request.POST.get('username'),
                        password=request.POST.get('password'),
                        enable_password=request.POST.get('enable_password'),
                        device_type=request.POST.get('device_type'))
            s1.save()

            form = DeviceForm()
            return render(request, 'add_device.html', {'form': form,
                                                       'successmessage': '设备添加成功'})

        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            # 如果检查到错误,会添加错误内容到form内,例如:<ul class="errorlist"><li>IP地址已经存在</li></ul>
            return render(request, 'add_device.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 显示表单内容给客户
        form = DeviceForm()
        return render(request, 'add_device.html', {'form': form})


def show_device(request):
    # 查询整个数据库的信息 object.all()
    result = Device.objects.all()
    # 最终得到设备清单devices_list,清单内部是每一个设备信息的字典
    devices_list = []
    for x in result:
        # 产生设备信息的字典
        device_dict = {'id_delete': "/delete_device/" + str(x.id) + "/",
                       'id_edit': "/edit_device/" + str(x.id) + "/",
                       'id': x.id,
                       'name': x.name,
                       'ip_address': x.ip_address,
                       'ro_community': x.ro_community,
                       'rw_community': x.rw_community,
                       'username': x.username,
                       'password': x.password,
                       'enable_password': x.enable_password,
                       'device_type': x.device_type,
                       'create_date': x.create_date}

        # 提取设备详细信息,并写入字典
        devices_list.append(device_dict)
    return render(request, 'show_device.html', {'devices_list': devices_list})


def delete_device(request, id):
    # 获取对应ID的设备
    m = Device.objects.get(id=id)
    # 从数据库中删除学员条目
    m.delete()
    # 成功后重定向到显示所有设备信息页面
    return HttpResponseRedirect('/show_device')

