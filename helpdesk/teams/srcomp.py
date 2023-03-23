"""A basic client for SRComp HTTP."""
from __future__ import annotations

from json import JSONDecodeError
from typing import Any, NamedTuple

import requests
from cachetools import TTLCache, cached
from django.conf import settings


class ScoreInfo(NamedTuple):

    league_pos: int
    game_score: int
    league_score: int


class SRComp:

    def __init__(self, *, base_url: str | None = None) -> None:
        self._base_url = base_url or settings.SRCOMP_HTTP_BASE_URL

    def _get(self, endpoint: str) -> dict[str, Any] | None:
        try:
            resp = requests.get(f"{self._base_url}/{endpoint}", timeout=1)
            resp.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        except ConnectionError:
            return None
    
        try:
            return resp.json()
        except JSONDecodeError:
            return None

    @cached(cache=TTLCache(maxsize=40, ttl=180))
    def get_score_info_for_team(self, tla: str) -> ScoreInfo | None:
        if not self._base_url:
            return None
        
        if data := self._get(f"teams/{tla}"):
            return ScoreInfo(
                league_pos=data.get("league_pos"),  # type: ignore[arg-type]
                game_score=data.get("scores", {}).get("game"),
                league_score=data.get("scores", {}).get("league"),
            )
        return None

srcomp = SRComp()
