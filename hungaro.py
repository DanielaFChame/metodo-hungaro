def verificar_Matriz(matriz):

    linhas = len(matriz)
    colunas = len(matriz[0])

    if linhas == colunas:
        return True

    else:
        return False


def transformar_quadrada(matriz):

    linhas = len(matriz)
    colunas = len(matriz[0])

    resultado = []

    for linha in matriz:
        resultado.append(linha[:])

    if linhas < colunas:
        for i in range(colunas - linhas):
            nova_linha = [0] * colunas
            resultado.append(nova_linha)

    elif colunas < linhas:
        for linha in resultado:
            for i in range(linhas - colunas):
                linha.append(0)

    return resultado


def Max_Min(matriz, objetivo):
    resultado = []

    if objetivo == 1:  # maximizar
        maior = max(max(linha) for linha in matriz)

        for linha in matriz:
            nova_linha = []

            for valor in linha:
                nova_linha.append(maior - valor)

            resultado.append(nova_linha)

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
        nova_linha = []

        for valor in linha:
            nova_linha.append(valor - menor)

        resultado.append(nova_linha)

    return resultado


def subtrair_colunas(matriz):
    resultado = [linha[:] for linha in matriz]

    linhas = len(resultado)
    colunas = len(resultado[0])

    for j in range(colunas):
        menor_coluna = matriz[0][j]

        for i in range(linhas):
            if matriz[i][j] < menor_coluna:
                menor_coluna = matriz[i][j]

        for i in range(linhas):
            resultado[i][j] = matriz[i][j] - menor_coluna

    return resultado


def encontrar_zeros(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])

    posicoes = []

    for i in range(linhas):
        for j in range(colunas):
            if matriz[i][j] == 0:
                posicoes.append((i, j))

    return posicoes


# def selecionar_zeros(posicoes):
#     selecinados = []
#     linhas_usadas = []
#     colunas_usadas = []

#     for i, j in posicoes:

#         if i not in linhas_usadas and j not in colunas_usadas:
#             linhas_usadas.append(i)
#             colunas_usadas.append(j)
#             selecinados.append((i,j))

#     return selecinados


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

    return selecionados


def calcular_total(matriz_original, posicoes):
    total = 0

    for (
        linha,
        coluna,
    ) in posicoes:
        total += matriz_original[linha][coluna]

    return total


def cobrir_zeros(matriz, posicoes):
    """

    Pelo teorema de Kőnig, o número mínimo de linhas e colunas
    necessárias para cobrir todos os zeros é igual ao número máximo de zeros independentes.

    """

    linhas = len(matriz)
    colunas = len(matriz[0])

    # identificar as linhas que possuem zeros selecionados

    linhas_atribuidas = []

    for i, j in posicoes:
        linhas_atribuidas.append(i)

    # identificar as linhas que possuem não possuem zeros selecionados

    linhas_marcadas = []

    for i in range(linhas):
        if i not in linhas_atribuidas:
            linhas_marcadas.append(i)

    colunas_marcadas = []

    mudou = True

    while mudou:
        mudou = False

        # marcar as colunas que contêm zeros nas linhas marcadas

        for i in linhas_marcadas:
            for j in range(colunas):
                if matriz[i][j] == 0 and j not in colunas_marcadas:
                    colunas_marcadas.append(j)
                    mudou = True

        # marcar as linhas que contêm zeros nas colunas marcadas

        for i, j in posicoes:
            if j in colunas_marcadas and i not in linhas_marcadas:
                linhas_marcadas.append(i)
                mudou = True

    # linhas cobertas = linhas que nao foram marcadas

    linhas_cobertas = []

    for i in range(linhas):
        if i not in linhas_marcadas:
            linhas_cobertas.append(i)

    colunas_cobertas = colunas_marcadas[:]

    return linhas_cobertas, colunas_cobertas


def ajustar_matriz(matriz, linhas_cobertas, colunas_cobertas):
    resultado = [linha[:] for linha in matriz]

    linhas = len(matriz)
    colunas = len(matriz[0])

    nao_cobertas = []

    for i in range(linhas):
        for j in range(colunas):
            if i not in linhas_cobertas and j not in colunas_cobertas:
                nao_cobertas.append((i, j))

    linha, coluna = nao_cobertas[0]
    menor = matriz[linha][coluna]

    for i, j in nao_cobertas:
        if matriz[i][j] < menor:
            menor = matriz[i][j]

    for i, j in nao_cobertas:
        resultado[i][j] = matriz[i][j] - menor

    for i in linhas_cobertas:
        for j in colunas_cobertas:
            resultado[i][j] = matriz[i][j] + menor

    return resultado


def resolver_com_etapas(custos, objetivo):
    etapas = []
    etapas.append(custos)
    etapas.append(transformar_quadrada(custos))


def registrar_etapa(
    etapas, titulo, matriz, linhas_cobertas=None, colunas_cobertas=None, posicoes=None
):
    dicionario = {
        "titulo": titulo,
        "matriz": [linha[:] for linha in matriz],
        "linhas_cobertas": linhas_cobertas,
        "colunas_cobertas": colunas_cobertas,
        "posicoes": posicoes,
    }
    etapas.append(dicionario)


def resolver_com_etapas(custos, objetivo):

    etapas = []

    registrar_etapa(etapas, "Matriz original", custos)

    matriz_quadrada = transformar_quadrada(custos)
    registrar_etapa(etapas, "Matriz quadrada", matriz_quadrada)

    matriz_preparada = Max_Min(matriz_quadrada, objetivo)

    if objetivo == 0:
        titulo = "Minimizar: matriz mantida como está"
    else:
        titulo = "Maximizar: maior - valor"
    registrar_etapa(etapas, titulo, matriz_preparada)
