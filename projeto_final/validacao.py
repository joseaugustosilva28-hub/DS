"""Funcoes de validacao reaproveitadas pelas rotas.

Cada funcao devolve (valor_convertido, mensagem_de_erro).
Se mensagem_de_erro for None, o valor esta valido.
"""


def pegar_json(request):
    """Le o corpo JSON da requisicao com seguranca.

    Devolve (dados, erro). Se o corpo nao for um objeto JSON valido,
    'erro' recebe a mensagem correspondente.
    """
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return None, "Envie um corpo JSON valido (objeto)."
    return dados, None


def texto_obrigatorio(dados, campo, tamanho_maximo=200):
    """Valida um campo de texto obrigatorio e nao vazio."""
    valor = dados.get(campo)
    if not isinstance(valor, str) or valor.strip() == "":
        return None, f"O campo '{campo}' e obrigatorio e deve ser um texto nao vazio."
    valor = valor.strip()
    if len(valor) > tamanho_maximo:
        return None, f"O campo '{campo}' deve ter no maximo {tamanho_maximo} caracteres."
    return valor, None


def texto_opcional(dados, campo, padrao=None, tamanho_maximo=200):
    """Valida um campo de texto opcional. Se ausente, devolve o padrao."""
    if campo not in dados or dados.get(campo) is None:
        return padrao, None
    return texto_obrigatorio(dados, campo, tamanho_maximo)


def inteiro_opcional(dados, campo, minimo=None, maximo=None, padrao=None):
    """Valida um campo inteiro opcional (aceita numero ou string numerica)."""
    if campo not in dados or dados.get(campo) is None:
        return padrao, None
    valor = dados.get(campo)
    if isinstance(valor, bool):
        return None, f"O campo '{campo}' deve ser um numero inteiro."
    try:
        valor = int(valor)
    except (TypeError, ValueError):
        return None, f"O campo '{campo}' deve ser um numero inteiro."
    if minimo is not None and valor < minimo:
        return None, f"O campo '{campo}' deve ser maior ou igual a {minimo}."
    if maximo is not None and valor > maximo:
        return None, f"O campo '{campo}' deve ser menor ou igual a {maximo}."
    return valor, None


def numero_opcional(dados, campo, minimo=None, padrao=None):
    """Valida um campo numerico (float) opcional."""
    if campo not in dados or dados.get(campo) is None:
        return padrao, None
    valor = dados.get(campo)
    if isinstance(valor, bool):
        return None, f"O campo '{campo}' deve ser um numero."
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return None, f"O campo '{campo}' deve ser um numero."
    if minimo is not None and valor < minimo:
        return None, f"O campo '{campo}' deve ser maior ou igual a {minimo}."
    return valor, None


def inteiro_obrigatorio(dados, campo, minimo=None):
    """Valida um campo inteiro obrigatorio."""
    if campo not in dados or dados.get(campo) is None:
        return None, f"O campo '{campo}' e obrigatorio."
    return inteiro_opcional(dados, campo, minimo=minimo)
