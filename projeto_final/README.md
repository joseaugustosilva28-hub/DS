# Projeto Final – API REST Biblioteca (Flask + SQLite)

API REST completa que gerencia uma **biblioteca**, com duas tabelas relacionadas,
CRUD nas duas, códigos HTTP corretos, rota com JOIN e rotas de filtro.

- **Tema:** Biblioteca
- **Tabela pai:** `autores`
- **Tabela filho:** `livros` (cada livro pertence a um autor)

---

## Tabelas

### `autores` (pai)

| Campo            | Tipo    | Observação                    |
| ---------------- | ------- | ----------------------------- |
| `id`             | INTEGER | PRIMARY KEY AUTOINCREMENT     |
| `nome`           | TEXT    | NOT NULL                      |
| `nacionalidade`  | TEXT    | NOT NULL, padrão "Desconhecida" |
| `ano_nascimento` | INTEGER | opcional                      |

### `livros` (filho)

| Campo      | Tipo    | Observação                                            |
| ---------- | ------- | ----------------------------------------------------- |
| `id`       | INTEGER | PRIMARY KEY AUTOINCREMENT                             |
| `titulo`   | TEXT    | NOT NULL                                              |
| `ano`      | INTEGER | opcional                                              |
| `preco`    | REAL    | NOT NULL, padrão 0                                    |
| `autor_id` | INTEGER | NOT NULL, **FOREIGN KEY → autores(id) ON DELETE CASCADE** |

O relacionamento é 1 autor → N livros. A `FOREIGN KEY` garante que não é possível
cadastrar um livro para um autor que não existe, e o `ON DELETE CASCADE` apaga
automaticamente os livros quando o autor é apagado.

---

## Estrutura de arquivos

```
projeto_final/
├── app.py                  # aplicação Flask: cria o app, registra rotas, sobe o servidor
├── config.py               # caminhos (banco, .sql) e configurações do servidor
├── database.py             # conexão SQLite, helpers de consulta e criação do banco
├── validacao.py            # validação dos dados recebidos (gera os erros 400)
├── requirements.txt        # dependências
├── .gitignore
├── README.md
├── routes/
│   ├── __init__.py         # exporta os Blueprints
│   ├── autores.py          # CRUD do pai + /autores/<id>/livros + /autores/sem-livros
│   └── livros.py           # CRUD do filho + /livros/completos (JOIN) + /livros/busca (LIKE)
├── sql/
│   ├── schema.sql          # CREATE TABLE das duas tabelas + FOREIGN KEY
│   └── seed.sql            # dados de exemplo
└── tests/
    ├── testes.http         # testes para a extensão REST Client do VS Code
    └── testes_curl.sh      # testes automatizados em curl (verifica os códigos HTTP)
```

O banco `biblioteca.db` é criado automaticamente na primeira execução.

---

## Dependências

- Python 3.10 ou superior
- Flask 3.x (`requirements.txt`)
- `sqlite3` (já vem na biblioteca padrão do Python)

---

## Como rodar

```bash
cd projeto_final

# 1) ambiente virtual (opcional, recomendado)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2) instalar dependências
pip install -r requirements.txt

# 3) criar o banco com os dados de exemplo (opcional: também é criado sozinho)
python app.py --init-db

# 4) rodar a API
python app.py
```

A API sobe em `http://127.0.0.1:5000`. Acesse `/` para ver a lista de rotas.

### Como testar

```bash
# opção 1 – script curl (com a API rodando em outro terminal)
bash tests/testes_curl.sh

# opção 2 – abrir tests/testes.http no VS Code (extensão REST Client)
# e clicar em "Send Request" em cada requisição
```

---

## Rotas

### Autores (tabela pai)

