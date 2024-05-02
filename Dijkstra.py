import tkinter as tk 
from collections import defaultdict

class Metro:
    def __init__(self):
        self.grafo = defaultdict(dict)
        self.linhas_por_estacao = defaultdict(list)

    def adicionar_conexao(self, estacao_origem, estacao_destino, distancia, linha):
        self.grafo[estacao_origem][estacao_destino] = (distancia, linha)
        self.linhas_por_estacao[estacao_origem].append(linha)
        self.linhas_por_estacao[estacao_destino].append(linha)

    def dijkstra(self, estacao_origem, estacao_destino):
        distancias = {estacao: float('inf') for estacao in self.grafo}
        predecessores = {estacao: None for estacao in self.grafo}
        distancias[estacao_origem] = 0
        nao_visitados = set(self.grafo.keys())

        while nao_visitados:
            estacao_atual = min(nao_visitados, key=lambda estacao: distancias[estacao])
            nao_visitados.remove(estacao_atual)

            for estacao_vizinha, (distancia, linha) in self.grafo[estacao_atual].items():
                nova_distancia = distancias[estacao_atual] + distancia
                if nova_distancia < distancias[estacao_vizinha]:
                    distancias[estacao_vizinha] = nova_distancia
                    predecessores[estacao_vizinha] = estacao_atual

        caminho = []
        estacao = estacao_destino
        caminho_linhas = []
        linha_anterior = None
        while estacao is not None:
            caminho.append(estacao)
            if predecessores[estacao] is not None:
                estacao_anterior = predecessores[estacao]
                linha_atual = set(self.linhas_por_estacao[estacao])
                linha_anterior = set(self.linhas_por_estacao[estacao_anterior])
                if linha_atual != linha_anterior:
                    caminho_linhas.append((linha_anterior.pop(), linha_atual.pop()))
            estacao = predecessores[estacao]

        caminho.reverse()
        caminho_linhas.reverse()
        return distancias[estacao_destino], caminho, caminho_linhas

metro = Metro()

# LINHA1
metro.adicionar_conexao('Estação Central', 'Praça dos Girassóis', 7, 'Linha1')
metro.adicionar_conexao('Praça dos Girassóis', 'Avenida das Flores', 5, 'Linha1')
metro.adicionar_conexao('Avenida das Flores', 'Parque das Aves', 10, 'Linha1')
metro.adicionar_conexao('Parque das Aves', 'Jardim Primavera', 8, 'Linha1')
metro.adicionar_conexao('Jardim Primavera', 'Lago Azul', 12, 'Linha1')
metro.adicionar_conexao('Lago Azul', 'Bosque Verde', 6, 'Linha1')
metro.adicionar_conexao('Bosque Verde', 'Centro Comercial', 9, 'Linha1')
metro.adicionar_conexao('Centro Comercial', 'Praia da Lua', 15, 'Linha1')
metro.adicionar_conexao('Praia da Lua', 'Mirante do Sol', 7, 'Linha1')
metro.adicionar_conexao('Mirante do Sol', 'Estação Central', 5, 'Linha1')

# LINHA2
metro.adicionar_conexao('Estação Central', 'Praça das Artes', 6, 'Linha2')
metro.adicionar_conexao('Praça das Artes', 'Rua do Comércio', 8, 'Linha2')
metro.adicionar_conexao('Rua do Comércio', 'Avenida Central', 7, 'Linha2')
metro.adicionar_conexao('Avenida Central', 'Parque dos Esportes', 10, 'Linha2')
metro.adicionar_conexao('Parque dos Esportes', 'Estádio Municipal', 5, 'Linha2')
metro.adicionar_conexao('Estádio Municipal', 'Estação Central', 9, 'Linha2')

# LINHA3
metro.adicionar_conexao('Estação Central', 'Praça da Liberdade', 7, 'Linha3')
metro.adicionar_conexao('Praça da Liberdade', 'Avenida da Paz', 6, 'Linha3')
metro.adicionar_conexao('Avenida da Paz', 'Jardim Botânico', 8, 'Linha3')
metro.adicionar_conexao('Jardim Botânico', 'Parque das Flores', 12, 'Linha3')
metro.adicionar_conexao('Parque das Flores', 'Estação Central', 10, 'Linha3')

# LINHA4
metro.adicionar_conexao('Estação Central', 'Praça dos Trabalhadores', 5, 'Linha4')
metro.adicionar_conexao('Praça dos Trabalhadores', 'Avenida Industrial', 9, 'Linha4')
metro.adicionar_conexao('Avenida Industrial', 'Parque Industrial', 11, 'Linha4')
metro.adicionar_conexao('Parque Industrial', 'Zona Residencial', 7, 'Linha4')
metro.adicionar_conexao('Zona Residencial', 'Estação Central', 8, 'Linha4')

# LINHA5
metro.adicionar_conexao('Estação Central', 'Praça da Cultura', 6, 'Linha5')
metro.adicionar_conexao('Praça da Cultura', 'Avenida do Saber', 9, 'Linha5')
metro.adicionar_conexao('Avenida do Saber', 'Universidade', 10, 'Linha5')
metro.adicionar_conexao('Universidade', 'Centro Tecnológico', 8, 'Linha5')
metro.adicionar_conexao('Centro Tecnológico', 'Estação Central', 11, 'Linha5')

