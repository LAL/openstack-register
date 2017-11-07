"""
Provide support for HTTP rendering for request uri://groups
"""
from django.shortcuts import render
from django.http import JsonResponse

from registration.decorators import groupadmin_required
from registration.Backend import OpenLdapGroupBackend


@groupadmin_required
def html(request):
    """
    Return the HTML page to display groups

    :param request: Web request
    :return: HTTP rendering
    """
    response = render(request, "groups/home.html")
    return response


@groupadmin_required
def json(request):  # pylint: disable=unused-argument
    """
    Return JSON list of groups

    :param request: Web request
    :return: HTTP rendering
    """
    ldap = OpenLdapGroupBackend()
    return JsonResponse(ldap.get(), safe=None)
