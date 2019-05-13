import uuid
from datetime import datetime
from functools import wraps

from django.http import HttpResponseRedirect
from django.urls import reverse

from user.models import Token


def get_token():
    token = uuid.uuid4().hex
    return token


def is_login(func):
    @wraps(func)
    def check(request, *args, **kwargs):
        token = request.COOKIES.get('token')
        my_token = Token.objects.filter(token=token).first()
        if not my_token:
            return HttpResponseRedirect(reverse('user:login'))
        if my_token.out_time.replace(tzinfo=None) < datetime.utcnow():
            return HttpResponseRedirect(reverse('user:login'))
        return func(request, *args, **kwargs)
    return check
