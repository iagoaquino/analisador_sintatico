from token import Token
from automato import Automato
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeros = "1234567890"
simbolos = "<>=+-*/&|:()!"
alfabeto = letras+numeros+simbolos
# ainda está incompleta
class Gramatica:
    def __init__(self):
        self.entrada =""
        self.position = 0
        self.token = Token("NULL","NULL")
        self.automato = Automato("NULL",0)

    def set_entrada(self,entrada):
        self.entrada = entrada
    def get_token(self):
        return self.token
    
    def formar_token(self,estado_atual,valor_token):
        token = Token("NULL","NULL")
        if estado_atual == 3 or estado_atual == 5 or estado_atual == 6 or estado_atual == 9 or estado_atual == 14 or estado_atual == 16:
            #RO -> relational operator
            token = Token("RO",valor_token)
        if estado_atual == 11 or estado_atual == 12:
            #MO -> multiply operator
            token = Token("MO",valor_token)
        if estado_atual == 17 or estado_atual == 18:
            #AO -> adding operator
            token = Token("AO",valor_token)
            #AS -> assigment symbol
        if estado_atual == 20:
            token = Token("AS",valor_token)
            #not -> not
        if estado_atual == 21:
            token = Token("not",valor_token)
            #AP ->open parenteses
        if estado_atual == 22:
            token = Token("OP",valor_token)
        if estado_atual == 23:
            #FP -> close parenteses
            token = Token("CP",valor_token)
        if estado_atual == 2:
            token = Token("ID",valor_token)
        if estado_atual == 7 or estado_atual == 10:
            token = Token("RO",valor_token)
        return token
    def get_next_token(self):
        atual_position = self.position
        estado_atual = 0
        valor_token = ""
        while atual_position != len(self.entrada):
            validador = 0
            valor_token = valor_token+self.entrada[atual_position]
            estado_atual,validador = self.automato.fazer_transicao(estado_atual,self.entrada[atual_position])
            if self.automato.checar_aceitacao(estado_atual) == 1:
                self.set_token(self.formar_token(estado_atual,valor_token))
                self.position = atual_position+1
                break
            if validador == 0:
                estado_atual,validador = self.automato.fazer_transicao_estrela(estado_atual,self.entrada[atual_position])
                if validador == 1:
                    valor_token = valor_token[:-1]
                    self.set_token(self.formar_token(estado_atual,valor_token))
                    self.position = atual_position
                    break
                else:
                    print("erro lexico encontrado na leitura do "+self.entrada[self.position]+" no estado: "+str(estado_atual))
            atual_position = atual_position + 1
            self.position = atual_position
        if estado_atual == 1:
            self.set_token(Token("ID",valor_token))
            valor_token = ""
        if estado_atual == 8:
            self.set_token(Token("RO",valor_token))
            valor_token = ""
    def match(self,token):
        if self.token.tipo == token.tipo:
            return 1
        else:
            return 0
    def set_token(self,token):
        self.token = token
        
    def get_position(self):
        return self.position

    def set_position(self,position):
        self.position = position

    def set_automato(self,automato):
        self.automato = automato
    #def simple_expression():
    #def term():
    #def factor():
    #def identifier():
    #def sign():
    #def relational_operator():
    #def adding_operator():
    #def multiplying_operator():
    #def assignment():
    #def digit():
    #def plus():

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
gramatica = Gramatica()
gramatica.set_automato(criar_automato(alfabeto,24))
gramatica.set_entrada("a:=ab")
gramatica.set_position(0)
while gramatica.position != len(gramatica.entrada):
    gramatica.get_next_token()
    token_atual = gramatica.get_token()
    print("token atual: "+token_atual.tipo)
