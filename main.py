# Implementação Projeto 1 - Teoria dos Grafos
# Joaquim Rafael M. P. Pereira 10408805
# Antonio Carlos Sciamarelli Neto 10409160
# Henrique Arabe Neres de Farias 10410152

import classes.filaCircular as fc
import classes.grafoLista as gl
import classes.grafoMatriz as gm
import classes.pilha as p
from collections import defaultdict

class TGrafoMatrizD(gm.Grafo):
    def __init__(self):
        self.vertices = []
        self.indices = {}
        self.matriz = [] 

    def inserirVertice(self, codigo, pais, media_voos):
        if codigo not in self.indices:
            self.vertices.append({'codigo': codigo, 'pais': pais, 'media_voos': media_voos})
            idx = len(self.vertices) - 1
            self.indices[codigo] = idx
            for linha in self.matriz:
                linha.append(None)
            self.matriz.append([None] * len(self.vertices))

    def removerVertice(self, codigo):
        if codigo in self.indices:
            idx = self.indices[codigo]
            del self.vertices[idx]
            del self.matriz[idx]
            for linha in self.matriz:
                del linha[idx]
            del self.indices[codigo]
            self.indices = {v['codigo']: i for i, v in enumerate(self.vertices)}

    def adicionarAresta(self, origem, destino, distancia, tempo_voo):
        if origem in self.indices and destino in self.indices:
            i = self.indices[origem]
            j = self.indices[destino]
            self.matriz[i][j] = (distancia, tempo_voo)

    def removerAresta(self, origem, destino):
        if origem in self.indices and destino in self.indices:
            i = self.indices[origem]
            j = self.indices[destino]
            self.matriz[i][j] = None

    def mostrarGrafo(self):
        codigos = [v['codigo'] for v in self.vertices]
        coluna = 13
        print("Matriz de Adjacência:")
        print("      " + "  ".join(f"{c:>8}" for c in codigos))

        header = "     " + "".join(c.ljust(coluna) for c in codigos)
        print(header)

        for i, linha in enumerate(self.matriz):
            linha_formatada = codigos[i].ljust(5)
            for valor in linha:
                if valor is None:
                    linha_formatada += "-".ljust(coluna)
                else:
                    dist, tempo = valor
                    conteudo = f"{dist}mi {tempo}"
                    linha_formatada += conteudo.ljust(coluna)
            
            print(linha_formatada)

    def lerArquivo(nome_arquivo):
        grafo = TGrafoMatrizD()

        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]

            tipo_grafo = linhas[0]
            n = int(linhas[1])

            paises = []

            for i in range(2, 2 + n):
                partes = linhas[i].split('"')
                codigo = partes[1]
                pais = partes[3]
                media_voos = float(partes[5])
                grafo.inserirVertice(codigo, pais, media_voos)
                paises.append(pais)

            m = int(linhas[2 + n])

            for i in range(3 + n, len(linhas)):
                partes = linhas[i].split()
                origem, destino = partes[0].split('_')
                distancia = int(partes[1])
                tempo_voo = f"{partes[2]} {partes[3]}"
                grafo.adicionarAresta(origem, destino, distancia, tempo_voo)
        
        return grafo
    
    def conexidade(self):
        def dfs(v, visitado, matriz):
            visitado.add(v)
            for i, aresta in enumerate(matriz[v]):
                if aresta is not None and i not in visitado:
                    dfs(i, visitado, matriz)

        n = len(self.vertices)

        for i in range(n):
            visitado = set()
            dfs(i, visitado, self.matriz)
            if len(visitado) != n:
                break
        else:
            return "fortemente conexo"

        matriz_nd = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if self.matriz[i][j] is not None or self.matriz[j][i] is not None:
                    matriz_nd[i][j] = 1
                    matriz_nd[j][i] = 1

        visitado = set()
        dfs(0, visitado, matriz_nd)
        if len(visitado) == n:
            return "fracamente conexo"
        else:
            return "desconexo"
        
    def grafo_reduzido(self):
        n = len(self.vertices)

        visited = set()
        order = []
    
        def dfs_order(v):
            visited.add(v)
            for i, edge in enumerate(self.matriz[v]):
                if edge is not None and i not in visited:
                    dfs_order(i)
            order.append(v)
    
        for v in range(n):
            if v not in visited:
                dfs_order(v)
    
        transposed = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if self.matriz[i][j] is not None:
                    transposed[j][i] = self.matriz[i][j]
    
        visited.clear()
        components = []
    
        def dfs_component(v, comp):
            visited.add(v)
            comp.append(v)
            for i, edge in enumerate(transposed[v]):
                if edge is not None and i not in visited:
                    dfs_component(i, comp)
    
        while order:
            v = order.pop() 
            if v not in visited:
                comp = []
                dfs_component(v, comp)
                components.append(comp)
    
        vertice_to_comp = {}
        for comp_idx, comp in enumerate(components):
            for v in comp:
                vertice_to_comp[v] = comp_idx

        reduzido = defaultdict(set)
        for i in range(n):
            for j, edge in enumerate(self.matriz[i]):
                if edge is not None:
                    c1 = vertice_to_comp[i]
                    c2 = vertice_to_comp[j]
                    if c1 != c2:
                        reduzido[c1].add(c2)
    
        components_codes = []
        for comp in components:
            comp_codes = [self.vertices[v]['codigo'] for v in comp]
            components_codes.append(comp_codes)
    
        return components_codes, reduzido
            
            
    
