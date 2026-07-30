# Graph Report - .  (2026-07-29)

## Corpus Check
- Corpus is ~3,558 words - fits in a single context window. You may not need a graph.

## Summary
- 180 nodes · 390 edges · 13 communities
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.82)
- Token cost: 0 input · 57,101 output

## Community Hubs (Navigation)
- Config & Project Docs
- App Bootstrap & Session
- Reviews & Feed
- Authentication
- Games & RAWG Integration
- Follow System
- Migrations & Game Lists
- RAWG API Client

## God Nodes (most connected - your core abstractions)
1. `Game Diary Backend README` - 44 edges
2. `User` - 21 edges
3. `_get_or_cache_game()` - 11 edges
4. `_to_public()` - 10 edges
5. `get_session()` - 9 edges
6. `get_current_user()` - 8 edges
7. `create_review()` - 8 edges
8. `Game` - 8 edges
9. `Review` - 8 edges
10. `login()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `register()` --calls--> `User`  [EXTRACTED]
  backend/app/api/auth.py → backend/app/models/user.py
- `get_current_user()` --references--> `User`  [EXTRACTED]
  backend/app/api/deps.py → backend/app/models/user.py
- `follow_user()` --references--> `User`  [EXTRACTED]
  backend/app/api/follows.py → backend/app/models/user.py
- `unfollow_user()` --references--> `User`  [EXTRACTED]
  backend/app/api/follows.py → backend/app/models/user.py
- `follow_status()` --references--> `User`  [EXTRACTED]
  backend/app/api/follows.py → backend/app/models/user.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Authentication flow (register/login)** — backend_app_api_auth, backend_app_core_security, backend_app_models_user, backend_readme_auth_register, backend_readme_auth_login [INFERRED 0.85]
- **RAWG game data integration** — backend_app_services_rawg_client, backend_app_models_game, backend_app_api_games, backend_readme_rawg_api_key [INFERRED 0.85]
- **Social follow/feed/review flow** — backend_app_models_follow, backend_app_api_follows, backend_app_api_feed, backend_app_models_like, backend_app_api_reviews [INFERRED 0.80]

## Communities (13 total, 0 thin omitted)

### Community 0 - "Config & Project Docs"
Cohesion: 0.07
Nodes (36): alembic/ (DB migrations), Configurações centrais da aplicação. Os valores são lidos automaticamente do…, Settings, Cliente para a API do RAWG (https://rawg.io/apidocs). Autenticação: bem mais…, Game Diary Backend README, Alembic migrations, Proposed: avatar upload via S3-compatible bucket, DATABASE_URL env var (+28 more)

### Community 1 - "App Bootstrap & Session"
Cohesion: 0.12
Nodes (19): get_current_user(), Session, decode_access_token(), Decodifica o token e retorna o subject (id do usuário), ou None se…, get_session(), init_db(), Dependency do FastAPI: entrega uma sessão de banco e garante que ela seja…, Cria as tabelas no banco caso ainda não existam. Em produção prefira usar as… (+11 more)

### Community 2 - "Reviews & Feed"
Cohesion: 0.18
Nodes (22): get_feed(), get, Session, Retorna as reviews mais recentes das pessoas que o usuário atual segue., create_review(), delete_review(), like_review(), list_reviews_for_game() (+14 more)

### Community 3 - "Authentication"
Cohesion: 0.16
Nodes (20): login(), post, Session, register(), create_access_token(), hash_password(), Gera um token JWT. `subject` normalmente é o id do usuário., verify_password() (+12 more)

### Community 4 - "Games & RAWG Integration"
Cohesion: 0.14
Nodes (19): get_game(), _get_or_cache_game(), get, Session, Converte o payload cru do RAWG nos campos do nosso modelo Game., Busca o jogo no cache local; se não existir, cria a partir do payload do RAWG., Busca jogos por nome. Consulta o RAWG e cacheia os resultados localmente., Retorna os detalhes de um jogo. Usa o cache local se já existir, senão busca no… (+11 more)

### Community 5 - "Follow System"
Cohesion: 0.19
Nodes (15): follow_status(), follow_user(), list_followers(), list_following(), delete, get, post, Session (+7 more)

### Community 6 - "Migrations & Game Lists"
Cohesion: 0.23
Nodes (7): GameList, GameListItem, SQLModel, Item dentro de uma GameList, referenciando um jogo., Uma lista criada pelo usuário, ex: 'Jogados em 2026', 'Quero jogar',…, SQLModel, ReviewLike

### Community 7 - "RAWG API Client"
Cohesion: 0.36
Nodes (5): Any, Busca jogos pelo nome., Busca um jogo específico pelo id do RAWG., Lista jogos populares de um determinado gênero (slug do RAWG, ex: "rpg",…, RAWGClient

## Knowledge Gaps
- **10 isolated node(s):** `Config`, `Config`, `Config`, `RAWG API (game data provider)`, `Flutter client (API consumer)` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Game Diary Backend README` connect `Config & Project Docs` to `App Bootstrap & Session`, `Reviews & Feed`, `Authentication`, `Games & RAWG Integration`, `Follow System`, `Migrations & Game Lists`?**
  _High betweenness centrality (0.347) - this node is a cross-community bridge._
- **Why does `User` connect `Reviews & Feed` to `App Bootstrap & Session`, `Authentication`, `Games & RAWG Integration`, `Follow System`, `Migrations & Game Lists`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `RAWGClient` connect `RAWG API Client` to `Config & Project Docs`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **What connects `Config`, `Config`, `Config` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Config & Project Docs` be split into smaller, more focused modules?**
  _Cohesion score 0.06612685560053981 - nodes in this community are weakly interconnected._
- **Should `App Bootstrap & Session` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._
- **Should `Games & RAWG Integration` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._