### =========================================================
### Testes da API Biblioteca (Flask + SQLite)
### Use a extensao "REST Client" do VS Code e clique em "Send Request".
### Servidor: python app.py
### =========================================================

@base = http://127.0.0.1:5000

### 0) Documentacao rapida da API (200)
GET {{base}}/


### =========================================================
### AUTORES (tabela pai) - CRUD
### =========================================================

### 1) Listar todos os autores (200) - inclui total_livros (LEFT JOIN)
GET {{base}}/autores

### 2) Listar autores com filtros combinados por query string (200)
GET {{base}}/autores?nome=machado&nacionalidade=brasil

### 3) Obter um autor existente (200)
GET {{base}}/autores/1

### 4) Obter autor inexistente (404)
GET {{base}}/autores/999

### 5) Criar autor (201)
POST {{base}}/autores
Content-Type: application/json

{
  "nome": "Jorge Amado",
  "nacionalidade": "Brasileira",
  "ano_nascimento": 1912
}

### 6) Criar autor sem o campo nome (400)
POST {{base}}/autores
Content-Type: application/json

{
  "nacionalidade": "Brasileira"
}

### 7) Criar autor com ano_nascimento invalido (400)
POST {{base}}/autores
Content-Type: application/json

{
  "nome": "Autor Teste",
  "ano_nascimento": "mil e novecentos"
}

### 8) Atualizar autor (200)
PUT {{base}}/autores/1
Content-Type: application/json

{
  "nome": "Machado de Assis",
  "nacionalidade": "Brasileira",
  "ano_nascimento": 1839
}

### 9) Atualizar autor inexistente (404)
PUT {{base}}/autores/999
Content-Type: application/json

{
  "nome": "Nao Existe"
}

### 10) Autores sem livros - LEFT JOIN (200)
GET {{base}}/autores/sem-livros


### =========================================================
### FILTRO POR CAMINHO: livros de um autor
### =========================================================

### 11) Livros do autor 1 (200)
GET {{base}}/autores/1/livros

### 12) Livros de autor inexistente (404)
GET {{base}}/autores/999/livros


### =========================================================
### LIVROS (tabela filho) - CRUD
### =========================================================

### 13) Listar livros (200)
GET {{base}}/livros

### 14) ROTA COM JOIN: livros com o nome do autor (200)
GET {{base}}/livros/completos

### 15) Obter um livro pelo id, com JOIN (200)
GET {{base}}/livros/1

### 16) Obter livro inexistente (404)
GET {{base}}/livros/999

### 17) Criar livro (201)
POST {{base}}/livros
Content-Type: application/json

{
  "titulo": "Capitaes da Areia",
  "ano": 1937,
  "preco": 44.90,
  "autor_id": 1
}

### 18) Criar livro sem titulo (400)
POST {{base}}/livros
Content-Type: application/json

{
  "ano": 2020,
  "autor_id": 1
}

### 19) Criar livro com autor_id inexistente (400)
POST {{base}}/livros
Content-Type: application/json

{
  "titulo": "Livro Orfao",
  "autor_id": 999
}

### 20) Atualizar livro (200)
PUT {{base}}/livros/1
Content-Type: application/json

{
  "titulo": "Dom Casmurro - Edicao Especial",
  "preco": 59.90
}

### 21) Atualizar livro inexistente (404)
PUT {{base}}/livros/999
Content-Type: application/json

{
  "titulo": "Nao Existe"
}


### =========================================================
### BUSCA POR QUERY STRING COM LIKE
### =========================================================

### 22) Busca por parte do titulo (200)
GET {{base}}/livros/busca?nome=casmurro

### 23) Busca por parte do nome do autor (200)
GET {{base}}/livros/busca?autor=orwell

### 24) Busca com varios filtros ao mesmo tempo (200)
GET {{base}}/livros/busca?nome=a&autor=machado&ano_min=1880&ano_max=1900&preco_max=60

### 25) Busca com filtro numerico invalido (400)
GET {{base}}/livros/busca?ano_min=abc


### =========================================================
### DELETE
### =========================================================

### 26) Apagar um livro (200)
DELETE {{base}}/livros/3

### 27) Apagar livro inexistente (404)
DELETE {{base}}/livros/999

### 28) Apagar autor COM livros - ON DELETE CASCADE (200)
DELETE {{base}}/autores/2

### 29) Confirmar que os livros do autor 2 foram apagados em cascata (200 - lista vazia)
GET {{base}}/livros/busca?autor=clarice

### 30) Apagar autor inexistente (404)
DELETE {{base}}/autores/999

### 31) Metodo nao permitido na rota (405)
DELETE {{base}}/autores
