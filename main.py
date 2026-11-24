import hungaro


def main():
    custos = [[13, 11, 1, 2], [11, 22, 12, 10], [6, 10, 1, 6], [6, 8, 1, 4]]

    objetivo = int(input("Minimizar (0) ou maximizar (1)? "))

    if hungaro.verificar_Matriz(custos):
        matriz_quadrada = [linha[:] for linha in custos]

    else:
        matriz_quadrada = hungaro.transformar_quadrada(custos)

    matriz_preparada = hungaro.Max_Min(matriz_quadrada, objetivo)

    print("\nMatriz preparada:\n")

    for linha in matriz_preparada:
        print(linha)

    matriz_linhas = hungaro.subtrair_linhas(matriz_preparada)

    print("\nMatriz após redução das linhas:\n")

    for linha in matriz_linhas:
        print(linha)

    matriz_colunas = hungaro.subtrair_colunas(matriz_linhas)

    print("\nMatriz após redução das colunas:\n")

    for linha in matriz_colunas:
        print(linha)

    posicoes = hungaro.selecionar_zeros_maximos(matriz_colunas)

    while len(posicoes) != len(matriz_colunas):
        linhas_cobertas, colunas_cobertas = hungaro.cobrir_zeros(
            matriz_colunas, posicoes
        )
        matriz_colunas = hungaro.ajustar_matriz(
            matriz_colunas, linhas_cobertas, colunas_cobertas
        )
        posicoes = hungaro.selecionar_zeros_maximos(matriz_colunas)
        print("\nAjuste Necessário, numero de  0 independentes < tamanho da matriz\n")
        for linha in matriz_colunas:
            print(linha)

    print("\nAtribuição ótima encontrada\n")

    posicoes_reais = []

    for linha, coluna in posicoes:
        if linha < len(custos) and coluna < len(custos[0]):
            posicoes_reais.append((linha, coluna))
            print(f"Linha {linha}, Coluna {coluna} ---> {custos[linha][coluna]}")

    total = hungaro.calcular_total(custos, posicoes_reais)
    print("Valor ótimo: ", total)


if __name__ == "__main__":
    main()
