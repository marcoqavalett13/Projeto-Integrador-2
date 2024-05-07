import tkinter as tk 
from collections import defaultdict
from itertools import groupby

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
        print(self.estacao_nas_linhas)

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
                else:
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

# teste
metro.adicionar_conexao('Estação Central', 'A', 10, '1')
metro.adicionar_conexao('A', 'B', 10, '1')
metro.adicionar_conexao('B', 'C', 10, '1')
metro.adicionar_conexao('C', 'D', 10, '1')
metro.adicionar_conexao('D', 'Estação Central', 10, '1')

metro.adicionar_conexao('Estação Central', '1', 11, '2')
metro.adicionar_conexao('1', 'B', 11, '2')
metro.adicionar_conexao('B', '2', 1, '2')
metro.adicionar_conexao('2', '3', 10, '2')
metro.adicionar_conexao('3', 'Estação Central', 10, '2')

metro.adicionar_conexao('Estação Central', 'O', 25, '3')
metro.adicionar_conexao('O', 'N', 15, '3')
metro.adicionar_conexao('N', '3', 10, '3')
metro.adicionar_conexao('3', 'M', 1, '3')
metro.adicionar_conexao('M', 'Estação Central', 10, '3')

metro.adicionar_conexao('Estação Central', 'A', 40, '4')
metro.adicionar_conexao('A', 'B', 40, '4')
metro.adicionar_conexao('B', 'C', 40, '4')
metro.adicionar_conexao('C', 'D', 40, '4')
metro.adicionar_conexao('D', 'Estação Central', 40, '4')

# # 1
# metro.adicionar_conexao('Estação Central', 'Praça dos Girassóis', 7, '1')
# metro.adicionar_conexao('Praça dos Girassóis', 'Avenida das Flores', 5, '1')
# metro.adicionar_conexao('Avenida das Flores', 'Parque das Aves', 10, '1')
# metro.adicionar_conexao('Parque das Aves', 'Jardim Primavera', 8, '1')
# metro.adicionar_conexao('Jardim Primavera', 'Lago Azul', 12, '1')
# metro.adicionar_conexao('Lago Azul', 'Bosque Verde', 6, '1')
# metro.adicionar_conexao('Bosque Verde', 'Centro Comercial', 9, '1')
# metro.adicionar_conexao('Centro Comercial', 'Praia da Lua', 15, '1')
# metro.adicionar_conexao('Praia da Lua', 'Mirante do Sol', 7, '1')
# metro.adicionar_conexao('Mirante do Sol', 'Estação Central', 5, '1')

# # 2
# metro.adicionar_conexao('Estação Central', 'Praça das Artes', 6, '2')
# metro.adicionar_conexao('Praça das Artes', 'Rua do Comércio', 8, '2')
# metro.adicionar_conexao('Rua do Comércio', 'Avenida Central', 7, '2')
# metro.adicionar_conexao('Avenida Central', 'Parque dos Esportes', 10, '2')
# metro.adicionar_conexao('Parque dos Esportes', 'Estádio Municipal', 5, '2')
# metro.adicionar_conexao('Estádio Municipal', 'Estação Central', 9, '2')

# # 3
# metro.adicionar_conexao('Estação Central', 'Praça da Liberdade', 7, '3')
# metro.adicionar_conexao('Praça da Liberdade', 'Avenida da Paz', 6, '3')
# metro.adicionar_conexao('Avenida da Paz', 'Jardim Botânico', 8, '3')
# metro.adicionar_conexao('Jardim Botânico', 'Parque das Flores', 12, '3')
# metro.adicionar_conexao('Parque das Flores', 'Estação Central', 10, '3')

# # 4
# metro.adicionar_conexao('Estação Central', 'Praça dos Trabalhadores', 5, '4')
# metro.adicionar_conexao('Praça dos Trabalhadores', 'Avenida Industrial', 9, '4')
# metro.adicionar_conexao('Avenida Industrial', 'Parque Industrial', 11, '4')
# metro.adicionar_conexao('Parque Industrial', 'Zona Residencial', 7, '4')
# metro.adicionar_conexao('Zona Residencial', 'Estação Central', 8, '4')

