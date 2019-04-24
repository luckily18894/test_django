# -*- coding=utf-8 -*-

from datetime import datetime
from testdjangodb.models import Device
from testdjangodb.forms import DeviceForm, EditDeviceForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required


@permission_required('testdjangodb.add_device')
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


@permission_required('testdjangodb.view_device')
def show_device(request):
    # 查询整个数据库的信息 object.all()
    result = Device.objects.all()
    # 最终得到设备清单devices_list,清单内部是每一个设备信息的字典
    devices_list = []
    for x in result:
        # 产生设备信息的字典
        device_dict = {'id_delete': "/delete_device/" + str(x.id),
                       'id_edit': "/edit_device/" + str(x.id),
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


def get_device_info(id):
    # 设置过滤条件,获取特定设备信息, objects.get(id=id)
    result = Device.objects.get(id=id)
    device_dict = {}
    device_dict['id'] = result.id
    device_dict['name'] = result.name
    device_dict['ip_address'] = result.ip_address
    device_dict['ro_community'] = result.ro_community
    device_dict['rw_community'] = result.rw_community
    device_dict['username'] = result.username
    device_dict['password'] = result.password
    device_dict['enable_password'] = result.enable_password
    device_dict['device_type'] = result.device_type
    device_dict['create_date'] = result.create_date
    # 返回特定设备详细信息
    return device_dict


@permission_required('testdjangodb.change_device')
def edit_device(request, id):
    # 首先获取特定ID设备的详细信息
    infodict = get_device_info(id)
    if request.method == 'POST':
        form = EditDeviceForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把修改过的设备信息写入数据库
        if form.is_valid():
            m = Device.objects.get(id=id)
            m.name = request.POST.get('name')
            m.ip_address = request.POST.get('ip_address')
            m.ro_community = request.POST.get('ro_community')
            m.rw_community = request.POST.get('rw_community')
            m.username = request.POST.get('username')
            m.password = request.POST.get('password')
            m.enable_password = request.POST.get('enable_password')
            m.device_type = request.POST.get('device_type')
            m.create_date = datetime.now()  # 最后修改时间
            m.save()

            # 写入成功后,提示修改成功
            return render(request, 'edit_device.html', {'form': form,
                                                        'successmessage': '设备修改成功'})
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'edit_device.html', {'form': form})

    else:  # 如果不是POST,就是GET,表示为初始访问, 把特定ID客户在数据库中的值,通过初始值的方式展现给客户看
        form = EditDeviceForm(initial={'id': infodict['id'],  # initial填写初始值
                                       'name': infodict['name'],
                                       'ip_address': infodict['ip_address'],
                                       'ro_community': infodict['ro_community'],
                                       'rw_community': infodict['rw_community'],
                                       'username': infodict['username'],
                                       'password': infodict['password'],
                                       'enable_password': infodict['enable_password'],
                                       'device_type': infodict['device_type']})

        # 将自动填写好的表单呈现出来
        return render(request, 'edit_device.html', {'form': form})


@permission_required('testdjangodb.delete_device')
def delete_device(request, id):
    # 获取对应ID的设备
    m = Device.objects.get(id=id)
    # 从数据库中删除学员条目
    m.delete()
    # 成功后重定向到显示所有设备信息页面
    # return HttpResponseRedirect('/show_device')
    return render(request, 'show_device.html', {'successmessage': '设备删除成功'})


if __name__ == '__main__':
    get_device_info(4)



