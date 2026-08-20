#!/usr/bin/env bash
# =========================================================
# Testes da API Biblioteca com curl.
# Antes de rodar, em outro terminal:  python app.py
#
# Uso:  bash tests/testes_curl.sh
# Cada teste mostra o codigo HTTP esperado e o obtido.
# =========================================================

BASE="http://127.0.0.1:5000"
OK=0
FALHOU=0

# testar <descricao> <codigo_esperado> <metodo> <caminho> [corpo_json]
testar() {
    local descricao="$1" esperado="$2" metodo="$3" caminho="$4" corpo="$5"

    if [ -n "$corpo" ]; then
        resposta=$(curl -s -w "\n%{http_code}" -X "$metodo" "$BASE$caminho" \
            -H "Content-Type: application/json" -d "$corpo")
    else
        resposta=$(curl -s -w "\n%{http_code}" -X "$metodo" "$BASE$caminho")
    fi

    codigo=$(echo "$resposta" | tail -n 1)
    corpo_resposta=$(echo "$resposta" | sed '$d')

    if [ "$codigo" = "$esperado" ]; then
        echo "[OK]    $metodo $caminho -> $codigo | $descricao"
        OK=$((OK + 1))
    else
        echo "[FALHA] $metodo $caminho -> $codigo (esperado $esperado) | $descricao"
        FALHOU=$((FALHOU + 1))
    fi
    echo "        $corpo_resposta"
}

echo "=== Documentacao ==="
testar "rota inicial" 200 GET "/"

echo
echo "=== CRUD AUTORES (tabela pai) ==="
testar "listar autores"                    200 GET    "/autores"
testar "filtros combinados na listagem"    200 GET    "/autores?nome=machado&nacionalidade=brasil"
testar "obter autor existente"             200 GET    "/autores/1"
testar "autor inexistente"                 404 GET    "/autores/999"
testar "criar autor"                       201 POST   "/autores" '{"nome":"Jorge Amado","nacionalidade":"Brasileira","ano_nascimento":1912}'
testar "criar autor sem nome"              400 POST   "/autores" '{"nacionalidade":"Brasileira"}'
testar "criar autor com ano invalido"      400 POST   "/autores" '{"nome":"Teste","ano_nascimento":"mil"}'
testar "atualizar autor"                   200 PUT    "/autores/1" '{"nome":"Machado de Assis","nacionalidade":"Brasileira","ano_nascimento":1839}'
testar "atualizar autor inexistente"       404 PUT    "/autores/999" '{"nome":"Nao Existe"}'
testar "autores sem livros (LEFT JOIN)"    200 GET    "/autores/sem-livros"

echo
echo "=== FILTRO POR CAMINHO ==="
testar "livros do autor 1"                 200 GET    "/autores/1/livros"
testar "livros de autor inexistente"       404 GET    "/autores/999/livros"

echo
echo "=== CRUD LIVROS (tabela filho) ==="
testar "listar livros"                     200 GET    "/livros"
testar "livros com JOIN (nome do autor)"   200 GET    "/livros/completos"
testar "obter livro existente"             200 GET    "/livros/1"
testar "livro inexistente"                 404 GET    "/livros/999"
testar "criar livro"                       201 POST   "/livros" '{"titulo":"Capitaes da Areia","ano":1937,"preco":44.90,"autor_id":1}'
testar "criar livro sem titulo"            400 POST   "/livros" '{"ano":2020,"autor_id":1}'
testar "criar livro com autor inexistente" 400 POST   "/livros" '{"titulo":"Livro Orfao","autor_id":999}'
testar "atualizar livro"                   200 PUT    "/livros/1" '{"titulo":"Dom Casmurro - Edicao Especial","preco":59.90}'
testar "atualizar livro inexistente"       404 PUT    "/livros/999" '{"titulo":"Nao Existe"}'

echo
echo "=== BUSCA COM LIKE (query string) ==="
testar "busca por titulo"                  200 GET    "/livros/busca?nome=casmurro"
testar "busca por autor"                   200 GET    "/livros/busca?autor=orwell"
testar "busca com varios filtros"          200 GET    "/livros/busca?nome=a&autor=machado&ano_min=1880&ano_max=1900&preco_max=60"
testar "busca com filtro invalido"         400 GET    "/livros/busca?ano_min=abc"

echo
echo "=== DELETE ==="
testar "apagar livro"                      200 DELETE "/livros/3"
testar "apagar livro inexistente"          404 DELETE "/livros/999"
testar "apagar autor com livros (CASCADE)" 200 DELETE "/autores/2"
testar "livros do autor apagado sumiram"   200 GET    "/livros/busca?autor=clarice"
testar "apagar autor inexistente"          404 DELETE "/autores/999"
testar "metodo nao permitido"              405 DELETE "/autores"

echo
echo "=============================="
echo "Testes OK: $OK | Falhas: $FALHOU"
echo "=============================="
[ "$FALHOU" -eq 0 ]
