# Game Diary — Backend

Backend do app estilo Letterboxd para jogos. Feito com FastAPI + SQLModel (Postgres) +
integração com o RAWG para dados dos jogos.

## Estrutura

```
app/
├── main.py                  # ponto de entrada da API
├── core/
│   ├── config.py             # configurações lidas do .env
│   └── security.py           # hash de senha e JWT
├── models/                   # tabelas do banco (SQLModel)
│   ├── user.py
│   ├── game.py                # cache local dos jogos do RAWG
│   ├── review.py
│   ├── follow.py
│   ├── game_list.py
│   └── like.py
├── schemas/                  # validação de entrada/saída (Pydantic)
├── services/
│   └── rawg_client.py         # integração com a API do RAWG
├── api/
│   ├── auth.py                # cadastro / login
│   ├── games.py                # busca e cache de jogos
│   ├── reviews.py              # avaliações, curtidas
│   ├── follows.py              # seguir / deixar de seguir
│   ├── feed.py                  # feed de quem você segue
│   └── recommendations.py      # sugestões por gênero
└── db/
    └── session.py             # conexão com o banco
alembic/                      # migrations do banco
```

## Como rodar localmente

1. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Copie o arquivo de variáveis de ambiente e preencha:

```bash
cp .env.example .env
```

- `DATABASE_URL`: aponte para um Postgres local (ex: rode um via Docker, veja abaixo).
- `SECRET_KEY`: gere uma chave aleatória (ex: `openssl rand -hex 32`).
- `RAWG_API_KEY`: deixe vazio até você gerar sua chave em
  https://rawg.io/apidocs. As rotas de jogos vão retornar erro 503 até essa
  credencial ser preenchida — todo o resto da API (auth, follows) funciona
  normalmente sem ela.

3. Suba um Postgres rapidamente com Docker (opcional, se não tiver um instalado):

```bash
docker run --name game-diary-db -e POSTGRES_PASSWORD=senha -e POSTGRES_DB=game_diary -p 5432:5432 -d postgres:16
```

Ajuste a `DATABASE_URL` no `.env` para bater com esses dados.

4. Rode a aplicação:

```bash
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. A documentação interativa (Swagger)
fica automaticamente em `http://localhost:8000/docs` — muito útil para testar
os endpoints antes de integrar com o Flutter.

## Obtendo a credencial do RAWG (quando for a hora)

1. Crie uma conta em https://rawg.io/login
2. Acesse https://rawg.io/apidocs e gere sua API key gratuita
3. Cole no `.env` como `RAWG_API_KEY`

Nenhuma outra mudança de código é necessária — o `rawg_client.py` já lida
com a autenticação (bem mais simples que a do IGDB: é só uma chave, sem OAuth)
automaticamente a partir dessa variável.

Vale saber: a versão gratuita do RAWG tem um limite de requisições mensais
(hoje na casa de 20 mil/mês) — mais do que suficiente para desenvolvimento e
os primeiros usuários, mas fique de olho se o app crescer.

## Migrations (Alembic)

Depois de mexer nos modelos, gere e aplique uma migration:

```bash
alembic revision --autogenerate -m "descrição da mudança"
alembic upgrade head
```

(Em desenvolvimento, `init_db()` no startup já cria as tabelas automaticamente
via SQLModel, então as migrations só passam a importar de fato quando o
banco já tiver dados reais que você precisa preservar.)

## Principais endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/register` | Cadastro |
| POST | `/auth/login` | Login (retorna JWT) |
| GET | `/games/search?q=` | Busca jogos (RAWG + cache) |
| GET | `/games/{rawg_id}` | Detalhe de um jogo |
| POST | `/reviews` | Criar review/avaliação |
| GET | `/reviews/game/{rawg_id}` | Reviews de um jogo |
| POST | `/reviews/{id}/like` | Curtir uma review |
| POST | `/users/{id}/follow` | Seguir um usuário |
| GET | `/feed` | Feed de quem você segue |
| GET | `/recommendations` | Sugestões por gênero |

## Próximos passos sugeridos

- Popular o campo de gênero no cache do `Game` com o `slug` do RAWG (hoje
  só guardamos o nome), para deixar `/recommendations` mais preciso — o
  RAWG filtra jogos por gênero usando slug (ex: "action"), não pelo nome exibido.
- Paginação nos endpoints de listagem (`/feed`, `/reviews/game/{id}`, etc).
- Upload de avatar (ex: usando um bucket S3-compatible).
- Rate limiting nas rotas públicas.
- Testes automatizados (pytest + banco de teste).
