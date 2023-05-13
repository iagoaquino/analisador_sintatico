from classes.automato import Automato
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeros = "1234567890"
simbolos = "<>=+-*/&|:"
alfabeto = letras+numeros+simbolos
def criar_automato(alfabeto,qtd_estados):
    analisador_lexico = Automato(alfabeto,qtd_estados)
    for letra in letras:
        analisador_lexico.adicionar_transicao(0,letra,1)
    for letra in letras:
        analisador_lexico.adicionar_transicao(1,letra,1)
    for numero in numeros:
        analisador_lexico.adicionar_transicao(1,numero,1)
    for simbolo in simbolos:
        analisador_lexico.adicionar_transicao_estrela(1,simbolo,2)
    analisador_lexico.adicionar_transicao(0,"=",3)
    #transição do simbolo '<'
    analisador_lexico.adicionar_transicao(0,"<",4)
    analisador_lexico.adicionar_transicao(4,"=",5)
    analisador_lexico.adicionar_transicao(4,">",6)
    for simbolo in simbolos:
        analisador_lexico.adicionar_transicao_estrela(4,simbolo,7)
    for letra in letras:
        analisador_lexico.adicionar_transicao_estrela(4,letra,7)
    for numero in numeros:
        analisador_lexico.adicionar_transicao_estrela(4,numero,7)
    #transição do simbolo '>'
    analisador_lexico.adicionar_transicao(0,">",8)
    analisador_lexico.adicionar_transicao(8,"=",9)
    for simbolo in simbolos:
        analisador_lexico.adicionar_transicao_estrela(8,simbolo,10)
    for letra in letras:
        analisador_lexico.adicionar_transicao_estrela(8,letra,10)
    for numero in numeros:
        analisador_lexico.adicionar_transicao_estrela(8,numero,10)
    #transição dos simbolos * /
    analisador_lexico.adicionar_transicao(0,"*",11)
    analisador_lexico.adicionar_transicao(0,"/",12)
    #transição do simbolo &&
    analisador_lexico.adicionar_transicao(0,"&",13)
    analisador_lexico.adicionar_transicao(13,"&",14)
    #transição do simbolo ||
    analisador_lexico.adicionar_transicao(0,"|",15)
    analisador_lexico.adicionar_transicao(15,"|",16)
    #transição do simbolo + e -
    analisador_lexico.adicionar_transicao(0,"-",17)
    analisador_lexico.adicionar_transicao(0,"+",18)
    #transição do simbolo :=
    analisador_lexico.adicionar_transicao(0,":",19)
    analisador_lexico.adicionar_transicao(19,"=",20)

    analisador_lexico.mostrar_transicoes()
    print("transições em estrela")
    #definindo os estados de aceitação
    analisador_lexico.definir_aceitacao(2)
    analisador_lexico.definir_aceitacao(3)
    analisador_lexico.definir_aceitacao(5)
    analisador_lexico.definir_aceitacao(6)
    analisador_lexico.definir_aceitacao(9)
    analisador_lexico.definir_aceitacao(11)
    analisador_lexico.definir_aceitacao(12)
    analisador_lexico.definir_aceitacao(14)
    analisador_lexico.definir_aceitacao(16)
    analisador_lexico.definir_aceitacao(17)
    analisador_lexico.definir_aceitacao(18)
    analisador_lexico.definir_aceitacao(20)
    analisador_lexico.mostrar_aceitacao()


criar_automato(alfabeto,21)