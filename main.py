# Implementação Projeto 1 - Teoria dos Grafos
# Joaquim Rafael M. P. Pereira 10408805
# Antonio Carlos Sciamarelli Neto 10409160
# Henrique Arabe Neres de Farias 10410152

import classes.filaCircular as fc
import classes.grafoLista as gl
import classes.grafoMatriz as gm
import classes.pilha as p

def main():
    while True:
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
        print("Digite a opção desejada: ");
        opcao = int(input())
        match opcao:
            case 1:
                # gl.lerArquivo()
                continue
            case 2:
                gl.gravarArquivo()
                continue
            case 3:
                gl.inserirVertice()
                continue
            case 4:
                gl.inserirAresta()
                continue
            case 5:
                gl.removeVertice()
                continue
            case 6:
                gl.removeAresta()
                continue
            case 7:
                gl.mostrarArquivo()
                continue
            case 8:
                gl.mostrarGrafo()
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
