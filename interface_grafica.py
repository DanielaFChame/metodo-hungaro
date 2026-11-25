import tkinter as tk
from tkinter import messagebox, ttk
import hungaro


MATRIZ_EXEMPLO = [
    [10, 15, 20, 25],
    [12, 18, 22, 28],
    [14, 20, 26, 30],
    [28, 22, 18, 10]
]


class AplicacaoHungaro:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Húngaro — Visualizador Passo a Passo")
        self.root.geometry("980x680")
        self.root.configure(bg="#f4f6f9")

        self.etapas = []
        self.indice_etapa = 0

        self._construir_interface()
        self._carregar_matriz_na_grade(MATRIZ_EXEMPLO)
        self._executar_algoritmo()

    def _construir_interface(self):
        # Cabeçalho
        topo = tk.Frame(self.root, bg="#1e293b", pady=12, padx=20)
        topo.pack(fill="x")

        tk.Label(
            topo,
            text="Método Húngaro — Passo a Passo Visual",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#1e293b",
        ).pack(anchor="w")

        tk.Label(
            topo,
            text="Visualize reduções, cobertura de zeros por linhas/colunas e ajustes com k",
            font=("Segoe UI", 10),
            fg="#cbd5e1",
            bg="#1e293b",
        ).pack(anchor="w")

        # Área principal dividida em esquerda (entrada) e direita (visualização)
        corpo = tk.Frame(self.root, bg="#f4f6f9", padx=16, pady=12)
        corpo.pack(fill="both", expand=True)

        painel_esq = tk.LabelFrame(
            corpo,
            text=" Configuração da Matriz ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            padx=12,
            pady=12,
        )
        painel_esq.pack(side="left", fill="y", padx=(0, 12))

        # Objetivo
        obj_frame = tk.Frame(painel_esq, bg="white")
        obj_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            obj_frame, text="Objetivo:", bg="white", font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 8))

        self.var_objetivo = tk.IntVar(value=0)
        ttk.Radiobutton(
            obj_frame, text="Minimizar", variable=self.var_objetivo, value=0
        ).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(
            obj_frame, text="Maximizar", variable=self.var_objetivo, value=1
        ).pack(side="left")

        # Caixa de texto grande para digitar as linhas da matriz
        tk.Label(
            painel_esq,
            text="Matriz (uma linha por linha, ex: 1,2,3,4):",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(4, 4))

        self.txt_matriz = tk.Text(
            painel_esq,
            width=26,
            height=8,
            font=("Consolas", 10),
            relief="solid",
            bd=1,
            padx=6,
            pady=6,
        )
        self.txt_matriz.pack(fill="x", pady=(0, 6))

        # Aviso de erro de validação da matriz (oculto por padrão)
        self.lbl_erro_matriz = tk.Label(
            painel_esq,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg="#fee2e2",
            fg="#991b1b",
            highlightbackground="#ef4444",
            highlightthickness=1,
            justify="left",
            wraplength=220,
            padx=8,
            pady=6,
            anchor="w",
        )

        # Grade de inputs
        self.frame_inputs = tk.Frame(painel_esq, bg="white", pady=6)
        self.frame_inputs.pack(pady=6)

        # Botões de ação
        btn_frame = tk.Frame(painel_esq, bg="white")
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(
            btn_frame, text="Resolver / Reiniciar", command=self._executar_algoritmo
        ).pack(fill="x", pady=3)
        ttk.Button(
            btn_frame, text="Carregar Exemplo (4x4)", command=self._carregar_exemplo
        ).pack(fill="x", pady=3)

        # Legenda
        leg_frame = tk.LabelFrame(
            painel_esq,
            text=" Legenda Visual ",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            padx=8,
            pady=8,
        )
        leg_frame.pack(fill="x", pady=(16, 0))

        self._item_legenda(leg_frame, "#dcfce7", "#166534", "Zero selecionado / atribuição")
        self._item_legenda(leg_frame, "#fef9c3", "#854d0e", "Elemento não coberto (-k)")
        self._item_legenda(leg_frame, "#fee2e2", "#991b1b", "Interseção riscada (+k)")
        self._item_legenda(leg_frame, "#2563eb", "#2563eb", "Linha/Coluna riscada (cobertura)", linha=True)

        # Painel direito: visualização da etapa
        painel_dir = tk.LabelFrame(
            corpo,
            text=" Demonstração da Etapa ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            padx=14,
            pady=12,
        )
        painel_dir.pack(side="right", fill="both", expand=True)

        self.lbl_titulo_etapa = tk.Label(
            painel_dir,
            text="",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#0f172a",
            anchor="w",
        )
        self.lbl_titulo_etapa.pack(fill="x")

        self.lbl_explicacao = tk.Label(
            painel_dir,
            text="",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg="#334155",
            justify="left",
            wraplength=560,
            padx=10,
            pady=8,
            relief="groove",
            bd=1,
        )
        self.lbl_explicacao.pack(fill="x", pady=(6, 10))

        # Card de destaque para a solução ótima (Etapa final)
        self.card_resultado = tk.Frame(
            painel_dir,
            bg="#ecfdf5",
            highlightbackground="#16a34a",
            highlightthickness=2,
            padx=12,
            pady=10,
        )

        self.lbl_resultado_header = tk.Label(
            self.card_resultado,
            text="★ ATRIBUIÇÕES ÓTIMAS ESCOLHIDAS",
            font=("Segoe UI", 10, "bold"),
            fg="#15803d",
            bg="#ecfdf5",
            anchor="w",
        )
        self.lbl_resultado_header.pack(fill="x")

        self.lbl_resultado_itens = tk.Label(
            self.card_resultado,
            text="",
            font=("Segoe UI", 11, "bold"),
            fg="#0f172a",
            bg="#ecfdf5",
            justify="left",
            wraplength=540,
            anchor="w",
        )
        self.lbl_resultado_itens.pack(fill="x", pady=(4, 2))

        self.lbl_resultado_total = tk.Label(
            self.card_resultado,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg="#166534",
            bg="#ecfdf5",
            anchor="w",
        )
        self.lbl_resultado_total.pack(fill="x")

        self.canvas = tk.Canvas(
            painel_dir, bg="white", highlightthickness=1, highlightbackground="#cbd5e1"
        )
        self.canvas.pack(fill="both", expand=True)

        # Controles de navegação entre etapas
        nav_frame = tk.Frame(painel_dir, bg="white", pady=8)
        nav_frame.pack(fill="x")

        self.btn_anterior = ttk.Button(
            nav_frame, text="◀ Etapa Anterior", command=self._etapa_anterior
        )
        self.btn_anterior.pack(side="left")

        self.lbl_contador = tk.Label(
            nav_frame, text="Etapa 0 / 0", font=("Segoe UI", 10, "bold"), bg="white"
        )
        self.lbl_contador.pack(side="left", padx=16)

        self.btn_proximo = ttk.Button(
            nav_frame, text="Próxima Etapa ▶", command=self._proxima_etapa
        )
        self.btn_proximo.pack(side="left")

        ttk.Button(
            nav_frame, text="Ir para o Final ⏭", command=self._ir_para_final
        ).pack(side="right")

    def _item_legenda(self, parent, bg_cor, fg_cor, texto, linha=False):
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", pady=2)
        if linha:
            c = tk.Canvas(row, width=22, height=16, bg="white", highlightthickness=0)
            c.create_line(2, 8, 20, 8, fill=fg_cor, width=3)
            c.pack(side="left", padx=(0, 6))
        else:
            tk.Label(
                row,
                text="  ",
                bg=bg_cor,
                fg=fg_cor,
                relief="solid",
                bd=1,
                font=("Segoe UI", 9, "bold"),
            ).pack(side="left", padx=(0, 6))
        tk.Label(row, text=texto, bg="white", fg="#334155", font=("Segoe UI", 8)).pack(
            side="left"
        )

    def _carregar_exemplo(self):
        self._carregar_matriz_na_grade(MATRIZ_EXEMPLO)
        self._executar_algoritmo()

    def _carregar_matriz_na_grade(self, matriz):
        linhas_formatadas = [
            ",".join(f"{v:g}" if isinstance(v, float) else str(v) for v in linha)
            for linha in matriz
        ]
        self.txt_matriz.delete("1.0", "end")
        self.txt_matriz.insert("1.0", "\n".join(linhas_formatadas))

    def _ler_matriz(self):
        conteudo = self.txt_matriz.get("1.0", "end").strip()
        if not conteudo:
            raise ValueError("Digite ao menos uma linha para formar a matriz.")

        linhas_processadas = []
        for idx, linha_raw in enumerate(conteudo.splitlines(), start=1):
            linha_limpa = linha_raw.strip()
            if not linha_limpa:
                continue

            linha_limpa = linha_limpa.strip("[]").rstrip(",").strip()
            if not linha_limpa:
                raise ValueError(f"A linha {idx} está vazia.")

            partes = [p.strip() for p in linha_limpa.replace(",", " ").split() if p.strip()]
            linha_vals = []
            for parte in partes:
                try:
                    valor = float(parte.replace(",", "."))
                except ValueError:
                    raise ValueError(f"Valor inválido '{parte}' na linha {idx}.")
                if valor.is_integer():
                    valor = int(valor)
                linha_vals.append(valor)

            linhas_processadas.append((idx, linha_vals))

        if not linhas_processadas:
            raise ValueError("Nenhuma linha válida encontrada.")

        qtd_esperada = len(linhas_processadas[0][1])
        for num_linha, vals in linhas_processadas:
            if len(vals) != qtd_esperada:
                raise ValueError(
                    f"Não é uma matriz: a linha {num_linha} tem {len(vals)} item(ns), "
                    f"mas as anteriores têm {qtd_esperada}."
                )

        return [vals for _, vals in linhas_processadas]

    def _executar_algoritmo(self):
        try:
            matriz = self._ler_matriz()
            self._ocultar_erro_matriz()
            objetivo = self.var_objetivo.get()
            self.etapas, _, _ = hungaro.resolver_com_etapas(matriz, objetivo)
            self.indice_etapa = 0
            self._desenhar_etapa()
        except ValueError as e:
            self._mostrar_erro_matriz(str(e))

    def _etapa_anterior(self):
        if self.indice_etapa > 0:
            self.indice_etapa -= 1
            self._desenhar_etapa()

    def _proxima_etapa(self):
        if self.indice_etapa < len(self.etapas) - 1:
            self.indice_etapa += 1
            self._desenhar_etapa()

    def _ir_para_final(self):
        if self.etapas:
            self.indice_etapa = len(self.etapas) - 1
            self._desenhar_etapa()

    def _desenhar_etapa(self):
        if not self.etapas:
            return

        etapa = self.etapas[self.indice_etapa]
        matriz = etapa["matriz"]
        linhas_cob = etapa["linhas_cobertas"]
        colunas_cob = etapa["colunas_cobertas"]
        posicoes = etapa["posicoes"]
        k = etapa["valor_k"]
        reducao_linhas = etapa.get("reducao_linhas", [])
        reducao_colunas = etapa.get("reducao_colunas", [])
        valor_max = etapa.get("valor_max")
        matriz_antes_max = etapa.get("matriz_antes_max")

        self.lbl_titulo_etapa.config(text=etapa["titulo"])
        self.lbl_explicacao.config(text=etapa["explicacao"])
        self.lbl_contador.config(
            text=f"Etapa {self.indice_etapa + 1} / {len(self.etapas)}"
        )

        self.btn_anterior.state(
            ["!disabled"] if self.indice_etapa > 0 else ["disabled"]
        )
        self.btn_proximo.state(
            ["!disabled"] if self.indice_etapa < len(self.etapas) - 1 else ["disabled"]
        )

        eh_etapa_final = self.indice_etapa == len(self.etapas) - 1

        if eh_etapa_final:
            if self.lbl_explicacao.winfo_ismapped():
                self.lbl_explicacao.pack_forget()
        else:
            if not self.lbl_explicacao.winfo_ismapped():
                self.lbl_explicacao.pack(
                    fill="x", pady=(6, 10), after=self.lbl_titulo_etapa
                )

        if eh_etapa_final and posicoes:
            matriz_orig = self.etapas[0]["matriz"]
            n_orig_l = len(matriz_orig)
            n_orig_c = len(matriz_orig[0])
            atribuicoes_reais = [
                (r, c) for (r, c) in posicoes if r < n_orig_l and c < n_orig_c
            ]
            total_otimo = hungaro.calcular_total(matriz_orig, atribuicoes_reais)

            linhas_texto = [
                f"• (L{r + 1}, C{c + 1}) - {matriz_orig[r][c]:g}"
                if isinstance(matriz_orig[r][c], float)
                else f"• (L{r + 1}, C{c + 1}) - {matriz_orig[r][c]}"
                for r, c in atribuicoes_reais
            ]

            self.lbl_resultado_itens.config(text="\n".join(linhas_texto))
            total_fmt = f"{total_otimo:g}" if isinstance(total_otimo, float) else str(total_otimo)
            self.lbl_resultado_total.config(text=f"Valor Total Ótimo: {total_fmt}")

            if not self.card_resultado.winfo_ismapped():
                self.card_resultado.pack(fill="x", pady=(6, 10), before=self.canvas)
        else:
            if self.card_resultado.winfo_ismapped():
                self.card_resultado.pack_forget()

        self.canvas.delete("all")
        self.canvas.update_idletasks()

        n_linhas = len(matriz)
        n_colunas = len(matriz[0])

        largura_canvas = max(self.canvas.winfo_width(), 400)
        altura_canvas = max(self.canvas.winfo_height(), 300)

        tam_celula = min(
            74,
            max(46, int((largura_canvas - 120) / max(n_colunas, 1))),
            max(46, int((altura_canvas - 90) / max(n_linhas, 1))),
        )

        largura_grade = n_colunas * tam_celula
        altura_grade = n_linhas * tam_celula

        x0 = max(50, (largura_canvas - largura_grade) // 2)
        y0 = max(35, (altura_canvas - altura_grade) // 2)

        # Rótulos de colunas e linhas
        for j in range(n_colunas):
            cx = x0 + j * tam_celula + tam_celula / 2
            self.canvas.create_text(
                cx, y0 - 16, text=f"C{j+1}", font=("Segoe UI", 9, "bold"), fill="#64748b"
            )

        for i in range(n_linhas):
            cy = y0 + i * tam_celula + tam_celula / 2
            self.canvas.create_text(
                x0 - 22, cy, text=f"L{i+1}", font=("Segoe UI", 9, "bold"), fill="#64748b"
            )

        # Desenha células
        for i in range(n_linhas):
            for j in range(n_colunas):
                rx1 = x0 + j * tam_celula
                ry1 = y0 + i * tam_celula
                rx2 = rx1 + tam_celula
                ry2 = ry1 + tam_celula

                fill_cor = "white"
                texto_cor = "#0f172a"
                borda_cor = "#94a3b8"
                espessura_borda = 1

                if (i, j) in posicoes:
                    fill_cor = "#bbf7d0" if eh_etapa_final else "#dcfce7"
                    texto_cor = "#14532d"
                    borda_cor = "#15803d"
                    espessura_borda = 3 if eh_etapa_final else 2
                elif k is not None and (linhas_cob or colunas_cob):
                    cob_l = i in linhas_cob
                    cob_c = j in colunas_cob
                    if not cob_l and not cob_c:
                        fill_cor = "#fef9c3"
                        texto_cor = "#854d0e"
                    elif cob_l and cob_c:
                        fill_cor = "#fee2e2"
                        texto_cor = "#991b1b"

                self.canvas.create_rectangle(
                    rx1,
                    ry1,
                    rx2,
                    ry2,
                    fill=fill_cor,
                    outline=borda_cor,
                    width=espessura_borda,
                )

                val = matriz[i][j]
                texto_val = f"{val:g}" if isinstance(val, float) else str(val)

                # sub_texto
                sub_texto = ""
                if k is not None and (linhas_cob or colunas_cob) and not posicoes:
                    cob_l = i in linhas_cob
                    cob_c = j in colunas_cob
                    if not cob_l and not cob_c:
                        sub_texto = f"-{k:g}" if isinstance(k, float) else f"-{k}"
                    elif cob_l and cob_c:
                        sub_texto = f"+{k:g}" if isinstance(k, float) else f"+{k}"

                if (
                    valor_max is not None
                    and matriz_antes_max is not None
                    and i < len(matriz_antes_max)
                    and j < len(matriz_antes_max[0])
                ):
                    antigo = matriz_antes_max[i][j]
                    ant_s = f"{antigo:g}" if isinstance(antigo, float) else str(antigo)

                    # Valor antigo no canto superior esquerdo da célula
                    self.canvas.create_text(
                        rx1 + 6,
                        ry1 + 5,
                        text=ant_s,
                        font=("Segoe UI", 8),
                        fill="#94a3b8",
                        anchor="nw",
                    )
                    # Valor convertido no centro
                    self.canvas.create_text(
                        rx1 + tam_celula / 2,
                        ry1 + tam_celula / 2 + 2,
                        text=texto_val,
                        font=("Segoe UI", 12, "bold"),
                        fill=texto_cor,
                    )
                elif sub_texto:
                    # Etapa de cobertura/ajuste: mantém exatamente o visual com -k / +k em vermelho
                    self.canvas.create_text(
                        rx1 + tam_celula / 2,
                        ry1 + tam_celula * 0.40,
                        text=texto_val,
                        font=("Segoe UI", 12, "bold"),
                        fill=texto_cor,
                    )
                    self.canvas.create_text(
                        rx1 + tam_celula / 2,
                        ry1 + tam_celula * 0.76,
                        text=sub_texto,
                        font=("Segoe UI", 8, "bold"),
                        fill="#dc2626",
                    )
                else:
                    self.canvas.create_text(
                        rx1 + tam_celula / 2,
                        ry1 + tam_celula / 2,
                        text=texto_val,
                        font=("Segoe UI", 12, "bold"),
                        fill=texto_cor,
                    )

        # ---> ADICIONE O VALOR MÁXIMO DO LADO DA MATRIZ AQUI <---
        if valor_max is not None:
            max_fmt = f"{valor_max:g}" if isinstance(valor_max, float) else str(valor_max)
            bx1 = x0 + largura_grade + 18
            by1 = y0
            bx2 = bx1 + 84
            by2 = by1 + 40

            self.canvas.create_rectangle(
                bx1,
                by1,
                bx2,
                by2,
                fill="#fef3c7",
                outline="#d97706",
                width=2,
            )
            self.canvas.create_text(
                (bx1 + bx2) / 2,
                by1 + 12,
                text="VALOR MÁX",
                font=("Segoe UI", 7, "bold"),
                fill="#b45309",
            )
            self.canvas.create_text(
                (bx1 + bx2) / 2,
                by1 + 27,
                text=max_fmt,
                font=("Segoe UI", 12, "bold"),
                fill="#78350f",
            )

        # Marca redução por linhas à direita da matriz (-valor em vermelho)
        for i, menor in enumerate(reducao_linhas):
            if menor != 0:
                cy = y0 + i * tam_celula + tam_celula / 2
                rotulo = f"-{menor:g}" if isinstance(menor, float) else f"-{menor}"
                self.canvas.create_text(
                    x0 + largura_grade + 24,
                    cy,
                    text=rotulo,
                    font=("Segoe UI", 10, "bold"),
                    fill="#dc2626",
                )

        # Marca redução por colunas embaixo da matriz (-valor em vermelho)
        for j, menor in enumerate(reducao_colunas):
            if menor != 0:
                cx = x0 + j * tam_celula + tam_celula / 2
                rotulo = f"-{menor:g}" if isinstance(menor, float) else f"-{menor}"
                self.canvas.create_text(
                    cx,
                    y0 + altura_grade + 18,
                    text=rotulo,
                    font=("Segoe UI", 10, "bold"),
                    fill="#dc2626",
                )

        # Desenha linhas riscadas (cobertura de linhas)
        for i in linhas_cob:
            cy = y0 + i * tam_celula + tam_celula / 2
            self.canvas.create_line(
                x0 - 10,
                cy,
                x0 + largura_grade + 10,
                cy,
                fill="#2563eb",
                width=3,
            )

        # Desenha colunas riscadas (cobertura de colunas)
        for j in colunas_cob:
            cx = x0 + j * tam_celula + tam_celula / 2
            self.canvas.create_line(
                cx,
                y0 - 10,
                cx,
                y0 + altura_grade + 10,
                fill="#2563eb",
                width=3,
            )

    def _mostrar_erro_matriz(self, mensagem):
        self.lbl_erro_matriz.config(text=f"⚠ {mensagem}")
        if not self.lbl_erro_matriz.winfo_ismapped():
            self.lbl_erro_matriz.pack(fill="x", pady=(4, 4), after=self.txt_matriz)

    def _ocultar_erro_matriz(self):
        if self.lbl_erro_matriz.winfo_ismapped():
            self.lbl_erro_matriz.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoHungaro(root)
    root.mainloop()