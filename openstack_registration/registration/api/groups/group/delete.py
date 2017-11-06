"""
Provide support for uri://groups/*group* call with **DELETE** HTTP method
"""
from django.http import JsonResponse

from registration.decorators import superuser_required
from registration.Backend.OpenLdap import OpenLdapGroupBackend


@superuser_required
def json(request, group):
    """
    Delete group.

    :param request: Web request
    :param groupname: groupname to delete
    :return: JSonResponse
    """
    ldap = OpenLdapGroupBackend()
    ldap.delete(group)
    return JsonResponse({
        'status': 'success'
    })
