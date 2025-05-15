# Usado em Projeto 2 - Teoria dos Grafos por:
# Joaquim Rafael M. P. Pereira 10408805
# Antonio Carlos Sciamarelli Neto 10409160
# Henrique Arabe Neres de Farias 10410152

#Atualizações:
#24/03/2025 - Itens 1, 3, 4, 5, 6 e 8 do menu feitos baseados em um exemplo especifico apenas para a realização do código 
#25/03/2025 - Itens 2, 7 e 9 feitos baseados no mesmo exemplo de antes
#26/03/2025 - Montagem do arquivo grafo.txt com os dados do nosso grafo final e modificações nas funções (apenas mudança na leitura do arquivo e armazenamento para se adequar ao formato correto)
#27/03/2025 - Finalização do código e testes com o arquivo grafo.txt final
#30/03/2025 - Última revisão do código e adição dos comentários explicando as funções e o funcionamento geral do código
#12/05/2025 - Itens 1 e 2 da Atividade Projeto 2 baseados no material dado em aula
#14/05/2025 - Finalização do código, print dos resultados, e fechamento do relatório

import re
import math
import grafoMatriz as gm
from collections import defaultdict

def parse_tempo(s: str) -> int:
    h = re.search(r'(\d+)h', s)
    m = re.search(r'(\d+)m', s)
    return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)