# # 5
# metro.adicionar_conexao('Estação Central', 'Praça da Cultura', 6, '5')
# metro.adicionar_conexao('Praça da Cultura', 'Avenida do Saber', 9, '5')
# metro.adicionar_conexao('Avenida do Saber', 'Universidade', 10, '5')
# metro.adicionar_conexao('Universidade', 'Centro Tecnológico', 8, '5')
# metro.adicionar_conexao('Centro Tecnológico', 'Estação Central', 11, '5')

# # 6
# metro.adicionar_conexao('Estação Central', 'Praça do Mercado', 7, '6')
# metro.adicionar_conexao('Praça do Mercado', 'Rua das Lojas', 5, '6')
# metro.adicionar_conexao('Rua das Lojas', 'Avenida do Progresso', 10, '6')
# metro.adicionar_conexao('Avenida do Progresso', 'Centro Financeiro', 8, '6')
# metro.adicionar_conexao('Centro Financeiro', 'Bairro Residencial', 12, '6')
# metro.adicionar_conexao('Bairro Residencial', 'Estação Central', 6, '6')

# # 7
# metro.adicionar_conexao('Estação Central', 'Praça do Porto', 9, '7')
# metro.adicionar_conexao('Praça do Porto', 'Avenida Marítima', 6, '7')
# metro.adicionar_conexao('Avenida Marítima', 'Píer Turístico', 8, '7')
# metro.adicionar_conexao('Píer Turístico', 'Terminal de Cruzeiros', 10, '7')
# metro.adicionar_conexao('Terminal de Cruzeiros', 'Estação Central', 7, '7')

# # 8
# metro.adicionar_conexao('Estação Central', 'Praça das Fontes', 8, '8')
# metro.adicionar_conexao('Praça das Fontes', 'Avenida dos Lagos', 9, '8')
# metro.adicionar_conexao('Avenida dos Lagos', 'Parque Aquático', 6, '8')
# metro.adicionar_conexao('Parque Aquático', 'Bairro das Águas', 11, '8')
# metro.adicionar_conexao('Bairro das Águas', 'Estação Central', 7, '8')

# # 9
# metro.adicionar_conexao('Estação Central', 'Praça das Nações', 7, '9')
# metro.adicionar_conexao('Praça das Nações', 'Avenida dos Monumentos', 9, '9')
# metro.adicionar_conexao('Avenida dos Monumentos', 'Museu Histórico', 8, '9')
# metro.adicionar_conexao('Museu Histórico', 'Praça dos Patrimônios', 12, '9')
# metro.adicionar_conexao('Praça dos Patrimônios', 'Estação Central', 6, '9')

# # 10
# metro.adicionar_conexao('Estação Central', 'Praça do Teatro', 6, '10')
# metro.adicionar_conexao('Praça do Teatro', 'Avenida da Arte', 7, '10')
# metro.adicionar_conexao('Avenida da Arte', 'Galeria de Exposições', 9, '10')
# metro.adicionar_conexao('Galeria de Exposições', 'Centro Cultural', 8, '10')
# metro.adicionar_conexao('Centro Cultural', 'Estação Central', 10, '10')
# metro.adicionar_conexao('Bosque Municipal', 'Trilha Natural', 10, '16')
# metro.adicionar_conexao('Trilha Natural', 'Estação Central', 6, '16')

# # 17
# metro.adicionar_conexao('Estação Central', 'Praça dos Viajantes', 7, '17')
# metro.adicionar_conexao('Praça dos Viajantes', 'Avenida das Viagens', 6, '17')
# metro.adicionar_conexao('Avenida das Viagens', 'Terminal Rodoviário', 9, '17')
# metro.adicionar_conexao('Terminal Rodoviário', 'Estação Ferroviária', 8, '17')
# metro.adicionar_conexao('Estação Ferroviária', 'Estação Central', 11, '17')

# # 18
# metro.adicionar_conexao('Estação Central', 'Praça da Juventude', 8, '18')
# metro.adicionar_conexao('Praça da Juventude', 'Avenida da Diversão', 7, '18')
# metro.adicionar_conexao('Avenida da Diversão', 'Parque de Diversões', 10, '18')
# metro.adicionar_conexao('Parque de Diversões', 'Praça da Aventura', 9, '18')
# metro.adicionar_conexao('Praça da Aventura', 'Estação Central', 6, '18')