| Método | Rota                   | Descrição                                              | Códigos       |
| ------ | ---------------------- | ------------------------------------------------------ | ------------- |
| GET    | `/autores`             | Lista autores + `total_livros` (LEFT JOIN). Filtros opcionais combináveis: `?nome=&nacionalidade=` (LIKE) | 200 |
| GET    | `/autores/<id>`        | Um autor                                               | 200, 404      |
| POST   | `/autores`             | Cria autor                                             | 201, 400      |
| PUT    | `/autores/<id>`        | Atualiza autor                                         | 200, 400, 404 |
| DELETE | `/autores/<id>`        | Apaga autor (e seus livros em cascata)                 | 200, 404      |
| GET    | `/autores/<id>/livros` | **Filtro por caminho:** livros daquele autor           | 200, 404      |
| GET    | `/autores/sem-livros`  | **LEFT JOIN:** autores que não têm nenhum livro        | 200           |

### Livros (tabela filho)

| Método | Rota                 | Descrição                                                | Códigos       |
| ------ | -------------------- | -------------------------------------------------------- | ------------- |
| GET    | `/livros`            | Lista simples de livros                                  | 200           |
| GET    | `/livros/completos`  | **Rota com JOIN:** cada livro com o **nome** do autor     | 200           |
| GET    | `/livros/busca`      | **Busca com LIKE por query string:** `?nome=&autor=&ano_min=&ano_max=&preco_max=` (podem ser combinados) | 200, 400 |
| GET    | `/livros/<id>`       | Um livro (também com JOIN)                                | 200, 404      |
| POST   | `/livros`            | Cria livro (`titulo` e `autor_id` obrigatórios)           | 201, 400      |
| PUT    | `/livros/<id>`       | Atualiza livro                                            | 200, 400, 404 |
| DELETE | `/livros/<id>`       | Apaga livro                                               | 200, 404      |

### Exemplos de corpo JSON

```json
POST /autores
{ "nome": "Jorge Amado", "nacionalidade": "Brasileira", "ano_nascimento": 1912 }

POST /livros
{ "titulo": "Capitaes da Areia", "ano": 1937, "preco": 44.90, "autor_id": 1 }
```

### Exemplos de uso

```bash
curl http://127.0.0.1:5000/livros/completos
curl http://127.0.0.1:5000/autores/1/livros
curl "http://127.0.0.1:5000/livros/busca?nome=casmurro"
curl "http://127.0.0.1:5000/livros/busca?autor=machado&ano_min=1880&preco_max=50"
curl -X POST http://127.0.0.1:5000/autores -H "Content-Type: application/json" \
     -d '{"nome":"Jorge Amado","nacionalidade":"Brasileira"}'
```

---

## Códigos HTTP e segurança

- **200** – consulta, atualização ou remoção com sucesso
- **201** – recurso criado (POST)
- **400** – dados inválidos (campo obrigatório ausente, tipo errado, `autor_id` inexistente, filtro numérico inválido)
- **404** – recurso ou rota não encontrada
- **405** – método HTTP não permitido na rota

Todas as consultas usam **placeholders `?`** no SQL (nunca concatenação de strings),
o que evita **SQL Injection**. Os erros também são retornados em JSON.

---

## Diferenciais implementados

- `ON DELETE CASCADE`: ao apagar um autor, seus livros são apagados e a resposta informa quantos foram (`PRAGMA foreign_keys = ON` é ativado em toda conexão, pois no SQLite as FKs vêm desligadas).
- `LEFT JOIN`: `/autores/sem-livros` lista pais sem filhos e `/autores` mostra a contagem de livros de cada autor.
- Busca com **vários filtros combinados** ao mesmo tempo em `/livros/busca` e em `/autores`.
- SQL do banco separado em arquivos `.sql`, rotas organizadas em Blueprints e script de testes que confere automaticamente os códigos HTTP.

---

## Integrantes

- Integrante 1 – nome completo
- Integrante 2 – nome completo

> Os dois integrantes devem realizar commits no repositório `aulas`, pasta `projeto_final`.
