from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.test import Client

    from accounts.models import User


def test_authentication_required(client: Client) -> None:
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp['Location'] == '/auth/login/?next=/'


def test_landing_page_redirects(client: Client, admin_user: User) -> None:
    client.force_login(admin_user)
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp['Location'] == '/accounts/onboarding/'