# # 19
# metro.adicionar_conexao('Estação Central', 'Praça do Sol', 9, '19')
# metro.adicionar_conexao('Praça do Sol', 'Avenida da Luz', 8, '19')
# metro.adicionar_conexao('Avenida da Luz', 'Parque Solar', 7, '19')
# metro.adicionar_conexao('Parque Solar', 'Avenida da Energia', 10, '19')
# metro.adicionar_conexao('Avenida da Energia', 'Estação Central', 6, '19')

# # 20
# metro.adicionar_conexao('Estação Central', 'Praça da Noite', 7, '20')
# metro.adicionar_conexao('Praça da Noite', 'Avenida das Estrelas', 6, '20')
# metro.adicionar_conexao('Avenida das Estrelas', 'Boate Central', 9, '20')
# metro.adicionar_conexao('Boate Central', 'Praça dos Sonhos', 8, '20')
# metro.adicionar_conexao('Praça dos Sonhos', 'Estação Central', 11, '20')

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

def calcular_tempo_viagem(distancia_km, velocidade_media=60):
    tempo_horas = distancia_km / velocidade_media
    
    horas = int(tempo_horas)
    minutos = int((tempo_horas - horas) * 60)
    
    return f"{horas}:{minutos}h"

def printar():
    resultado_label.config(text='')
    resultado_text.delete('1.0', tk.END)

    for estacao, conexoes in metro.grafo.items():
        resultado_text.insert(tk.END, f'{estacao}:\n')
        for destino, detalhes in conexoes.items():
            detalhes_formatados = ', '.join(f"({distancia}, '{linha}')" for distancia, linha in detalhes)
            resultado_text.insert(tk.END, f'  {destino}: [{detalhes_formatados}]\n')
        resultado_text.insert(tk.END, '\n') 

def encontrar_menor_caminho():
    resultado_text.delete('1.0', tk.END)
    estacao_origem = origem_entry.get().strip().upper()
    estacao_destino = destino_entry.get().strip().upper()

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

root = tk.Tk()
root.title("Metrô de Erechim")

resultado_text = tk.Text(root, wrap='word', height=25, width=80)
resultado_text.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

scroll = tk.Scrollbar(root, command=resultado_text.yview)
scroll.grid(row=6, column=4, sticky='nsew')
resultado_text['yscrollcommand'] = scroll.set

origem_label = tk.Label(root, text="Estação de Origem:")
origem_label.grid(row=0, column=0, padx=10, pady=5)

origem_entry = tk.Entry(root)
origem_entry.grid(row=0, column=1, padx=10, pady=5)

destino_label = tk.Label(root, text="Estação de Destino:")
destino_label.grid(row=1, column=0, padx=10, pady=5)

destino_entry = tk.Entry(root)
destino_entry.grid(row=1, column=1, padx=10, pady=5)

linha_label = tk.Label(root, text="Linha:")
linha_label.grid(row=2, column=0, padx=10, pady=5)

linha_entry = tk.Entry(root)
linha_entry.grid(row=2, column=1, padx=10, pady=5)

distancia_label = tk.Label(root, text="Distância:")
distancia_label.grid(row=3, column=0, padx=10, pady=5)

distancia_entry = tk.Entry(root)
distancia_entry.grid(row=3, column=1, padx=10, pady=5)

adicionar_button = tk.Button(root, text="Adicionar Conexão", command=add_new)
adicionar_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

remover_button = tk.Button(root, text="Remover Conexão", command=pop_old)
remover_button.grid(row=4, column=3, columnspan=2, padx=10, pady=10)

calcular_button = tk.Button(root, text="Print Grafo", command=printar)
calcular_button.grid(row=5, column=3, columnspan=2, padx=10, pady=10)

print_button = tk.Button(root, text="Calcular", command=encontrar_menor_caminho)
print_button.grid(row=5, column=0, columnspan=2, padx=10, pady=1)

resultado_label = tk.Label(root, text="", justify=tk.LEFT)
resultado_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
