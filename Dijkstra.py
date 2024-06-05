import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import math

class Metro:
    def __init__(self):
        self.grafo = defaultdict(lambda: defaultdict(list))
        self.estacao_nas_linhas = defaultdict(set)

    def pode_chegar_a_estacao_central(self, estacao_origem):
        if estacao_origem == 'ESTAÇÃO CENTRAL':
            return True
        visitados = set()
        fila = [estacao_origem]

        while fila:
            estacao_atual = fila.pop(0)
            if estacao_atual == 'ESTAÇÃO CENTRAL':
                return True
            for vizinho in self.grafo[estacao_atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return False

    def adicionar_conexao(self, estacao_origem, estacao_destino, distancia, linha):
        estOrigem = estacao_origem.upper()
        estDestino = estacao_destino.upper()

        if estOrigem == 'ESTAÇÃO CENTRAL' and estDestino == 'ESTAÇÃO CENTRAL':
            return

        if 'ESTAÇÃO CENTRAL' in self.grafo[estOrigem]:
            del self.grafo[estOrigem]['ESTAÇÃO CENTRAL']
            self.adicionar_conexao(estDestino, 'ESTAÇÃO CENTRAL', distancia, linha)

        self.grafo[estOrigem][estDestino].append((distancia, linha))
        self.estacao_nas_linhas[estOrigem].add(linha)
        self.estacao_nas_linhas[estDestino].add(linha)

        # Atualizar comboboxes
        atualizar_comboboxes()


    def remover_conexao(self, estacao_origem, estacao_destino, linha):
        estOrigem = estacao_origem.strip().upper()
        estDestino = estacao_destino.strip().upper()

        if estDestino in self.grafo[estOrigem]:
            estado_original = list(self.grafo[estOrigem][estDestino])

            self.grafo[estOrigem][estDestino] = [conexao for conexao in self.grafo[estOrigem][estDestino] if conexao[1] != linha]
            if not self.grafo[estOrigem][estDestino]:
                del self.grafo[estOrigem][estDestino]

            if not self.pode_chegar_a_estacao_central(estOrigem):
                self.grafo[estOrigem][estDestino] = estado_original
                return f"Não é possível remover o trecho {estacao_origem.title()} até {estacao_destino.title()} na linha {linha}, pois isso deixaria a estação sem nenhuma rota originária."

            # Verifica se a estação ainda tem conexões
            if not self.grafo[estOrigem]:
                del self.grafo[estOrigem]
                del self.estacao_nas_linhas[estOrigem]

            if not self.grafo[estDestino]:
                del self.grafo[estDestino]
                del self.estacao_nas_linhas[estDestino]

            atualizar_comboboxes()
            return f"Conexão {estacao_origem.title()} até {estacao_destino.title()} na linha {linha} removida."
        else:
            return f"Nenhuma conexão encontrada no trecho {estacao_origem.title()} até {estacao_destino.title()} na linha {linha}."

    def dijkstra(self, estacao_origem, estacao_destino):
        distancias = defaultdict(lambda: float('inf'))
        predecessores = {}
        distancias[estacao_origem] = 0
        nao_visitados = set(self.grafo.keys())

        while nao_visitados:
            estacao_atual = min(nao_visitados, key=lambda estacao: distancias[estacao])
            nao_visitados.remove(estacao_atual)

            for estacao_vizinha, conexoes in self.grafo[estacao_atual].items():
                for distancia, linha in conexoes:
                    nova_distancia = distancias[estacao_atual] + distancia
                    if nova_distancia < distancias[estacao_vizinha]:
                        distancias[estacao_vizinha] = nova_distancia
                        predecessores[estacao_vizinha] = (estacao_atual, linha)

        caminho = []
        prox_estacao = estacao_destino
        caminho_linhas = []

        while prox_estacao != estacao_origem:
            if prox_estacao is None:
                break
            caminho.append(prox_estacao.title())
            linha_atual = predecessores.get(prox_estacao)
            if linha_atual:
                if linha_atual[0] == "ESTAÇÃO CENTRAL":
                    caminho_linhas.append("Estação Central")
                elif len(caminho_linhas) > 0:
                    if ("Linha " + linha_atual[1]) != caminho_linhas[-1]:
                        caminho_linhas.append("Linha " + linha_atual[1])
                elif len(caminho_linhas) == 0:
                    caminho_linhas.append("Linha " + linha_atual[1])
                prox_estacao = linha_atual[0]
            else:
                caminho.append("Linha sem nenhuma ligação final, favor adicionar o retorno à Estação Central no destino.")
                break

        caminho.append(estacao_origem)
        caminho.reverse()
        caminho_linhas.reverse()

        return distancias[estacao_destino], caminho, caminho_linhas

metro = Metro()


# Atualizar comboboxes
def atualizar_comboboxes():
    estacoes = set(metro.grafo.keys())
    for destinos in metro.grafo.values():
        estacoes.update(destinos.keys())
    estacoes = sorted(estacoes)
    origem_combobox['values'] = estacoes
    destino_combobox['values'] = estacoes

# Função para abrir a janela de cadastro
def abrir_janela_cadastro():
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro de Conexão")

    origem_label = tk.Label(cadastro_window, text="Estação de Origem:")
    origem_label.grid(row=0, column=0, padx=10, pady=5)

    origem_entry = tk.Entry(cadastro_window)
    origem_entry.grid(row=0, column=1, padx=10, pady=5)

    destino_label = tk.Label(cadastro_window, text="Estação de Destino:")
    destino_label.grid(row=1, column=0, padx=10, pady=5)

    destino_entry = tk.Entry(cadastro_window)
    destino_entry.grid(row=1, column=1, padx=10, pady=5)

    linha_label = tk.Label(cadastro_window, text="Linha:")
    linha_label.grid(row=2, column=0, padx=10, pady=5)

    linha_entry = tk.Entry(cadastro_window)
    linha_entry.grid(row=2, column=1, padx=10, pady=5)

    distancia_label = tk.Label(cadastro_window, text="Distância:")
    distancia_label.grid(row=3, column=0, padx=10, pady=5)

    distancia_entry = tk.Entry(cadastro_window)
    distancia_entry.grid(row=3, column=1, padx=10, pady=5)

    def add_new():
        resultado_text.delete('1.0', tk.END)
        new_origem = origem_entry.get().strip().upper()
        new_destino = destino_entry.get().strip().upper()
        new_distancia = distancia_entry.get()
        new_linha = linha_entry.get()

        metro.adicionar_conexao(new_origem, new_destino, int(new_distancia), new_linha)
        origem_entry.delete(0, tk.END)
        destino_entry.delete(0, tk.END)
        distancia_entry.delete(0, tk.END)
        linha_entry.delete(0, tk.END)
        resultado_str = f"Deslocamento de {new_origem.title()} até {new_destino.title()} adicionado na linha {new_linha}, com distância de {new_distancia}."
        resultado_label.config(text=resultado_str)
        atualizar_comboboxes()

    def pop_old():
        resultado_text.delete('1.0', tk.END)
        new_origem = origem_entry.get().strip().upper()
        new_destino = destino_entry.get().strip().upper()
        new_linha = linha_entry.get()
        origem_entry.delete(0, tk.END)
        destino_entry.delete(0, tk.END)
        linha_entry.delete(0, tk.END)

        remocao = metro.remover_conexao(new_origem, new_destino, new_linha)
        resultado_label.config(text=remocao)
        atualizar_comboboxes()

    adicionar_button = tk.Button(cadastro_window, text="Adicionar Conexão", command=add_new)
    adicionar_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    remover_button = tk.Button(cadastro_window, text="Remover Conexão", command=pop_old)
    remover_button.grid(row=4, column=3, columnspan=2, padx=10, pady=10)

# Função para calcular o tempo de viagem
def calcular_tempo_viagem(distancia_km, velocidade_media=30):
    tempo_horas = distancia_km / velocidade_media

    horas = int(tempo_horas)
    minutos = int((tempo_horas * 60) % 60)
    segundos = int((tempo_horas * 3600) % 60)

    return f"{horas} horas, {minutos} minutos e {segundos} segundos"

# Função para printar o grafo
def printar():
    resultado_text.delete('1.0', tk.END)
    for origem, destinos in metro.grafo.items():
        resultado_text.insert(tk.END, f"{origem}:\n")
        for destino, detalhes in destinos.items():
            detalhes_formatados = ", ".join(f"({distancia} km, Linha {linha})" for distancia, linha in detalhes)
            resultado_text.insert(tk.END, f'  {destino}: [{detalhes_formatados}]\n')
        resultado_text.insert(tk.END, '\n')

# Função para encontrar o menor caminho
def encontrar_menor_caminho():
    resultado_text.delete('1.0', tk.END)
    estacao_origem = origem_combobox.get().strip().upper()
    estacao_destino = destino_combobox.get().strip().upper()

    if estacao_origem != 'ESTAÇÃO CENTRAL' and not metro.pode_chegar_a_estacao_central(estacao_origem):
        resultado_label.config(text=f"Não é possível ir da Estação Central até {estacao_origem.title()}, favor inserir conexão à Estação.")
        return

    if estacao_origem not in metro.estacao_nas_linhas:
        resultado_str = f"Estação {estacao_origem.title()} não encontrada"
        resultado_label.config(text=resultado_str)
        return

    if estacao_destino not in metro.estacao_nas_linhas:
        resultado_str = f"Estação {estacao_destino.title()} não encontrada"
        resultado_label.config(text=resultado_str)
        return

    menor_caminho_distancia, menor_caminho_estacoes, trocas_de_linha = metro.dijkstra(estacao_origem, estacao_destino)

    if "Linha sem nenhuma ligação final, favor adicionar o retorno à Estação Central no destino." in menor_caminho_estacoes:
        caminho_str = "Linha sem nenhuma ligação final, favor adicionar o retorno à Estação Central no destino."
        resultado_str = caminho_str
    else:
        caminho_str = " -> ".join(menor_caminho_estacoes)
        resultado_str = f"O melhor caminho entre {estacao_origem.title()} e {estacao_destino.title()} tem {menor_caminho_distancia} km, e demora aproximadamente {calcular_tempo_viagem(menor_caminho_distancia)}.\nCaminho: {caminho_str}\n"

    if trocas_de_linha:
        resultado_str += "\nTrocas de linha:\n"
        resultado_str += " -> ".join(trocas_de_linha)
    resultado_label.config(text=resultado_str)


def desenhar_grafo():
    grafo_window = tk.Toplevel(root)
    grafo_window.title("Grafo de Conexões")

    canvas = tk.Canvas(grafo_window, width=800, height=600, bg="white")
    canvas.pack()

    estacoes_pos = {}
    centro_x, centro_y = 400, 300
    raio = 200
    n = len(metro.grafo)
    angulo = 360 / n
    circulo_raio = 10

    linha_cores = {
        '1': 'red',
        '2': 'green',
        '3': 'blue',
    }

    for i, estacao in enumerate(metro.grafo.keys()):
        x = centro_x + raio * math.cos(math.radians(i * angulo))
        y = centro_y + raio * math.sin(math.radians(i * angulo))
        estacoes_pos[estacao] = (x, y)
        # Determinar a cor da estação com base nas linhas que passam por ela
        linhas = metro.estacao_nas_linhas[estacao]
        cor = linha_cores.get(next(iter(linhas)), "black") if linhas else "black"
        canvas.create_oval(x-circulo_raio, y-circulo_raio, x+circulo_raio, y+circulo_raio, fill=cor)
        # Desenhar contorno preto do texto
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            canvas.create_text(x + dx, y - 15 + dy, text=estacao, anchor=tk.CENTER, fill="black", font=('Helvetica', 10, 'bold'))
        # Desenhar texto amarelo no centro
        canvas.create_text(x, y-15, text=estacao, anchor=tk.CENTER, fill="yellow", font=('Helvetica', 10, 'bold'))

    # Função para calcular o ponto de interseção fora do círculo
    def calcular_ponto_intersecao(x1, y1, x2, y2, raio):
        dx, dy = x2 - x1, y2 - y1
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            return x2, y2  # Evita divisão por zero
        scale = (dist - raio) / dist
        return x1 + dx * scale, y1 + dy * scale

    # Desenhar as conexões
    for estacao_origem, destinos in metro.grafo.items():
        for estacao_destino, detalhes in destinos.items():
            x1, y1 = estacoes_pos[estacao_origem]
            x2, y2 = estacoes_pos[estacao_destino]
            offset = 0
            for detalhe in detalhes:
                dx = (y2 - y1) * offset / 10
                dy = (x1 - x2) * offset / 10
                x1_offset, y1_offset = x1 + dx, y1 + dy
                x2_offset, y2_offset = calcular_ponto_intersecao(x1_offset, y1_offset, x2 + dx, y2 + dy, circulo_raio)
                canvas.create_line(x1_offset, y1_offset, x2_offset, y2_offset, arrow=tk.LAST)
                offset += 2  # Incrementa o offset para desenhar a próxima linha ligeiramente deslocada



root = tk.Tk()
root.title("Metrô de Erechim")

# Adicionar botão para desenhar o grafo
desenhar_button = tk.Button(root, text="Desenhar Grafo", command=desenhar_grafo)
desenhar_button.grid(row=2, column=3, columnspan=2, padx=10, pady=10)

resultado_text = tk.Text(root, wrap='word', height=25, width=80)
resultado_text.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

scroll = tk.Scrollbar(root, command=resultado_text.yview)
scroll.grid(row=6, column=4, sticky='nsew')
resultado_text['yscrollcommand'] = scroll.set

origem_label = tk.Label(root, text="Estação de Origem:")
origem_label.grid(row=0, column=0, padx=10, pady=5)

origem_combobox = ttk.Combobox(root)
origem_combobox.grid(row=0, column=1, padx=10, pady=5)

destino_label = tk.Label(root, text="Estação de Destino:")
destino_label.grid(row=1, column=0, padx=10, pady=5)

destino_combobox = ttk.Combobox(root)
destino_combobox.grid(row=1, column=1, padx=10, pady=5)

adicionar_button = tk.Button(root, text="Cadastrar Conexão", command=abrir_janela_cadastro)
adicionar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

calcular_button = tk.Button(root, text="Print Grafo", command=printar)
calcular_button.grid(row=3, column=3, columnspan=2, padx=10, pady=10)

print_button = tk.Button(root, text="Calcular", command=encontrar_menor_caminho)
print_button.grid(row=3, column=0, columnspan=2, padx=10, pady=1)

resultado_label = tk.Label(root, text="", justify=tk.LEFT)
resultado_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#teste 01

metro.adicionar_conexao('Estação Central', 'A', 10, '1')
metro.adicionar_conexao('A', 'B', 10, '1')
metro.adicionar_conexao('B', '2', 5, '1')
metro.adicionar_conexao('2', '3', 5, '1')
metro.adicionar_conexao('3', 'C', 50, '1')
metro.adicionar_conexao('C', 'ESTAÇÃO CENTRAL', 50, '1')

metro.adicionar_conexao('Estação Central', '1', 15, '2')
metro.adicionar_conexao('1', 'B', 10, '2')
metro.adicionar_conexao('B', '2', 5, '2')
metro.adicionar_conexao('2', '3', 5, '2')
metro.adicionar_conexao('3', '4', 50, '2')
metro.adicionar_conexao('4', 'estação central', 50, '2')

metro.adicionar_conexao('Estação Central', 'O', 30, '3')
metro.adicionar_conexao('O', 'N', 15, '3')
metro.adicionar_conexao('N', '3', 10, '3')
metro.adicionar_conexao('3', 'M', 5, '3')
metro.adicionar_conexao('M', 'Estação Central', 5, '3')


# Preencher comboboxes inicialmente
atualizar_comboboxes()

root.mainloop()
