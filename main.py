import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import io

# Seus dados originais
csv_data = """from,to,weight
Bianca,Animação,1
Bianca,Comédia,1
Bianca,Drama,1
Bianca,Super-Herói,1
Bianca,Fantasia,1
Rafael,Comédia,1
Rafael,Ação,1
Rafael,Super-Herói,1
Henrique,Suspense,1
Henrique,Terror,1
Henrique,SciFi,1
Douglas,SciFi,1
Douglas,Drama,1
Douglas,Horror,1
William,Terror,1
William,Horror,1
William,SciFi,1
William,Fantasia,1
Jéssica,SciFi,1
Jéssica,Super-Herói,1
Jéssica,Animação,1
Jéssica,Época,1
Matheus,SciFi,1
Matheus,Super-Herói,1
Matheus,Animação,1
Paulinho,Policial,1
Paulinho,Ficção,1
Paulinho,Ação,1"""

# 1. Carregar os dados
df = pd.read_csv(io.StringIO(csv_data))

# 2. Adicionar alunos fictícios para chegar a 10 (Regra do exercício)
novos_alunos = pd.DataFrame({
    'from': ['Ana', 'Ana', 'Carlos', 'Carlos'],
    'to': ['Drama', 'Romance', 'Ação', 'SciFi'],
    'weight': [1, 1, 1, 1]
})
df_completo = pd.concat([df, novos_alunos], ignore_index=True)

# 3. Gerar a Matriz (Crosstab faz a contagem cruzada automaticamente)
matriz = pd.crosstab(df_completo['from'], df_completo['to'])
print("--- Matriz Gerada ---")
print(matriz)

# 4. Gerar o Grafo Visual
G = nx.from_pandas_edgelist(df_completo, 'from', 'to')

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.3) # Layout elástico

# Desenhar com cores diferentes para Alunos e Gêneros
alunos = df_completo['from'].unique()
generos = df_completo['to'].unique()

nx.draw_networkx_nodes(G, pos, nodelist=alunos, node_color='skyblue', label='Alunos', node_size=1000)
nx.draw_networkx_nodes(G, pos, nodelist=generos, node_color='lightgreen', label='Gêneros', node_size=1000, node_shape='s')
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos)

plt.legend()
plt.title("Rede de Preferências de Filmes")
plt.show()