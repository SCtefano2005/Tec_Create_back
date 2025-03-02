from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_view(self, request, *args, **kwargs):
        return redirect("/accounts/google/login/?process=login")
