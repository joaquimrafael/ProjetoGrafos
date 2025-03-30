# Implementação Projeto 1 - Teoria dos Grafos
# Joaquim Rafael M. P. Pereira 10408805
# Antonio Carlos Sciamarelli Neto 10409160
# Henrique Arabe Neres de Farias 10410152

#Atualizações:
#24/03/2025 - Itens 1, 3, 4, 5, 6 e 8 do menu feitos baseados em um exemplo especifico apenas para a realização do código 
#25/03/2025 - Itens 2, 7 e 9 feitos baseados no mesmo exemplo de antes
#26/03/2025 - Montagem do arquivo grafo.txt com os dados do nosso grafo final e modificações nas funções (apenas mudança na leitura do arquivo e armazenamento para se adequar ao formato correto)
#27/03/2025 - Finalização do código e testes com o arquivo grafo.txt final
#30/03/2025 - Última revisão do código e adição dos comentários explicando as funções e o funcionamento geral do código 

import grafoMatriz as gm
from collections import defaultdict

class TGrafoMatrizD(gm.Grafo):
    def __init__(self):
        self.vertices = []
        self.indices = {}
        self.matriz = [] 

    def inserirVertice(self, codigo, pais, media_voos):
        #Verifica se o código fornecido já não existe dentro do grafo
        if codigo not in self.indices:
            #Armazena as informações passadas dentro do vetor de vértices
            self.vertices.append({'codigo': codigo, 'pais': pais, 'media_voos': media_voos})
            idx = len(self.vertices) - 1
            self.indices[codigo] = idx
            #For para adicionar o vértice dentro da matriz
            for linha in self.matriz:
                linha.append(None)
            self.matriz.append([None] * len(self.vertices))

    def removerVertice(self, codigo):
        #Verifica de o código passada existe no grafo
        if codigo in self.indices:
            idx = self.indices[codigo]
            #Deleta as informações do vértice, do vetor e da matriz
            del self.vertices[idx]
            del self.matriz[idx]
            for linha in self.matriz:
                del linha[idx]
            del self.indices[codigo]
            self.indices = {v['codigo']: i for i, v in enumerate(self.vertices)}

    def adicionarAresta(self, origem, destino, distancia, tempo_voo):
        #Verifica se a origem e o destino existem dentro do grafo
        if origem in self.indices and destino in self.indices:
            #Adiciona o valor da aresta na posição correspondente dentro da matriz
            i = self.indices[origem]
            j = self.indices[destino]
            self.matriz[i][j] = (distancia, tempo_voo)

    def removerAresta(self, origem, destino):
        #Verifica se existe uma aresta com essa origem e destino
        if origem in self.indices and destino in self.indices:
            #Remove o valor da aresta da matriz
            i = self.indices[origem]
            j = self.indices[destino]
            self.matriz[i][j] = None

    def mostrarGrafo(self):
        #Armazena os códigos salvos em um vetor para ser usado na hora de imprimir a matriz
        codigos = [v['codigo'] for v in self.vertices]
        coluna = 13
        print("Matriz de Adjacência:")
        print("      " + "  ".join(f"{c:>8}" for c in codigos))

        header = "     " + "".join(c.ljust(coluna) for c in codigos)
        print(header)

        #Looping for para formatar a imprimir as linhas da matriz de forma que fique fácil a a vizualização
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

        #Abre o arquivo em modo de leitura
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]

            #Armazena o tipo do grafo e o número de vértices (n)
            tipo_grafo = linhas[0]
            n = int(linhas[1])

            #Vetor para armazenar o nome do país em que o aeroporto se localiza
            paises = []

            #Le as linhas baseadas no valor de n para ler todos os vértices e guardar as informações de código, país e média de voos
            for i in range(2, 2 + n):
                partes = linhas[i].split('"')
                codigo = partes[1]
                pais = partes[3]
                media_voos = float(partes[5])
                grafo.inserirVertice(codigo, pais, media_voos)
                paises.append(pais)

            #Armazena em m o número de arestas
            m = int(linhas[2 + n])

            #For que percorre o restante das linhas para armazenar as informações de destino, origem, distancia e tempo presente na aresta
            for i in range(3 + n, len(linhas)):
                partes = linhas[i].split()
                origem, destino = partes[0].split('_')
                distancia = int(partes[1])
                tempo_voo = f"{partes[2]} {partes[3]}"
                grafo.adicionarAresta(origem, destino, distancia, tempo_voo)
        
        return grafo
    
    def conexidade(self):
        # Função que verifica a conectividade do grafo dirigido.
        # Retorna:
        # - "fortemente conexo" se para todo vértice há caminho para todos os demais;
        # - "fracamente conexo" se o grafo, quando considerado como não-dirigido, é conexo;
        # - "desconexo" caso contrário.
        def dfs(v, visitado, matriz):
            # Busca em profundidade (DFS) recursiva a partir do vértice 'v'.
            # 'visitado' é um conjunto que registra os vértices já visitados.
            # 'matriz' representa a matriz de adjacência do grafo a ser percorrido.
            visitado.add(v)
            for i, aresta in enumerate(matriz[v]):
                # Se há uma aresta saindo de 'v' para 'i' e 'i' ainda não foi visitado,
                # realiza DFS a partir de 'i'.
                if aresta is not None and i not in visitado:
                    dfs(i, visitado, matriz)

        n = len(self.vertices)

        # Verifica se o grafo é fortemente conexo:
        # Para cada vértice, executa DFS para verificar se é possível alcançar todos os outros.
        for i in range(n):
            visitado = set()
            dfs(i, visitado, self.matriz)
            if len(visitado) != n:
                # Se a partir de algum vértice não é possível alcançar todos os outros,
                # o grafo não é fortemente conexo; sai do laço.
                break
        else:
            return "fortemente conexo"

        # Converte o grafo dirigido em um grafo não-dirigido para testar a conectividade fraca.
        # Cria uma nova matriz onde, se existir uma aresta em qualquer direção entre i e j,
        # uma conexão é estabelecida entre eles.
        matriz_nd = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if self.matriz[i][j] is not None or self.matriz[j][i] is not None:
                    matriz_nd[i][j] = 1
                    matriz_nd[j][i] = 1

        # Realiza DFS no grafo não-dirigido a partir do vértice 0 para verificar a conectividade.
        visitado = set()
        dfs(0, visitado, matriz_nd)
        if len(visitado) == n:
            return "fracamente conexo"
        else:
            return "desconexo"
        
    def grafo_reduzido(self):
        # Função que constrói o grafo reduzido, ou seja, o grafo dos componentes fortemente conexos.
        # Retorna uma tupla contendo:
        # - Uma lista com os códigos (atributo 'codigo') dos vértices de cada componente fortemente conexa.
        # - Um dicionário que representa o grafo reduzido, onde cada chave é o índice do componente
        #   e o valor é um conjunto com os índices dos componentes adjacentes.
        n = len(self.vertices)

        visited = set()
        order = []
    
        def dfs_order(v):
            # DFS que registra a ordem de finalização dos vértices.
            # Essa ordem é utilizada para identificar os componentes fortemente conexos.
            visited.add(v)
            for i, edge in enumerate(self.matriz[v]):
                if edge is not None and i not in visited:
                    dfs_order(i)
            order.append(v)

        # Realiza DFS para todos os vértices que ainda não foram visitados e preenche a lista 'order'.
        for v in range(n):
            if v not in visited:
                dfs_order(v)

        # Cria a matriz transposta do grafo, invertendo a direção de todas as arestas.
        transposed = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if self.matriz[i][j] is not None:
                    transposed[j][i] = self.matriz[i][j]
    
        visited.clear()
        components = []
    
        def dfs_component(v, comp):
            # DFS na matriz transposta para coletar todos os vértices que pertencem
            # ao mesmo componente fortemente conexo.
            visited.add(v)
            comp.append(v)
            for i, edge in enumerate(transposed[v]):
                if edge is not None and i not in visited:
                    dfs_component(i, comp)

        # Processa os vértices na ordem inversa da finalização (armazenada em 'order')
        while order:
            v = order.pop() 
            if v not in visited:
                comp = []
                dfs_component(v, comp)
                components.append(comp)

        # Mapeia cada vértice para o índice do componente ao qual ele pertence.
        vertice_to_comp = {}
        for comp_idx, comp in enumerate(components):
            for v in comp:
                vertice_to_comp[v] = comp_idx

        # Constrói o grafo reduzido:
        # Para cada aresta do grafo original, se os vértices de origem e destino pertencerem a
        # componentes diferentes, adiciona uma aresta entre esses componentes.
        reduzido = defaultdict(set)
        for i in range(n):
            for j, edge in enumerate(self.matriz[i]):
                if edge is not None:
                    c1 = vertice_to_comp[i]
                    c2 = vertice_to_comp[j]
                    if c1 != c2:
                        reduzido[c1].add(c2)

        # Cria uma lista que contém os códigos dos vértices (atributo 'codigo')
        # para cada componente fortemente conexo encontrado.
        components_codes = []
        for comp in components:
            comp_codes = [self.vertices[v]['codigo'] for v in comp]
            components_codes.append(comp_codes)
    
        return components_codes, reduzido
            
            
    
