from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pytest_django.asserts import assertContains

from core.models import NavigationLink
from core.templatetags.navigation import STATIC_LINKS

if TYPE_CHECKING:
    from django.test import Client

    from accounts.models import User


def test_authentication_required(client: Client) -> None:
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp["Location"] == "/auth/login/?next=/"


def test_landing_page_redirects(client: Client, admin_user: User) -> None:
    client.force_login(admin_user)
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp["Location"] == "/accounts/onboarding/"


def test_onboarding(client: Client, admin_user: User) -> None:
    client.force_login(admin_user)
    resp = client.get("/accounts/onboarding/")
    assert resp.status_code == 200


@pytest.mark.parametrize("link", STATIC_LINKS)
def test_static_links(client: Client, admin_user: User, link: NavigationLink) -> None:
    client.force_login(admin_user)
    resp = client.get("/accounts/onboarding/")

    assertContains(resp, link.url)
    assertContains(resp, link.name)
