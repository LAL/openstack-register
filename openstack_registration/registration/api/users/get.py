"""
Provide view that will be call when a uri:/users request will be call
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.decorators import superuser_required, groupadmin_required
from registration.Backend import OpenLdapUserBackend


@superuser_required
def html(request):
    """
    Return the HTML page to display users list

    :param request: Web request
    :return: HTTP rendering
    """
    response = render(request, "users/home.html")
    return response


@groupadmin_required
def json(request):  # pylint: disable=unused-argument
    """
    Provide a list of user. This view can only be called by a superuser. A PermissionDenied
    exception is raised if user is not a superuser

    :param request: Web request
    :return: JSonResponse
    """
    ldap = OpenLdapUserBackend()
    return JsonResponse(ldap.get(), safe=None)