def mostrarArquivo(nome_arquivo):
        #Dentro do try/except ele abre o arquivo em modo de leitura e printa todas as linhas presentes
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

    #Vetor para guardar as arestas presentes no grafo
    arestas = []

    #Looping que percorre todas as arestas buscando a origem, destino e distancia e guardando no vetor arestas
    for i, linha in enumerate(grafo.matriz):
        for j, valor in enumerate(linha):
            if valor is not None:
                origem = grafo.vertices[i]['codigo']
                destino = grafo.vertices[j]['codigo']
                distancia, tempo = valor
                arestas.append(f"{origem}_{destino} {distancia} {tempo}")
    
    print("Dados gravados com sucesso!")

    #O arquivo é aberto no modo de escrita
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        #As duas primeiras linhas são preenchidas com o tipo do grafo (7) e o número de vértices (n)
        arquivo.write(f"{tipo_grafo}\n")
        arquivo.write(f"{len(grafo.vertices)}\n")

        #Percorre todos os vértices do grafo e grava no arquivo no formato adequado
        for i, v in enumerate(grafo.vertices):
            codigo = v['codigo']
            pais = v['pais']
            media_voos = v['media_voos']
            arquivo.write(f'{i} "{codigo}" "{pais}" "{media_voos}"\n')

        #Escreve no arquivo as arestas que foram armazenadas anteriormente
        arquivo.write(f"{len(arestas)}\n")

        for linha in arestas:
            arquivo.write(linha + "\n")


