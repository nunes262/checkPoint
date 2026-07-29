"""
Cliente para a API do RAWG (https://rawg.io/apidocs).

Autenticação: bem mais simples que o IGDB — o RAWG usa uma única API key
enviada como query param (`key=`) em cada chamada. Não tem OAuth, não expira.

Como obter a chave:
1. Crie uma conta em https://rawg.io/login
2. Acesse https://rawg.io/apidocs e gere sua API key gratuita
3. Cole em RAWG_API_KEY no seu .env

IMPORTANTE: enquanto RAWG_API_KEY não estiver preenchida, as chamadas
deste cliente vão levantar RuntimeError — as rotas tratam isso e retornam
503 pro cliente da API.
"""

from typing import Any, Optional

import httpx

from app.core.config import settings

RAWG_BASE_URL = "https://api.rawg.io/api"


class RAWGClient:
    def _require_key(self) -> str:
        if not settings.rawg_api_key:
            raise RuntimeError(
                "RAWG_API_KEY não configurada no .env. "
                "Gere uma chave gratuita em https://rawg.io/apidocs e preencha essa variável."
            )
        return settings.rawg_api_key

    async def search_games(self, search_term: str, limit: int = 20) -> list[dict[str, Any]]:
        """
        Busca jogos pelo nome.
        """
        key = self._require_key()
        params = {
            "key": key,
            "search": search_term,
            "page_size": limit,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{RAWG_BASE_URL}/games", params=params)
            response.raise_for_status()
            return response.json().get("results", [])

    async def get_game_by_id(self, rawg_id: int) -> Optional[dict[str, Any]]:
        """
        Busca um jogo específico pelo id do RAWG.
        """
        key = self._require_key()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{RAWG_BASE_URL}/games/{rawg_id}", params={"key": key}
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()

    async def get_games_by_genre(self, genre_slug: str, limit: int = 20) -> list[dict[str, Any]]:
        """
        Lista jogos populares de um determinado gênero (slug do RAWG, ex: "rpg", "action").
        Útil para as recomendações "jogos parecidos com os que você segue/avaliou".
        """
        key = self._require_key()
        params = {
            "key": key,
            "genres": genre_slug,
            "ordering": "-rating",
            "page_size": limit,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{RAWG_BASE_URL}/games", params=params)
            response.raise_for_status()
            return response.json().get("results", [])


# instância única reutilizada pela aplicação
rawg_client = RAWGClient()