class TGrafoMatrizD(gm.Grafo):
    def __init__(self):
        super().__init__()
        self.vertices = []
        self.indices  = {}
        self.matriz   = []

    # --- inserção/remover vértices e arestas ---
    def inserirVertice(self, codigo, pais, media_voos):
        if codigo not in self.indices:
            self.vertices.append({
                'codigo': codigo,
                'pais': pais,
                'media_voos': media_voos
            })
            idx = len(self.vertices) - 1
            self.indices[codigo] = idx
            # expande matriz
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
            self.indices = {
                v['codigo']: i
                for i, v in enumerate(self.vertices)
            }

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
        largura = max(len(c) for c in codigos) + 3
        print("Matriz de Adjacência:")
        print("     " + "".join(c.ljust(largura) for c in codigos))
        for i, linha in enumerate(self.matriz):
            linha_fmt = codigos[i].ljust(5)
            for val in linha:
                if val is None:
                    linha_fmt += "-".ljust(largura)
                else:
                    d, t = val
                    linha_fmt += f"{d}mi {t}".ljust(largura)
            print(linha_fmt)

    # --- I/O de arquivo ---
    @staticmethod
    def lerArquivo(nome_arquivo):
        grafo = TGrafoMatrizD()
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            linhas = [l.strip() for l in f if l.strip()]
        n = int(linhas[1])
        for i in range(2, 2 + n):
            p = linhas[i].split('"')
            codigo, pais, media = p[1], p[3], float(p[5])
            grafo.inserirVertice(codigo, pais, media)
        for linha in linhas[3 + n:]:
            origdest, dist, t1, t2 = linha.split()
            o, d = origdest.split('_')
            grafo.adicionarAresta(o, d, int(dist), f"{t1} {t2}")
        return grafo

    def conexidade(self):
        def dfs(u, vis, mat):
            vis.add(u)
            for v, e in enumerate(mat[u]):
                if e is not None and v not in vis:
                    dfs(v, vis, mat)

        n = len(self.vertices)
        # forte?
        for i in range(n):
            vis = set()
            dfs(i, vis, self.matriz)
            if len(vis) != n:
                break
        else:
            return "fortemente conexo"
        # fraca?
        mat_nd = [[None]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if self.matriz[i][j] or self.matriz[j][i]:
                    mat_nd[i][j] = mat_nd[j][i] = 1
        vis = set()
        dfs(0, vis, mat_nd)
        return "fracamente conexo" if len(vis)==n else "desconexo"

    def grafo_reduzido(self):
        n = len(self.vertices)
        order, vis = [], set()
        def dfs1(u):
            vis.add(u)
            for v, e in enumerate(self.matriz[u]):
                if e is not None and v not in vis:
                    dfs1(v)
            order.append(u)
        for i in range(n):
            if i not in vis: dfs1(i)

        # transposto
        trans = [[None]*n for _ in range(n)]
        for i in range(n):
            for j, e in enumerate(self.matriz[i]):
                if e is not None:
                    trans[j][i] = e

        vis.clear()
        comps = []
        def dfs2(u, comp):
            vis.add(u); comp.append(u)
            for v, e in enumerate(trans[u]):
                if e is not None and v not in vis:
                    dfs2(v, comp)
        for u in reversed(order):
            if u not in vis:
                c = []; dfs2(u, c)
                comps.append(c)

        vert2comp = {v:i for i, comp in enumerate(comps) for v in comp}
        red = defaultdict(set)
        for u in range(n):
            for v, e in enumerate(self.matriz[u]):
                if e is not None and vert2comp[u]!=vert2comp[v]:
                    red[vert2comp[u]].add(vert2comp[v])

        comps_codes = [
            [self.vertices[v]['codigo'] for v in comp]
            for comp in comps
        ]
        return comps_codes, red

    # --- Menores caminhos (Dijkstra / Floyd) ---
    def _parse_tempo(self, s): return parse_tempo(s)

    def dijkstra(self, o, d, criterio='distancia'):
        if o not in self.indices or d not in self.indices:
            return [], math.inf
        n = len(self.vertices)
        src, dst = self.indices[o], self.indices[d]
        dist = [math.inf]*n; prev = [None]*n; dist[src]=0
        vis = set()
        for _ in range(n):
            u = min((i for i in range(n) if i not in vis), key=lambda i: dist[i], default=None)
            if u is None or dist[u]==math.inf: break
            vis.add(u)
            for v, e in enumerate(self.matriz[u]):
                if e is None: continue
                w = e[0] if criterio=='distancia' else self._parse_tempo(e[1])
                if dist[u]+w < dist[v]:
                    dist[v]=dist[u]+w; prev[v]=u
        if dist[dst]==math.inf: return [], math.inf
        path=[]; u=dst
        while u is not None:
            path.append(self.vertices[u]['codigo']); u=prev[u]
        return list(reversed(path)), dist[dst]

    def floyd_warshall(self, criterio='distancia'):
        n = len(self.vertices)
        dist = [[math.inf]*n for _ in range(n)]
        nxt  = [[None]*n for _ in range(n)]
        for i in range(n):
            dist[i][i]=0; nxt[i][i]=i
            for j, e in enumerate(self.matriz[i]):
                if e is not None:
                    w = e[0] if criterio=='distancia' else self._parse_tempo(e[1])
                    dist[i][j]=w; nxt[i][j]=j
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k]+dist[k][j] < dist[i][j]:
                        dist[i][j]=dist[i][k]+dist[k][j]
                        nxt[i][j]=nxt[i][k]
        return dist, nxt
    
    def bellman_ford(self, origem, criterio='distancia'):
        if origem not in self.indices:
            raise ValueError(f"Aeroporto de origem '{origem}' inválido.")
        n   = len(self.vertices)
        INF = float('inf')
        src = self.indices[origem]

        dist = [INF] * n
        pred = [None] * n
        dist[src] = 0

        edges = []
        for u in range(n):
            for v, e in enumerate(self.matriz[u]):
                if e is not None:
                    peso = e[0] if criterio == 'distancia' else self._parse_tempo(e[1])
                    edges.append((u, v, peso))

        for _ in range(n - 1):
            updated = False
            for u, v, peso in edges:
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    pred[v] = u
                    updated = True
            if not updated:
                break

        for u, v, peso in edges:
            if dist[u] + peso < dist[v]:
                raise ValueError("Ciclo de peso negativo detectado.")
            
        dist_map = {
            self.vertices[i]['codigo']: dist[i]
            for i in range(n)
        }
        pred_map = {
            self.vertices[i]['codigo']: self.vertices[pred[i]]['codigo']
            for i in range(n) if pred[i] is not None
        }

        return dist_map, pred_map

    # --- Coloração e ciclos ---
    def coloracao(self):
        n = len(self.vertices); cores = {}
        for u in range(n):
            usadas = set()
            for v in range(n):
                if (self.matriz[u][v] is not None or
                    self.matriz[v][u] is not None):
                    cod = self.vertices[v]['codigo']
                    if cod in cores: usadas.add(cores[cod])
            c = 0
            while c in usadas: c += 1
            cores[self.vertices[u]['codigo']] = c
        return cores

    def maior_componente_fortes(self):
        comps, _ = self.grafo_reduzido()
        return max(comps, key=len) if comps else []

    def ciclo_hamiltoniano(self):
        n = len(self.vertices)
        seq, used = [], [False]*n
        def bt(pos):
            if pos==n:
                return self.matriz[self.indices[seq[-1]]][self.indices[seq[0]]] is not None
            for v in range(n):
                if not used[v]:
                    if pos==0 or self.matriz[self.indices[seq[-1]]][v] is not None:
                        used[v]=True; seq.append(self.vertices[v]['codigo'])
                        if bt(pos+1): return True
                        used[v]=False; seq.pop()
            return False
        for start in range(n):
            seq=[self.vertices[start]['codigo']]
            used=[False]*n; used[start]=True
            if bt(1): return seq+[seq[0]]
        return []


def mostrarArquivo(nome):
    try:
        with open(nome, 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"Arquivo '{nome}' não encontrado.")


def gravarArquivo(grafo, nome, tipo=7):
    linhas = []
    for i, row in enumerate(grafo.matriz):
        for j, e in enumerate(row):
            if e is not None:
                o = grafo.vertices[i]['codigo']
                d = grafo.vertices[j]['codigo']
                dist, t = e
                linhas.append(f"{o}_{d} {dist} {t}")
    with open(nome, 'w', encoding='utf-8') as f:
        f.write(f"{tipo}\n{len(grafo.vertices)}\n")
        for i, v in enumerate(grafo.vertices):
            f.write(f'{i} "{v["codigo"]}" "{v["pais"]}" "{v["media_voos"]}"\n')
        f.write(f"{len(linhas)}\n")
        for l in linhas:
            f.write(l + "\n")
    print("Dados gravados com sucesso!")


