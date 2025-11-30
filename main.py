import pandas as pd
import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt

def carregar_excel(arquivo):
    if not os.path.exists(arquivo):
            print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
            print("Dica: Verifique se o nome está correto (ex: 'Dado.xlsx') e se está na mesma pasta do script.")
            return None
        
    try:
        df = pd.read_excel(arquivo, engine='openpyxl')
        print(f"Sucesso! '{arquivo}' carregado com {len(df)} linhas.")
        return df
    except Exception as e:
        print(f"Erro ao ler: {e}")
        return None

dados = carregar_excel('Dados.xlsx')
print(dados)

print("\n")
def gerar_matriz_incidencia(df):
    matriz = pd.crosstab(df['from'], df['to'])
    
    return matriz

matriz_inc = gerar_matriz_incidencia(dados)

print(matriz_inc)
print("\n")
def gerar_matriz_similaridade(matriz_inc):
    matriz_sim = matriz_inc.dot(matriz_inc.T)
    np.fill_diagonal(matriz_sim.values, 0)
    
    return matriz_sim

matriz_sim = gerar_matriz_similaridade(matriz_inc)

print(matriz_sim)

def gerar_matriz_coocorrencia(matriz_inc):
    matriz_co = matriz_inc.T.dot(matriz_inc)

    np.fill_diagonal(matriz_co.values, 0)
    
    return matriz_co
matriz_co = gerar_matriz_coocorrencia(matriz_inc)

print(matriz_co)

print("\n")
def gerar_grafo_incidencia(df):
    G = nx.from_pandas_edgelist(df, source='from', target='to', edge_attr='weight', create_using=nx.DiGraph())

    plt.figure(figsize=(12, 8))
    

    pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42) 
    
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
    s = nx.from_pandas_adjacency(matriz_sim)

    arestas_zero = [(u, v) for u, v, d in s.edges(data=True) if d.get('weight', 0) == 0]
    s.remove_edges_from(arestas_zero)

    plt.figure(figsize=(14, 12))

    pos = nx.spring_layout(s, k=3.5, iterations=100, seed=42)
    
    pesos = [s[u][v]['weight'] for u, v in s.edges()]
    

    nx.draw(s, pos, 
            with_labels=True, 
            node_color='skyblue', 
            node_size=1500, 
            font_size=10,
            font_weight='bold',
            edge_color='blue',
            alpha=0.7,
            width=pesos)
    
    labels_pesos = nx.get_edge_attributes(s, 'weight')
    nx.draw_networkx_edge_labels(s, pos, edge_labels=labels_pesos)
            
    plt.title("Grafo de Similaridade entre Alunos")
    plt.show()
    
    return s

grafo_sim = gerar_grafo_similaridade(matriz_sim)

def gerar_grafo_coocorrencia(matriz_co):
    c = nx.from_pandas_adjacency(matriz_co)

    arestas_zero = [(u, v) for u, v, d in c.edges(data=True) if d.get('weight', 0) == 0]
    c.remove_edges_from(arestas_zero)

    c.remove_edges_from(nx.selfloop_edges(c))

    plt.figure(figsize=(12, 10))
    
    pos = nx.spring_layout(c, k=3.5, iterations=100, seed=42) 

    pesos = [c[u][v]['weight'] for u, v in c.edges()]

    nx.draw(c, pos, 
            with_labels=True, 
            node_color='lightgreen',
            node_size=1800, 
            font_size=10,
            font_weight='bold',
            edge_color='green',
            alpha=0.6,
            width=pesos)
    
    labels_pesos = nx.get_edge_attributes(c, 'weight')
    nx.draw_networkx_edge_labels(c, pos, edge_labels=labels_pesos)
            
    plt.title("Grafo de Coocorrência (Relação entre Gêneros)")
    plt.show()
    
    return c

grafo_co = gerar_grafo_coocorrencia(matriz_co)

def calcular_metricas(grafo, nome_do_grafo):
    print(f"MÉTRICAS: {nome_do_grafo}")
    print("="*40)

    num_nos = grafo.number_of_nodes()
    num_arestas = grafo.number_of_edges()
    
    print(f"- Número de Vértices (Nós): {num_nos}")
    print(f"- Número de Arestas (Ligações): {num_arestas}")

    graus = [grau for node, grau in grafo.degree()]
    grau_medio = np.mean(graus) if np.degrees else 0
    
    print(f"- Grau Médio: {grau_medio:.4f}")
    max_grau = max(graus) if np.degrees else 0
    print(f"- (Grau Máximo encontrado: {max_grau})")

    pesos = [d.get('weight', 1) for u, v, d in grafo.edges(data=True)]
    
    if pesos:
        media_pesos = np.mean(pesos)
        print(f"- Força de Conectividade Média (Peso Médio): {media_pesos:.4f}")
    else:
        print("- Força de Conectividade Média: 0 (Grafo sem pesos)")

    densidade = nx.density(grafo)
    print(f"- Densidade da Rede: {densidade:.4f}")
    
    print("\n")

# 1. Métricas do Grafo de Incidência
# (Nota: Em grafos direcionados, a densidade considera idas e vindas)
calcular_metricas(grafo_inc, "Grafo de Incidência (Alunos -> Filmes)")

# 2. Métricas do Grafo de Similaridade
calcular_metricas(grafo_sim, "Grafo de Similaridade (Entre Alunos)")

# 3. Métricas do Grafo de Coocorrência
calcular_metricas(grafo_co, "Grafo de Coocorrência (Entre Gêneros)")