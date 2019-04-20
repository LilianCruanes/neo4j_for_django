from neo4j_for_django.contrib.auth.authentication import get_user_is_logged, get_user_from_request
from neo4j_for_django.contrib.auth.node_models import AnonymousUser
from django.conf import settings
from django.shortcuts import redirect, render


def login_required(function=None, login_page_url=settings.N4D_LOGIN_URL):
    """
    If the user is logged, execute the decorated view, else redirect to 'login_page_url

    :param login_page_url: The page to which one redirect the user if it is not logged.
    """

    def wrapped_function(request, *args, **kwargs):
        if get_user_is_logged(request):
            return function(request, *args, **kwargs)
        else:
            return redirect(login_page_url, permanent=True)

    return wrapped_function


def protect_authentication_view(function=None, home_page_url=settings.N4D_HOME_PAGE_URL):
    """
    If the user is already logged, the login view (and the page that it sent), is not accessible, the decorator
    automatically redirect the user to the home page.

    :param home_page_url: The url of the home page (ex: '/blog/home/')
    """
    def wrapped_function(request, *args, **kwargs):
        if get_user_is_logged(request):
            return redirect(home_page_url, permanent=True)
        else:
            return function(request, *args, **kwargs)

    return wrapped_function


def permission_required(permission_codename, if_false_html=None, if_false_url=settings.N4D_HOME_PAGE_URL):
    """
    If the user has the permission, execute the decorated view, else redirect to 'if_false_url'.

    :param permission_codename: The codename of the permission.
    :param if_false_url: The url of the page to which one redirect the user, if the user doesn't have the
            permission
    """
    def decorator(function):

        def wrapped_function(request, *args, **kwargs):
            user = get_user_from_request(request)

            if not isinstance(user, AnonymousUser):
                if isinstance(permission_codename, str):
                    if user.has_perm(permission_codename):
                        return function(request, *args, **kwargs)
                    else:
                        if if_false_html is not None:
                            return render(request, if_false_html)
                        else:
                            return redirect(if_false_url)

        return wrapped_function
    return decorator