# LINHA6
metro.adicionar_conexao('Estação Central', 'Praça do Mercado', 7, 'Linha6')
metro.adicionar_conexao('Praça do Mercado', 'Rua das Lojas', 5, 'Linha6')
metro.adicionar_conexao('Rua das Lojas', 'Avenida do Progresso', 10, 'Linha6')
metro.adicionar_conexao('Avenida do Progresso', 'Centro Financeiro', 8, 'Linha6')
metro.adicionar_conexao('Centro Financeiro', 'Bairro Residencial', 12, 'Linha6')
metro.adicionar_conexao('Bairro Residencial', 'Estação Central', 6, 'Linha6')

# LINHA7
metro.adicionar_conexao('Estação Central', 'Praça do Porto', 9, 'Linha7')
metro.adicionar_conexao('Praça do Porto', 'Avenida Marítima', 6, 'Linha7')
metro.adicionar_conexao('Avenida Marítima', 'Píer Turístico', 8, 'Linha7')
metro.adicionar_conexao('Píer Turístico', 'Terminal de Cruzeiros', 10, 'Linha7')
metro.adicionar_conexao('Terminal de Cruzeiros', 'Estação Central', 7, 'Linha7')

# LINHA8
metro.adicionar_conexao('Estação Central', 'Praça das Fontes', 8, 'Linha8')
metro.adicionar_conexao('Praça das Fontes', 'Avenida dos Lagos', 9, 'Linha8')
metro.adicionar_conexao('Avenida dos Lagos', 'Parque Aquático', 6, 'Linha8')
metro.adicionar_conexao('Parque Aquático', 'Bairro das Águas', 11, 'Linha8')
metro.adicionar_conexao('Bairro das Águas', 'Estação Central', 7, 'Linha8')

# LINHA9
metro.adicionar_conexao('Estação Central', 'Praça das Nações', 7, 'Linha9')
metro.adicionar_conexao('Praça das Nações', 'Avenida dos Monumentos', 9, 'Linha9')
metro.adicionar_conexao('Avenida dos Monumentos', 'Museu Histórico', 8, 'Linha9')
metro.adicionar_conexao('Museu Histórico', 'Praça dos Patrimônios', 12, 'Linha9')
metro.adicionar_conexao('Praça dos Patrimônios', 'Estação Central', 6, 'Linha9')

# LINHA10
metro.adicionar_conexao('Estação Central', 'Praça do Teatro', 6, 'Linha10')
metro.adicionar_conexao('Praça do Teatro', 'Avenida da Arte', 7, 'Linha10')
metro.adicionar_conexao('Avenida da Arte', 'Galeria de Exposições', 9, 'Linha10')
metro.adicionar_conexao('Galeria de Exposições', 'Centro Cultural', 8, 'Linha10')
metro.adicionar_conexao('Centro Cultural', 'Estação Central', 10, 'Linha10')

# LINHA11
metro.adicionar_conexao('Estação Central', 'Praça da Harmonia', 7, 'Linha11')
metro.adicionar_conexao('Praça da Harmonia', 'Avenida da Serenidade', 6, 'Linha11')
metro.adicionar_conexao('Avenida da Serenidade', 'Bairro da Paz', 9, 'Linha11')
metro.adicionar_conexao('Bairro da Paz', 'Condomínio Residencial', 8, 'Linha11')
metro.adicionar_conexao('Condomínio Residencial', 'Estação Central', 11, 'Linha11')

# LINHA12
metro.adicionar_conexao('Estação Central', 'Praça da Alegria', 8, 'Linha12')
metro.adicionar_conexao('Praça da Alegria', 'Avenida da Felicidade', 10, 'Linha12')
metro.adicionar_conexao('Avenida da Felicidade', 'Parque dos Sonhos', 7, 'Linha12')
metro.adicionar_conexao('Parque dos Sonhos', 'Bairro das Cores', 12, 'Linha12')
metro.adicionar_conexao('Bairro das Cores', 'Estação Central', 6, 'Linha12')

# LINHA13
metro.adicionar_conexao('Estação Central', 'Praça do Saber', 7, 'Linha13')
metro.adicionar_conexao('Praça do Saber', 'Avenida da Educação', 9, 'Linha13')
metro.adicionar_conexao('Avenida da Educação', 'Escola Primária', 8, 'Linha13')
metro.adicionar_conexao('Escola Primária', 'Colégio Secundário', 11, 'Linha13')
metro.adicionar_conexao('Colégio Secundário', 'Estação Central', 10, 'Linha13')

# LINHA14
metro.adicionar_conexao('Estação Central', 'Praça da Justiça', 6, 'Linha14')
metro.adicionar_conexao('Praça da Justiça', 'Avenida da Lei', 7, 'Linha14')
metro.adicionar_conexao('Avenida da Lei', 'Tribunal', 9, 'Linha14')
metro.adicionar_conexao('Tribunal', 'Fórum', 8, 'Linha14')
metro.adicionar_conexao('Fórum', 'Estação Central', 10, 'Linha14')

