from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if request.path.rstrip("/") == reverse("account_signup").rstrip("/"):
            return False
        return True


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def validate_disconnect(self, account, accounts):
        raise ValidationError("Can not disconnect")
