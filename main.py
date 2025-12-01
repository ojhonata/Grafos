import pandas as pd # Lê o Excel e organiza os dados em tabelas
import numpy as np # Faz os cálculos das matrizes 
import os # Verifica se o arquivo realmente existe no computador
import networkx as nx # Cria a estrutura da rede e calcula as estatísticas Grau Médio, Densidade e Conectividade
import matplotlib.pyplot as plt # Desenha os grafos na tela

def carregar_excel(arquivo):
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo):
            print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
            print("Dica: Verifique se o nome está correto (ex: 'Dado.xlsx') e se está na mesma pasta do script.")
            return None
        
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(arquivo, engine='openpyxl')
        print(f"Sucesso! '{arquivo}' carregado com {len(df)} linhas.")
        return df
    except Exception as e:
        # Tratar erros na leitura do arquivo
        print(f"Erro ao ler: {e}")
        return None

dados = carregar_excel('Dados.xlsx')
print(dados)


print("MATRIZ DE INCIDÊNCIA:")
print("\n")
def gerar_matriz_incidencia(df):
    # Criar a matriz de incidência usando crosstab
    matriz = pd.crosstab(df['from'], df['to'])
    # Retornar a matriz de incidência
    return matriz

matriz_inc = gerar_matriz_incidencia(dados)

print(matriz_inc)
print("\n")
print("MATRIZ DE SIMILARIDADE:")
def gerar_matriz_similaridade(matriz_inc):
    # Multiplicação da matriz de incidência pela sua transposta
    matriz_sim = matriz_inc.dot(matriz_inc.T)
    np.fill_diagonal(matriz_sim.values, 0)
    # Retornar a matriz de similaridade
    return matriz_sim

matriz_sim = gerar_matriz_similaridade(matriz_inc)

print(matriz_sim)
print("\n")
print("MATRIZ DE COOCORRÊNCIA:")
print("\n")
def gerar_matriz_coocorrencia(matriz_inc):
    # Multiplicação da transposta da matriz de incidência pela própria matriz de incidência
    matriz_co = matriz_inc.T.dot(matriz_inc)
    # Definir os valores da diagonal principal como zero
    np.fill_diagonal(matriz_co.values, 0)
    # Retornar a matriz de coocorrência
    return matriz_co
matriz_co = gerar_matriz_coocorrencia(matriz_inc)

print(matriz_co)

print("\n")
print("GRAFOS:")
print("\n")
def gerar_grafo_incidencia(df):
    # Criar o grafo direcionado a partir do DataFrame
    G = nx.from_pandas_edgelist(df, source='from', target='to', edge_attr='weight', create_using=nx.DiGraph())
    
    plt.figure(figsize=(12, 8))
    
    # Definir a posição dos nós usando o layout spring
    pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42) 
    # Desenhar o grafo
    nx.draw(G, pos, 
            with_labels=True, 
            node_color='lightgray', 
            node_size=2000, 
            font_size=10,
            font_family='sans-serif',
            font_weight='bold',
            edge_color='gray',
            arrowsize=20)
            
    plt.title("Grafo de Incidência")
    plt.show()
    
    return G

grafo_inc = gerar_grafo_incidencia(dados)

def gerar_grafo_similaridade(matriz_sim):
    # Criar o grafo a partir da matriz de similaridade
    s = nx.from_pandas_adjacency(matriz_sim)
    # Remover arestas com peso zero
    arestas_zero = [(u, v) for u, v, d in s.edges(data=True) if d.get('weight', 0) == 0]
    s.remove_edges_from(arestas_zero)

    plt.figure(figsize=(14, 12))

    pos = nx.spring_layout(s, k=3.5, iterations=100, seed=42)
    # Obter os pesos das arestas para definir a largura
    pesos = [s[u][v]['weight'] for u, v in s.edges()]
    
    # Desenhar o grafo
    nx.draw(s, pos, 
            with_labels=True, 
            node_color='skyblue', 
            node_size=1500, 
            font_size=10,
            font_weight='bold',
            edge_color='blue',
            alpha=0.7,
            width=pesos)
    # Adicionar rótulos de peso às arestas
    labels_pesos = nx.get_edge_attributes(s, 'weight')
    nx.draw_networkx_edge_labels(s, pos, edge_labels=labels_pesos)
    # Adicionar título ao grafo
    plt.title("Grafo de Similaridade entre Alunos")
    plt.show()
    
    return s

