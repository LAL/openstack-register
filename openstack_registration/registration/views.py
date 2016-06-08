#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from openstack_registration.settings import LOGIN_REDIRECT_URL, GLOBAL_CONFIG
from Backend import OpenLdap
from utils import *


def login(request):
    """

    :param request:
    :return:
    """

    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'].lower(),
                                 password=request.POST['password'])
        if user is not None:
            redirect_page = "users/{}".format(request.POST['username'].lower())
            auth.login(request, user)
            return HttpResponseRedirect(redirect_page)
        else:
            return render(request, "login.html")
    else:
        return render(request, "login.html")


@login_required()
def user_dispatcher(request,
                    username):
    if request.method == 'GET'\
            and 'format' in request.GET\
            and request.GET['format'] == 'json':
        return user_get_json(request,
                             username)
    elif request.method == 'GET':
        return render(request, 'user_get_html.html')


@login_required()
def user_get_html(request):
    return render(request, 'user_get_html.html')


@login_required()
def user_get_json(request,
                  username):
    data = {}
    ldap = OpenLdap(GLOBAL_CONFIG)
    attrs = ldap.search_user(attributes=username)
    print attrs
    # attrs = attrs[0][1]
    for key, value in attrs:
        for each in value:
            data[each] = value[each]
    return JsonResponse(data)


def home_get_html(request):
    """

    :param request:
    :return:
    """
    return render(request, 'home_get_html.html')


def policies_get_html(request):
    """

    :param request:
    :return:
    """
    return render(request, 'policies_get_html.html')


def register_dispatcher(request):
    if 'format' in request.GET:
        if 'adduser' in request.GET:
            attributes = QueryDict(request.body).dict()
            # print type(attributes['password'])
            # print attributes['password']
            add_user(request, attributes)
            return JsonResponse(attributes)
    else:
        return render(request, 'register_get_html.html')


def attributes_dispatcher(request):
    attributes = {}
    if 'password' in request.GET:
        password = request.GET['password']
        attributes = check_password_constraints(password)
        return JsonResponse(attributes)

    ### TEST ###
    elif 'passwords' in request.GET:
        password = request.GET['passwords']
        attributes['password'] = encode_password(password)
        print type(password)
        print password
        print type(attributes['password'])
        print attributes['password']
        return JsonResponse(attributes)
    ### END ###

    elif 'uid' in request.GET:
        ldap = OpenLdap(GLOBAL_CONFIG)
        uid = normalize_string(request.GET['uid'])
        checked = ldap.search_user(uid=uid)
        attributes['uid'] = uid

        if checked:
            attributes['status'] = 'fail'
        else:
            attributes['status'] = 'success'
        return JsonResponse(attributes)

    elif 'mail' in request.GET:
        ldap = OpenLdap(GLOBAL_CONFIG)
        mail = request.GET['mail']
        checked = ldap.search_user(mail=mail)

        if checked:
            attributes['status'] = 'fail'
        else:
            attributes['status'] = 'success'
        return JsonResponse(attributes)


def add_user(request,
             attributes):
    ldap = OpenLdap(GLOBAL_CONFIG)
    username = str(attributes['username'])
    email = str(attributes['email'])
    firstname = str(attributes['firstname'])
    lastname = str(attributes['lastname'])
    password = encode_password(attributes['password'])

    ldap.add_user(username, email, firstname, lastname, password)
    send_mail(username,email,'', 'add')

def activate_user(request):
    uuid = request.path.split('/action/')
    uuid.pop(0)
    uuid = str(uuid[0])
    ldap = OpenLdap(GLOBAL_CONFIG)
    info = {}
    try :
        attrs = ldap.enable_user(uuid)
        send_mail(attrs['username'], attrs['mail'], '', 'enable')
    except:
        info['info'] = 'Your account is already enable or the url is not ' \
                          'valid, please check your mailbox.'
        return render(request, 'error_get_html.html', context=info)
    return render(request, 'home_get_html.html')