def mostrarArquivo(nome_arquivo):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                print("Conteúdo do arquivo txt:")
                print("-" * 40)
                print(conteudo)
                print("-" * 40)
        except FileNotFoundError:
            print(f"Arquivo '{nome_arquivo}' não encontrado.")

def gravarArquivo(grafo, nome_arquivo, tipo_grafo=7):

    arestas = []

    for i, linha in enumerate(grafo.matriz):
        for j, valor in enumerate(linha):
            if valor is not None:
                origem = grafo.vertices[i]['codigo']
                destino = grafo.vertices[j]['codigo']
                distancia, tempo = valor
                arestas.append(f"{origem}_{destino} {distancia} {tempo}")
    
    print(len(arestas))
    
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(f"{tipo_grafo}\n")
        arquivo.write(f"{len(grafo.vertices)}\n")

        for i, v in enumerate(grafo.vertices):
            codigo = v['codigo']
            pais = v['pais']
            media_voos = v['media_voos']
            arquivo.write(f'{i} "{codigo}" "{pais}" "{media_voos}"\n')


        arquivo.write(f"{len(arestas)}\n")

        for linha in arestas:
            arquivo.write(linha + "\n")


def main():
    while True:
        print("\nProjeto 1 - Teoria dos Grafos - Rede internacional de voos a longas distancias\n")
        print("1-Ler dados do arquivo grafo.txt");
        print("2-Gravar dados no arquivo grafo.txt");
        print("3-Inserir vértice");
        print("4-Inserir aresta");
        print("5-Remove vértice");
        print("6-Remove aresta");
        print("7-Mostrar conteúdo do arquivo");
        print("8-Mostrar grafo");
        print("9-Apresentar a conexidade do grafo e o reduzido");
        print("10-Encerrar a aplicação");
        print("\nDigite a opção desejada: ");
        opcao = int(input())
        match opcao:
            case 1:
                filename = "grafo.txt"
                grafo = TGrafoMatrizD.lerArquivo(filename)
                print("Arquivo Lido!")
                continue
            case 2:
                filename = "grafo.txt"
                gravarArquivo(grafo, filename)
                continue
            case 3:
                print("Código do aeroporto: ")
                codigo = input()
                print("País do aeroporto: ")
                pais = input()
                print("Média de voos: ")
                voos = float(input())
                grafo.inserirVertice(codigo, pais, voos)
                continue
            case 4:
                print("Origem da aresta: ")
                origem = input()
                print("Destino da aresta: ")
                destino = input()
                print("Distancia: ")
                distancia = float(input())
                print("Tempo do voo: ")
                tempo = input()
                grafo.adicionarAresta(origem, destino, distancia, tempo)
                continue
            case 5:
                print("Código do aeroporto a ser removido: ")
                remove = input()
                grafo.removerVertice(remove)
                continue
            case 6:
                print("Origem da aresta a ser removida: ")
                origem = input()
                print("Destino da aresta a ser removida: ")
                destino = input()
                grafo.removerAresta(origem, destino)
                continue
            case 7:
                filename2 = "grafo.txt"
                mostrarArquivo(filename2)
                continue
            case 8:
                grafo.mostrarGrafo()
                continue
            case 9:
                print("Conexidade do grafo: ", grafo.conexidade())
                componentes, reduzido = grafo.grafo_reduzido()

                print("Componentes Fortemente Conexos:")
                for idx, comp in enumerate(componentes):
                    print(f"Componente {idx}: {comp}")

                print("\nGrafo Reduzido (arestas entre componentes):")
                for origem, destinos in reduzido.items():
                    for destino in destinos:
                        print(f"C{origem} -> C{destino}")
                continue
            case 10:
                print("Finalizando...")
                break
            case _:
                print("Opção inválida")
                continue
        

if __name__ == '__main__':
    main()
