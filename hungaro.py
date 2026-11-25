def verificar_Matriz(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])
    return linhas == colunas


def transformar_quadrada(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])
    resultado = [linha[:] for linha in matriz]

    if linhas < colunas:
        for _ in range(colunas - linhas):
            resultado.append([0] * colunas)
    elif colunas < linhas:
        for linha in resultado:
            for _ in range(linhas - colunas):
                linha.append(0)

    return resultado


def Max_Min(matriz, objetivo):
    resultado = []

    if objetivo == 1:  # maximizar
        maior = max(max(linha) for linha in matriz)
        for linha in matriz:
            resultado.append([maior - valor for valor in linha])
    elif objetivo == 0:  # minimizar
        for linha in matriz:
            resultado.append(linha[:])
    else:
        raise ValueError("Objetivo inválido")

    return resultado


def subtrair_linhas(matriz):
    resultado = []
    for linha in matriz:
        menor = min(linha)
        resultado.append([valor - menor for valor in linha])
    return resultado


def subtrair_colunas(matriz):
    resultado = [linha[:] for linha in matriz]
    linhas = len(resultado)
    colunas = len(resultado[0])

    for j in range(colunas):
        menor_coluna = min(matriz[i][j] for i in range(linhas))
        for i in range(linhas):
            resultado[i][j] = matriz[i][j] - menor_coluna

    return resultado


def encontrar_zeros(matriz):
    posicoes = []
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 0:
                posicoes.append((i, j))
    return posicoes


def tentar_atribuir(linha, matriz, atribuicao, visitadas):
    colunas = len(matriz[0])
    for j in range(colunas):
        if matriz[linha][j] == 0 and not visitadas[j]:
            visitadas[j] = True
            if atribuicao[j] == -1 or tentar_atribuir(
                atribuicao[j], matriz, atribuicao, visitadas
            ):
                atribuicao[j] = linha
                return True
    return False


def selecionar_zeros_maximos(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])
    atribuicao = [-1] * colunas

    for i in range(linhas):
        visitadas = [False] * colunas
        tentar_atribuir(i, matriz, atribuicao, visitadas)

    selecionados = []
    for coluna, linha in enumerate(atribuicao):
        if linha != -1:
            selecionados.append((linha, coluna))

    selecionados.sort()
    return selecionados


def calcular_total(matriz_original, posicoes):
    total = 0
    for linha, coluna in posicoes:
        if linha < len(matriz_original) and coluna < len(matriz_original[0]):
            total += matriz_original[linha][coluna]
    return total


def cobrir_zeros(matriz, posicoes):
    """
    Pelo teorema de Kőnig, o número mínimo de linhas e colunas
    necessárias para cobrir todos os zeros é igual ao número máximo de zeros independentes.
    """
    linhas = len(matriz)
    colunas = len(matriz[0])

    linhas_atribuidas = [i for i, _ in posicoes]
    linhas_marcadas = [i for i in range(linhas) if i not in linhas_atribuidas]
    colunas_marcadas = []

    mudou = True
    while mudou:
        mudou = False
        for i in linhas_marcadas:
            for j in range(colunas):
                if matriz[i][j] == 0 and j not in colunas_marcadas:
                    colunas_marcadas.append(j)
                    mudou = True

        for i, j in posicoes:
            if j in colunas_marcadas and i not in linhas_marcadas:
                linhas_marcadas.append(i)
                mudou = True

    linhas_cobertas = [i for i in range(linhas) if i not in linhas_marcadas]
    colunas_cobertas = colunas_marcadas[:]

    return linhas_cobertas, colunas_cobertas


def obter_menor_nao_coberto(matriz, linhas_cobertas, colunas_cobertas):
    linhas = len(matriz)
    colunas = len(matriz[0])
    nao_cobertos = [
        matriz[i][j]
        for i in range(linhas)
        for j in range(colunas)
        if i not in linhas_cobertas and j not in colunas_cobertas
    ]
    return min(nao_cobertos) if nao_cobertos else 0


def ajustar_matriz(matriz, linhas_cobertas, colunas_cobertas):
    resultado = [linha[:] for linha in matriz]
    linhas = len(matriz)
    colunas = len(matriz[0])
    menor = obter_menor_nao_coberto(matriz, linhas_cobertas, colunas_cobertas)

    for i in range(linhas):
        for j in range(colunas):
            coberta_linha = i in linhas_cobertas
            coberta_coluna = j in colunas_cobertas
            if not coberta_linha and not coberta_coluna:
                resultado[i][j] = matriz[i][j] - menor
            elif coberta_linha and coberta_coluna:
                resultado[i][j] = matriz[i][j] + menor

    return resultado


def registrar_etapa(
    etapas,
    titulo,
    explicacao,
    matriz,
    linhas_cobertas=None,
    colunas_cobertas=None,
    posicoes=None,
    valor_k=None,
    reducao_linhas=None,
    reducao_colunas=None,
    valor_max=None,
    matriz_antes_max=None,
):
    etapas.append(
        {
            "titulo": titulo,
            "explicacao": explicacao,
            "matriz": [linha[:] for linha in matriz],
            "linhas_cobertas": list(linhas_cobertas) if linhas_cobertas is not None else [],
            "colunas_cobertas": list(colunas_cobertas) if colunas_cobertas is not None else [],
            "posicoes": list(posicoes) if posicoes is not None else [],
            "valor_k": valor_k,
            "reducao_linhas": list(reducao_linhas) if reducao_linhas is not None else [],
            "reducao_colunas": list(reducao_colunas) if reducao_colunas is not None else [],
            "valor_max": valor_max,
            "matriz_antes_max": (
                [linha[:] for linha in matriz_antes_max]
                if matriz_antes_max is not None
                else None
            ),
        }
    )

