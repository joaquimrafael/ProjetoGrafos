# Implementação Projeto 1 - Teoria dos Grafos
# Joaquim Rafael M. P. Pereira 10408805
# Antonio Carlos Sciamarelli Neto 10409160
# Henrique Arabe Neres de Farias 10410152

import classes.filaCircular as fc
import classes.grafoLista as gl
import classes.grafoMatriz as gm
import classes.pilha as p

class TGrafoMatrizD(gm.Grafo):
    def __init__(self):
        self.vertices = []
        self.indices = {}
        self.matriz = [] 

    def inserirVertice(self, nome, media_voos):
        if nome not in self.indices:
            self.vertices.append({'nome': nome, 'media_voos': media_voos})
            self.indices[nome] = len(self.vertices) -1
            for linha in self.matriz:
                linha.append(None)
            self.matriz.append([None] * len(self.vertices))

    def removerVertice(self, nome):
        if nome in self.indices:
            idx = self.indices[nome]
            del self.vertices[idx]
            del self.matriz[idx]
            for linha in self.matriz:
                del linha[idx]
            del self.indices[nome]
            self.indices = {v['nome']: i for i, v in enumerate(self.vertices)}

    def adicionarAresta(self, origem, destino, distancia):
        if origem in self.indices and destino in self.indices:
            i = self.indices[origem]
            j = self.indices[destino]
            self.matriz[i][j] = distancia

    def removerAresta(self, origem, destino):
        if origem in self.indices and destino in self.indices:
            i = self.indices[origem]
            j = self.indices[destino]
            self.matriz[i][j] = None

    def mostrarGrafo(self):
        nomes = [v['nome'] for v in self.vertices]
        print("Matriz de Adjacência:")
        print("     " + "  ".join(f"{nome:>5}" for nome in nomes))

        for i, linha in enumerate(self.matriz):
            linha_formatada = []
            for j, valor in enumerate(linha):
                if valor is None:
                    linha_formatada.append("  -  ")
                else:
                    linha_formatada.append(f"{valor:5.0f}")
            
            print(f"{nomes[i]:>5} " + " ".join(linha_formatada))

    def lerArquivo(nome_arquivo):
        grafo = TGrafoMatrizD()

        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip() != '']

            tipo_grafo = linhas[0]
            n = int(linhas[1])

            rotulos = []

            for i in range(2, 2 + n):
                partes = linhas[i].split('"')
                id_vertice = int(partes[0].strip())
                nome = partes[1]
                media_voos = float(partes[3])
                grafo.inserirVertice(nome, media_voos)
                rotulos.append(nome)

            for i in range(2 + n, len(linhas)):
                partes = linhas[i].split()
                origem, destino = partes[0].split('_')
                distancia = float(partes[1])
                grafo.adicionarAresta(origem, destino, distancia)
        
        return grafo




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
                gl.gravarArquivo()
                continue
            case 3:
                print("Aeroporto a ser adicionado: ")
                nome = input()
                print("Média de voos: ")
                voos = float(input())
                grafo.inserirVertice(nome, voos)
                continue
            case 4:
                print("Origem da aresta: ")
                origem = input()
                print("Destino da aresta: ")
                destino = input()
                print("Distancia: ")
                distancia = float(input())
                grafo.adicionarAresta(origem, destino, distancia)
                continue
            case 5:
                print("Aeroporto a ser removido: ")
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
                gl.mostrarArquivo()
                continue
            case 8:
                grafo.mostrarGrafo()
                continue
            case 9:
                gl.conexidade()
                gl.reduzido()
                continue
            case 10:
                print("Finalizando...")
                break
            case _:
                print("Opção inválida")
                continue
        

if __name__ == '__main__':
    main()
