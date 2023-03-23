from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpRequest
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest) -> bool:
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        if request.path.rstrip("/") == reverse("account_signup").rstrip("/"):
            return False
        return True