def main():
    #Looping contendo as opções do menu, rodando até que o usuário escolha encerrar o programa
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
                #Cria o grafo a partir do arquivo "grafo.txt"
                filename = "grafo.txt"
                grafo = TGrafoMatrizD.lerArquivo(filename)
                print("Arquivo Lido!")
                continue
            case 2:
                #Grava o grafo atual dentro do arquivo "grafo.txt" no formato adequado 
                filename = "grafo.txt"
                gravarArquivo(grafo, filename)
                continue
            case 3:
                #O sistema pede o código, país e a média de voos diários do aeroporto que será adicionado ao grafo como um novo vértice
                print("Código do aeroporto: ")
                codigo = input()
                print("País do aeroporto: ")
                pais = input()
                print("Média de voos: ")
                voos = float(input())
                grafo.inserirVertice(codigo, pais, voos)
                continue
            case 4:
                #Aqui pede a origem (Vértice de onde a aresta vai sair), o destino (Vértice onde a aresta vai chegar), a distancia e o tempo (valores da aresta) e adiciona a aresta ao grafo
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
                #O sistema pede o código do aeroporto e com base nele remove o vértice correspondente
                print("Código do aeroporto a ser removido: ")
                remove = input()
                grafo.removerVertice(remove)
                continue
            case 6:
                #O sitema pede a origem e o destino e remove a aresta correspondente 
                print("Origem da aresta a ser removida: ")
                origem = input()
                print("Destino da aresta a ser removida: ")
                destino = input()
                grafo.removerAresta(origem, destino)
                continue
            case 7:
                #O sistema simplesmente imprime o conteúdo do arquivo "grafo.txt"
                filename2 = "grafo.txt"
                mostrarArquivo(filename2)
                continue
            case 8:
                #O sistema imprime o grafo em forma de matriz
                grafo.mostrarGrafo()
                continue
            case 9:
                #O sistema primeiramente mostra a conexidade do grafo e depois mostra os seus componentes fortemente conexos seguido do grafo reduzido
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
                #O programa é encerrado
                print("Finalizando...")
                break
            case _:
                print("Opção inválida")
                continue
        

if __name__ == '__main__':
    main()