# LINHA15
metro.adicionar_conexao('Estação Central', 'Praça da Saúde', 8, 'Linha15')
metro.adicionar_conexao('Praça da Saúde', 'Avenida da Cura', 6, 'Linha15')
metro.adicionar_conexao('Avenida da Cura', 'Hospital Central', 9, 'Linha15')
metro.adicionar_conexao('Hospital Central', 'Clínica Médica', 11, 'Linha15')
metro.adicionar_conexao('Clínica Médica', 'Estação Central', 7, 'Linha15')

# LINHA16
metro.adicionar_conexao('Estação Central', 'Praça do Parque', 9, 'Linha16')
metro.adicionar_conexao('Praça do Parque', 'Avenida das Árvores', 8, 'Linha16')
metro.adicionar_conexao('Avenida das Árvores', 'Bosque Municipal', 7, 'Linha16')
metro.adicionar_conexao('Bosque Municipal', 'Trilha Natural', 10, 'Linha16')
metro.adicionar_conexao('Trilha Natural', 'Estação Central', 6, 'Linha16')

# LINHA17
metro.adicionar_conexao('Estação Central', 'Praça dos Viajantes', 7, 'Linha17')
metro.adicionar_conexao('Praça dos Viajantes', 'Avenida das Viagens', 6, 'Linha17')
metro.adicionar_conexao('Avenida das Viagens', 'Terminal Rodoviário', 9, 'Linha17')
metro.adicionar_conexao('Terminal Rodoviário', 'Estação Ferroviária', 8, 'Linha17')
metro.adicionar_conexao('Estação Ferroviária', 'Estação Central', 11, 'Linha17')

# LINHA18
metro.adicionar_conexao('Estação Central', 'Praça da Juventude', 8, 'Linha18')
metro.adicionar_conexao('Praça da Juventude', 'Avenida da Diversão', 7, 'Linha18')
metro.adicionar_conexao('Avenida da Diversão', 'Parque de Diversões', 10, 'Linha18')
metro.adicionar_conexao('Parque de Diversões', 'Praça da Aventura', 9, 'Linha18')
metro.adicionar_conexao('Praça da Aventura', 'Estação Central', 6, 'Linha18')

# LINHA19
metro.adicionar_conexao('Estação Central', 'Praça do Sol', 9, 'Linha19')
metro.adicionar_conexao('Praça do Sol', 'Avenida da Luz', 8, 'Linha19')
metro.adicionar_conexao('Avenida da Luz', 'Parque Solar', 7, 'Linha19')
metro.adicionar_conexao('Parque Solar', 'Avenida da Energia', 10, 'Linha19')
metro.adicionar_conexao('Avenida da Energia', 'Estação Central', 6, 'Linha19')

# LINHA20
metro.adicionar_conexao('Estação Central', 'Praça da Noite', 7, 'Linha20')
metro.adicionar_conexao('Praça da Noite', 'Avenida das Estrelas', 6, 'Linha20')
metro.adicionar_conexao('Avenida das Estrelas', 'Boate Central', 9, 'Linha20')
metro.adicionar_conexao('Boate Central', 'Praça dos Sonhos', 8, 'Linha20')
metro.adicionar_conexao('Praça dos Sonhos', 'Estação Central', 11, 'Linha20')

def add_new():
    new_origem = origem_entry.get()
    new_destino = destino_entry.get()
    new_distancia = distancia_entry.get()
    new_linha = linha_entry.get()
    print("Dist" + new_distancia)

    metro.adicionar_conexao(new_origem, new_destino, int(new_distancia), new_linha)
    destino_entry.delete(0, tk.END)
    origem_entry.delete(0, tk.END)
    linha_entry.delete(0, tk.END)
    distancia_entry.delete(0, tk.END)



def encontrar_menor_caminho():
    estacao_origem = origem_entry.get()
    estacao_destino = destino_entry.get()
    print(distancia_entry)
    menor_caminho_distancia, menor_caminho_estacoes, trocas_de_linha = metro.dijkstra(estacao_origem, estacao_destino)

    caminho_str = " -> ".join(menor_caminho_estacoes)
    resultado_str = f"O melhor caminho entre {estacao_origem} e {estacao_destino} leva {menor_caminho_distancia} minutos.\nCaminho: {caminho_str}\n"

    if trocas_de_linha:
        resultado_str += "\nTrocas de linha:\n"
        for linha_origem, linha_destino in trocas_de_linha:
            resultado_str += f"De: {linha_origem} - Para: {linha_destino}\n"

    resultado_label.config(text=resultado_str)


root = tk.Tk()
root.title("Metrô de Erechim")

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
print(distancia_entry)

calcular_button = tk.Button(root, text="Calcular", command=encontrar_menor_caminho)
calcular_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

resultado_label = tk.Label(root, text="", justify=tk.LEFT)
resultado_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
print(distancia_entry)