def main():
    grafo = None
    while True:
        print("\nProjeto 1 – Teoria dos Grafos – Rede internacional de voos\n")
        print("1- Ler dados do arquivo grafo.txt")
        print("2- Gravar dados no arquivo grafo.txt")
        print("3- Inserir vértice")
        print("4- Inserir aresta")
        print("5- Remover vértice")
        print("6- Remover aresta")
        print("7- Mostrar conteúdo do arquivo")
        print("8- Mostrar grafo")
        print("9- Conexidade e grafo reduzido")
        print("10- Dijkstra (menor caminho)")
        print("11- Floyd-Warshall (todos os caminhos mínimos)")
        print("12- Bellman–Ford (menor caminho e detecção de ciclos negativos)")
        print("13- Colorir vértices")
        print("14- Maior componente fortemente conexa")
        print("15- Detectar ciclo Hamiltoniano")
        print("16- Encerrar aplicação")

        opc = int(input("Digite a opção desejada: "))

        match opc:
            case 1:
                grafo = TGrafoMatrizD.lerArquivo("grafo.txt")
                print("Arquivo lido com sucesso!")
            case 2:
                if grafo:
                    gravarArquivo(grafo, "grafo.txt")
                else:
                    print("❗ Carregue um grafo primeiro (opção 1).")
            case 3:
                c = input("Código: "); p = input("País: ")
                v = float(input("Média de voos: "))
                grafo.inserirVertice(c, p, v)
            case 4:
                o = input("Origem: "); d = input("Destino: ")
                dist = int(input("Distância (mi): "))
                t = input("Tempo (e.g. '2h 30m'): ")
                grafo.adicionarAresta(o, d, dist, t)
            case 5:
                rm = input("Código para remover: ")
                grafo.removerVertice(rm)
            case 6:
                o = input("Origem da aresta: ")
                d = input("Destino da aresta: ")
                grafo.removerAresta(o, d)
            case 7:
                mostrarArquivo("grafo.txt")
            case 8:
                grafo.mostrarGrafo()
            case 9:
                print("Conexidade:", grafo.conexidade())
                comps, red = grafo.grafo_reduzido()
                print("Componentes Fort. Conexos:")
                for i, comp in enumerate(comps):
                    print(f"  C{i}: {comp}")
                print("Grafo Reduzido:")
                for o, ds in red.items():
                    for d in ds:
                        print(f"  C{o} -> C{d}")
            case 10:
                o = input("Origem: "); d = input("Destino: ")
                cri = input("Critério ('distancia' ou 'tempo'): ").strip().lower()
                path, cst = grafo.dijkstra(o, d, cri)
                if cst == math.inf:
                    print("Não há caminho.")
                else:
                    print(f"Caminho: {' -> '.join(path)} | Custo: {cst}")
            case 11:
                cri = input("Critério ('distancia' ou 'tempo'): ").strip().lower()
                dist_mat, _ = grafo.floyd_warshall(cri)
                print("Matriz de custos mínimos:")
                for i, row in enumerate(dist_mat):
                    o = grafo.vertices[i]['codigo']
                    for j, v in enumerate(row):
                        d = grafo.vertices[j]['codigo']
                        print(f"  {o} -> {d} = {v}")
            case 12:
                origem = input("Origem para Bellman–Ford: ")
                criterio = input("Critério ('distancia' ou 'tempo'): ").strip().lower()

                if origem not in grafo.indices:
                    print("❗ Origem inválida.")
                else:
                    try:
                        dist_map, pred_map = grafo.bellman_ford(origem, criterio)
                        print(f"Distâncias mínimas a partir de {origem}:")
                        for v, d in dist_map.items():
                           print(f"  {v}: {d}")
                        print("Predecessores:")
                        for v, p in pred_map.items():
                            print(f"  {v}: {p}")
                    except ValueError as e:
                        print(f"Erro no Bellman–Ford: {e}")
            case 13:
                cores = grafo.coloracao()
                print("Coloração (vértice: cor):")
                for v, c in cores.items():
                    print(f"  {v}: {c}")
            case 14:
                mc = grafo.maior_componente_fortes()
                print("Maior componente fortemente conexa:", mc)
            case 15:
                ciclo = grafo.ciclo_hamiltoniano()
                if ciclo:
                    print("Ciclo Hamiltoniano:", " -> ".join(ciclo))
                else:
                    print("Nenhum ciclo Hamiltoniano encontrado.")
            case 16:
                print("Encerrando…")
                break
            case _:
                print("Opção inválida.")

if __name__ == "__main__":
    main()