def resolver_com_etapas(custos, objetivo):
    etapas = []
    n_orig_linhas = len(custos)
    n_orig_colunas = len(custos[0])

    registrar_etapa(
        etapas,
        "1. Matriz Original",
        "Matriz de custos/pesos inicial informada pelo usuário.",
        custos,
    )

    if verificar_Matriz(custos):
        matriz_atual = [linha[:] for linha in custos]
        registrar_etapa(
            etapas,
            "2. Matriz Quadrada",
            "A matriz já é quadrada, então nenhuma linha ou coluna fictícia foi adicionada.",
            matriz_atual,
        )
    else:
        matriz_atual = transformar_quadrada(custos)
        registrar_etapa(
            etapas,
            "2. Matriz Quadrada",
            "Como a matriz não era quadrada, foram adicionadas linhas ou colunas fictícias com zeros.",
            matriz_atual,
        )

    if objetivo == 1:
        matriz_antes = [linha[:] for linha in matriz_atual]
        maior_val = max(max(linha) for linha in matriz_atual)
        matriz_atual = Max_Min(matriz_atual, 1)
        registrar_etapa(
            etapas,
            "3. Conversão para Maximização",
            f"Cada elemento foi substituído por ({maior_val} - valor_antigo).",
            matriz_atual,
            valor_max=maior_val,
            matriz_antes_max=matriz_antes,
        )
    else:
        registrar_etapa(
            etapas,
            "3. Objetivo: Minimização",
            "Como o objetivo é minimizar, os valores da matriz são mantidos.",
            matriz_atual,
        )

    menores_linhas = [min(linha) for linha in matriz_atual]
    matriz_atual = subtrair_linhas(matriz_atual)
    registrar_etapa(
        etapas,
        "4. Redução por Linhas",
        f"Subtraído o menor valor de cada linha: {menores_linhas}.",
        matriz_atual,
        reducao_linhas=menores_linhas,
    )

    menores_colunas = [
        min(matriz_atual[i][j] for i in range(len(matriz_atual)))
        for j in range(len(matriz_atual[0]))
    ]
    matriz_atual = subtrair_colunas(matriz_atual)
    registrar_etapa(
        etapas,
        "5. Redução por Colunas",
        f"Subtraído o menor valor de cada coluna: {menores_colunas}.",
        matriz_atual,
        reducao_colunas=menores_colunas,
    )

    tamanho = len(matriz_atual)
    iteracao = 1

    while True:
        posicoes = selecionar_zeros_maximos(matriz_atual)
        registrar_etapa(
            etapas,
            f"6.{iteracao} Busca de Zeros Independentes",
            f"Encontrados {len(posicoes)} zeros independentes (destacados em verde) de um total necessário de {tamanho}.",
            matriz_atual,
            posicoes=posicoes,
        )

        if len(posicoes) == tamanho:
            break

        linhas_cob, colunas_cob = cobrir_zeros(matriz_atual, posicoes)
        k = obter_menor_nao_coberto(matriz_atual, linhas_cob, colunas_cob)

        registrar_etapa(
            etapas,
            f"6.{iteracao}b Cobertura de Zeros (Linhas e Colunas Riscadas)",
            f"Como {len(posicoes)} < {tamanho}, cobrimos todos os zeros com {len(linhas_cob) + len(colunas_cob)} traços "
            f"(linhas riscadas: {[i+1 for i in linhas_cob]}, colunas riscadas: {[j+1 for j in colunas_cob]}). "
            f"Menor elemento não riscado (k) = {k}.",
            matriz_atual,
            linhas_cobertas=linhas_cob,
            colunas_cobertas=colunas_cob,
            posicoes=posicoes,
            valor_k=k,
        )

        matriz_atual = ajustar_matriz(matriz_atual, linhas_cob, colunas_cob)
        registrar_etapa(
            etapas,
            f"6.{iteracao}c Ajuste da Matriz (k = {k})",
            f"Elementos não riscados: subtrai {k}. "
            f"Interseções de linha e coluna riscadas: soma {k}. "
            f"Demais elementos riscados: permanecem iguais.",
            matriz_atual,
            linhas_cobertas=linhas_cob,
            colunas_cobertas=colunas_cob,
            valor_k=k,
        )
        iteracao += 1

    posicoes_reais = [
        (r, c) for (r, c) in posicoes if r < n_orig_linhas and c < n_orig_colunas
    ]
    total = calcular_total(custos, posicoes_reais)
    detalhes = ", ".join(
        f"({r+1},{c+1})={custos[r][c]}" for r, c in posicoes_reais
    )

    registrar_etapa(
        etapas,
        "7. Solução Ótima Encontrada",
        f"Atribuições escolhidas: {detalhes}  |  Valor total ótimo = {total}.",
        matriz_atual,
        posicoes=posicoes_reais,
    )

    return etapas, posicoes_reais, total