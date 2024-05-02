#MARCO

import tkinter as tk
from collections import defaultdict  # Importa defaultdict para criar um dicionário com valores padrão
# O "defaultdict" serve como uma camada a mais de robustez pra aplicação. Se o usuário tenta fazer uma pesquisa entre
# duas estações de metrô que não possuem conexão, ao invés de retornar um erro "Key Error" (chave inexistente) ele cria
# a conexão e atribui um dicionário com valor padrão.
# estamos testando essa funcionalidade ainda, falar com o Marcos Lucas


#Quando um método de uma classe é chamado, o Python automaticamente passa o objeto como o primeiro argumento para o método,
#por isso é necessário ter self como o primeiro parâmetro em todos os métodos da classe para acessar os atributos e métodos do objeto.

class Metro:
    def __init__(self):
        self.grafo = defaultdict(dict)  # inicializa o grafo como um dicionário padrão
        #__self__(self) metodo especial que representa a inicialização da classe


    def adicionar_conexao(self, estacao_origem, estacao_destino, distancia):
        self.grafo[estacao_origem][estacao_destino] = distancia  # adiciona uma conexão entre as estações de metrô
        self.grafo[estacao_destino][estacao_origem] = distancia  # adiciona a conexão inversa com a mesma distância

    def dijkstra(self, estacao_origem, estacao_destino):
        distancias = {estacao: float('inf') for estacao in self.grafo}  # inicializa todas as distâncias como infinito
        #compreensão de dicionário essa expressão cria um dicionário onde as chaves são as estações do grafo e os valores são inicializados como infinito. Isso é usado para representar
        #as distâncias iniciais no algoritmo de Dijkstra, onde todas as distâncias são consideradas como infinito no início, exceto a distância da estação de origem, que é zero.

        distancias[estacao_origem] = 0  # define a distância da estação de origem como 0
        nao_visitados = set(self.grafo.keys())  # cria um conjunto de estações não visitadas

        while nao_visitados:
            estacao_atual = min(nao_visitados, key=lambda estacao: distancias[estacao])  # escolhe a estação não visitada com a menor distância
            #lambda é utilizado para nomear funções anônimas em Python, onde não tem a necessidade de serem definidas com "def"
            #estrutura: lambda parametros: expressao ex: lambda x: x**2 funcao que recebe x e retorna ele ao quadrado

            nao_visitados.remove(estacao_atual)  # remove a estação atual da lista de não visitados

            for estacao_vizinha, distancia in self.grafo[estacao_atual].items():  # para cada estação vizinha da estação atual
                nova_distancia = distancias[estacao_atual] + distancia  # calcula a nova distância
                if nova_distancia < distancias[estacao_vizinha]:  # se a nova distância for menor que a anterior
                    distancias[estacao_vizinha] = nova_distancia  # atualiza a distância para a nova menor distância

        return distancias[estacao_destino]  # retorna a menor distância até a estação de destino

# criando a instância do metrô
metro = Metro()  # cria um objeto da classe Metro

# adicionando conexões entre as estações de metrô
# conexoes e distâncias fictícias, verificar com o ML.

metro.adicionar_conexao('A', 'B', 5)
metro.adicionar_conexao('B', 'C', 3)
metro.adicionar_conexao('C', 'D', 7)
metro.adicionar_conexao('A', 'D', 10)
metro.adicionar_conexao('B', 'E', 2)
metro.adicionar_conexao('E', 'F', 4)
metro.adicionar_conexao('F', 'G', 6)
metro.adicionar_conexao('G', 'H', 8)
metro.adicionar_conexao('H', 'I', 9)
metro.adicionar_conexao('I', 'J', 7)
metro.adicionar_conexao('J', 'K', 5)
metro.adicionar_conexao('K', 'L', 3)

####

def encontrar_menor_caminho():
    estacao_origem = origem_entry.get()  # estação de origem do campo de entrada
    estacao_destino = destino_entry.get()  # estação de destino do campo de entrada

    menor_caminho = metro.dijkstra(estacao_origem, estacao_destino)  # calcula o menor caminho
    resultado_label.config(text=f"A menor distância entre {estacao_origem} e {estacao_destino} é: {menor_caminho}" + " KM")  #display do resultado


def add_new():
    new_d = new_d_entry.get()
    new_e = new_e_entry.get()
    new_km = new_km_entry.get()

    metro.adicionar_conexao(new_d, new_e, int(new_km))

root = tk.Tk()  # cria uma instância da classe Tk para a janela principal
root.title("Metrô de Erechim")  # define o título da janela


origem_label = tk.Label(root, text="Estação de Origem:")  # entrada da estação de origem
origem_label.grid(row=0, column=0, padx=10, pady=5)  # posição do label

origem_entry = tk.Entry(root)  # cria uma entrada para o usuário inserir a estação de origem
# estudar equivalencia do .toUpper()
origem_entry.grid(row=0, column=1, padx=10, pady=5)  # posição do label

destino_label = tk.Label(root, text="Estação de Destino:")  # entrada da estação de destino
destino_label.grid(row=1, column=0, padx=10, pady=5)  # posição do label

destino_entry = tk.Entry(root)  # cria uma entrada para o usuário inserir a estação de destino
# estudar equivalencia do .toUpper()
destino_entry.grid(row=1, column=1, padx=10, pady=5)  # posição do label

calcular_button = tk.Button(root, text="Calcular", command=encontrar_menor_caminho)  # botão para calcular o menor caminho
calcular_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)  # posição do botão

resultado_label = tk.Label(root, text="")  # exibição do resultado
resultado_label.grid(row=3, column=0, columnspan=2)  # posição do resultado


new_d_entry = tk.Entry(root)
new_d_entry.grid(row=4, column=1, padx=4, pady=5)

new_e_entry = tk.Entry(root)
new_e_entry.grid(row=5, column=1, padx=4, pady=5)

new_km_entry = tk.Entry(root)
new_km_entry.grid(row=6, column=1, padx=4, pady=5)

add_button = tk.Button(root, text="Add", command=add_new)  # botão para calcular o menor caminho
add_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)  # posição do botão


root.mainloop()  # inicia o loop principal da interface gráfica
