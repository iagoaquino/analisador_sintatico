from classes.automato import Automato
from classes.token import Token
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeros = "1234567890"
simbolos = "<>=+-*/&|:()!"
texto="a:=a*b"
tokens = []
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
    #transição do simbolo !
    analisador_lexico.adicionar_transicao(0,"!",21)
    #transição dos simbolo ()
    analisador_lexico.adicionar_transicao(0,"(",22)
    analisador_lexico.adicionar_transicao(0,")",23)

    #descomente esses codigos para printar dados do automato
    #analisador_lexico.mostrar_transicoes()
    #print("transições em estrela")
    #analisador_lexico.mostrar_transicoes_estrela()
    #definindo os estados de aceitação
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
    analisador_lexico.definir_aceitacao(21)
    analisador_lexico.definir_aceitacao(22)
    analisador_lexico.definir_aceitacao(23)
    analisador_lexico.mostrar_aceitacao()
    return analisador_lexico
def formar_token(estado_atual,valor_token):
    if estado_atual == 3 or estado_atual == 5 or estado_atual == 6 or estado_atual == 9 or estado_atual == 14 or estado_atual == 16:
        #RO -> relational operator
        token = Token("RO",valor_token)
        tokens.append(token)
        valor_token = ""
    if estado_atual == 11 or estado_atual == 12:
        #MO -> multiply operator
        token = Token("MO",valor_token)
        tokens.append(token)
        valor_token = ""
    if estado_atual == 17 or estado_atual == 18:
        #AO -> adding operator
        token = Token("AO",valor_token)
        tokens.append(token)
        valor_token = ""
        #AS -> assigment symbol
    if estado_atual == 20:
        token = Token("AS",valor_token)
        tokens.append(token)
        valor_token = ""
        #not -> not
    if estado_atual == 21:
        token = Token("not",valor_token)
        tokens.append(token)
        valor_token = ""
        #AP ->open parenteses
    if estado_atual == 22:
        token = Token("OP",valor_token)
        tokens.append(token)
        valor_token = ""
    if estado_atual == 23:
        #FP -> close parenteses
        token = Token("CP",valor_token)
        tokens.append(token)
        valor_token = ""
def gerar_tokens():
    #inicialmente cria o automato
    automato = criar_automato(alfabeto,24)
    valor_token = ""
    #define o estado inicial
    estado_atual = 0
    #percorre a entrada
    for letra in texto:
        valor_token = valor_token+letra
        validador = 0
        if automato.checar_aceitacao(estado_atual) == 1:
            validador = 1
        else:
            estado_atual,validador = automato.fazer_transicao(estado_atual,letra)
        if automato.checar_aceitacao(estado_atual) == 1:
            formar_token(estado_atual,valor_token)
            valor_token = ""
            estado_atual = 0
            validador = 1
        if validador == 0:
            estado_atual,validador = automato.fazer_transicao_estrela(estado_atual,letra)
            if validador == 1:
                valor_token = valor_token[:-1]
                if estado_atual == 2:
                    token = Token("ID",valor_token)
                    tokens.append(token)
                    valor_token = ""
                if estado_atual == 7 or estado_atual == 10:
                    token = Token("RO",valor_token)
                    tokens.append(token)
                    valor_token = ""
                valor_token = valor_token+letra
                estado_atual = 0
                estado_atual,validador = automato.fazer_transicao(estado_atual,letra)
                if automato.checar_aceitacao(estado_atual) == 1:
                    formar_token(estado_atual,valor_token)
                    valor_token = ""
                    estado_atual = 0
            else:
                # caso ele não tenha sido capaz de fazer a transição comun ou estrela significa que a letra não tem transição naquele estado significando erro lexico
                print("erro lexico encontrado, na leitura do:"+letra+" no estado: "+str(estado_atual))
    #ao final caso ele tenha terminado porém não guardado o ultimo token por conta do final do texto é feito o ultimo teste
    if estado_atual == 1:
        token = Token("ID",valor_token)
        tokens.append(token)
        valor_token = ""
    if estado_atual == 8:
        token = Token("RO",valor_token)
        tokens.append(token)
        valor_token = ""
#chamando todo codigo anterior
gerar_tokens()
print("entrada:"+texto)
for token in tokens:
    print("tipo do token:"+token.tipo+"<>valor do token:"+token.valor)