grafo_sim = gerar_grafo_similaridade(matriz_sim)

def gerar_grafo_coocorrencia(matriz_co):
    # Criar o grafo a partir da matriz de coocorrência
    c = nx.from_pandas_adjacency(matriz_co)

    # Remover arestas com peso zero
    arestas_zero = []

    # Percorre todas as arestas com seus atributos
    for u, v, data in c.edges(data=True):
        peso = data.get('weight', 0)
        if peso == 0:
            arestas_zero.append((u, v))
    c.remove_edges_from(arestas_zero)
    # Remover auto-laços
    c.remove_edges_from(nx.selfloop_edges(c))

    plt.figure(figsize=(12, 10))
    # Definir a posição dos nós usando o layout spring
    pos = nx.spring_layout(c, k=3.5, iterations=100, seed=42) 
    # Obter os pesos das arestas para definir a largura
    pesos = []

    # Itera sobre os pares de nós que formam as arestas
    for u, v in c.edges():
        peso = c[u][v]['weight']
        
        pesos.append(peso)
    # Desenhar o grafo
    nx.draw(c, pos, 
            with_labels=True, 
            node_color='lightgreen',
            node_size=1800, 
            font_size=10,
            font_weight='bold',
            edge_color='green',
            alpha=0.6,
            width=pesos)
    # Adicionar rótulos de peso às arestas
    labels_pesos = nx.get_edge_attributes(c, 'weight')
    nx.draw_networkx_edge_labels(c, pos, edge_labels=labels_pesos)
    
    # Adicionar título ao grafo
    plt.title("Grafo de Coocorrência (Relação entre Gêneros)")
    plt.show()
    
    return c
grafo_co = gerar_grafo_coocorrencia(matriz_co)

def calcular_metricas(grafo, nome_do_grafo):
    print(f"MÉTRICAS: {nome_do_grafo}")
    print("="*40)

    #contagem do número de vértices e arestas
    num_nos = grafo.number_of_nodes()
    num_arestas = grafo.number_of_edges()
    
    print(f"- Número de Vértices (Nós): {num_nos}")
    print(f"- Número de Arestas (Ligações): {num_arestas}")

    print(f"\nArestas: {list(grafo.edges())}\n")

    # Cria a lista de graus percorrendo o grafo
    graus = []
    for node, grau in grafo.degree():
        graus.append(grau)

    # Calcula a média verificando se a lista não está vazia
    if len(graus) > 0:
        grau_medio = np.mean(graus)
    else:
        grau_medio = 0
    
    print(f"- Grau Médio: {grau_medio:.4f}")
    max_grau = max(graus) if np.degrees else 0
    print(f"- Grau Máximo encontrado: {max_grau}")

    pesos = []
    #Força de conectividade média (peso médio das arestas)
    for u, v, data in grafo.edges(data=True):
        peso = data.get('weight', 1)
    
        pesos.append(peso)
    if pesos:
        media_pesos = np.mean(pesos)
        print(f"- Força de Conectividade Média (Peso Médio): {media_pesos:.4f}")
    else:
        print("- Força de Conectividade Média: 0 (Grafo sem pesos)")

    pesos = [d.get('weight', 1) for u, v, d in grafo.edges(data=True)]
    print(f"- Pesos das arestas: {pesos}")

    #Densidade da rede
    densidade = nx.density(grafo)
    print(f"- Densidade da Rede: {densidade:.4f}")
    
    print("\n")

# 1. Métricas do Grafo de Incidência
calcular_metricas(grafo_inc, "Grafo de Incidência (Alunos -> Filmes)")

# 2. Métricas do Grafo de Similaridade
calcular_metricas(grafo_sim, "Grafo de Similaridade (Entre Alunos)")

# 3. Métricas do Grafo de Coocorrência
calcular_metricas(grafo_co, "Grafo de Coocorrência (Entre Gêneros)")