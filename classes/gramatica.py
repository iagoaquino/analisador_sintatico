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
        if estado_atual == 25:
            token = Token("digit",valor_token)
        return token
    def get_next_token(self):
        if self.position == len(self.entrada):
            return 0
        else:
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
                        return 0
                atual_position = atual_position + 1
                self.position = atual_position
            if self.position == len(self.entrada):
                if estado_atual == 1:
                    self.set_token(Token("ID",valor_token))
                    valor_token = ""
                elif estado_atual == 8:
                    self.set_token(Token("RO",valor_token))
                    valor_token = ""
                elif estado_atual != 0:
                    print("erro lexico:estado atual"+ str(estado_atual))
                    return 0
    def match(self,token):
        if self.token.tipo == token:
            if self.get_next_token() != 0:
                print("token: tipo("+self.token.tipo+"),valor("+self.token.valor+") na posição:"+str(self.position))
        else:
            return 0
    def checar_final(self):
        if self.position == len(self.entrada):
            return 0
        else:
            return 1
    
    def set_token(self,token):
        self.token = token

    def get_position(self):
        return self.position

    def set_position(self,position):
        self.position = position

    def set_automato(self,automato):
        self.automato = automato
    
    def assignment(self):
        if self.identifier() == 0:
            return 0
        
        if self.checar_final() == 0:
            return 0
        
        if self.match("AS") == 0:
            return 0
        
        if self.checar_final() == 0:
            return 0
        
        if self.expression() == 0:
            return 0
        return 1
    
    def expression(self):
        if self.simple_expression() == 0:
            return 0
        if self.complemento_1() == 0:
            return 0
        return 1
    
    def complemento_1(self):
        if self.checar_final() == 0 and self.get_token().tipo == "RO":
            return 0
        elif self.checar_final != 0 and self.get_token().tipo == "RO":
            self.relational_operator()
            if self.simple_expression() == 0:
                return 0
            return 1
        else:
            return 1

    def simple_expression(self):
        if self.sign() == 0:
            return 0
        if self.term() == 0:
            return 0
        if self.complemento_2() == 0:
            return 0
        return 1
    
    def complemento_2(self):
        if self.checar_final == 0 and self.get_token().tipo == "AO":
            return 0
        elif self.checar_final != 0 and self.get_token().tipo == "AO":
            self.adding_operator()
            if self.factor() == 0:
                return 0
            if self.complemento_2() == 0:
                return 0
            return 1
        else:
            return 1
    def term(self):
        if self.factor() == 0:
            return 0
        if self.complemento_3() == 0:
            return 0
        return 1
    def complemento_3(self):
        if self.checar_final == 0 and self.get_token().tipo == "MO":
            return 0
        elif self.checar_final != 0 and self.get_token().tipo == "MO":
            if self.factor() == 0:
                return 0
            if self.complemento_3() == 0:
                return 0
            return 1
        else:
            return 1
        
    def factor(self):
        if self.get_token().tipo == "ID":
            if self.identifier() == 0:
                return 0
            else:
                return 1
        if self.get_token().tipo == "OP":
            if self.match("OP") == 0:
                return 0
            if self.expression() == 0:
                return 0
            if self.match("CP") == 0:
                return 0
            else:
                return 1
        if self.get_token().tipo == "not":
            if self.match("not") == 0:
                return 0
            if self.factor() == 0:
                return 0
            else:
                return 1
        if self.get_token().tipo == "digit":
            if self.match("digit") == 0:
                return 0
            if self.get_token.valor =="-" or self.match("adding_operador") == 0:
                return 0
            else:
                return 1
                
    def identifier(self):
        if self.match("ID") == 0:
            return 0
        else:
            return 1
    def sign(self):
        if self.get_token().tipo == "AO":
            self.match("AO")
        else:
            return 1
    def relational_operator(self):
        if self.match("RO") == 0:
            return 0
        else:
            return 1
    def adding_operator(self):
        if self.match("AO") == 0:
            return 0
        else:
            return 1
    def multiply_operator(self):
        if self.match("MO") == 0:
            return 0
        else:
            return 1
    def digit(self):
        if self.match("digit") == 0:
            return 0
        else:
            return 1
    def aplicar_analise(self):
        self.get_next_token()
        print("token: tipo("+self.token.tipo+"),valor("+self.token.valor+")")
        if self.assignment() == 0:
            print("erro sintatico")
            return 0
        else:
            print("sintaxe correta")




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
    #tansição do digit 
    for numero in numeros:
        analisador_lexico.adicionar_transicao(0,numero,24)
    for numero in numeros:
        analisador_lexico.adicionar_transicao(24,numero,24)
    for letra in letras:
        analisador_lexico.adicionar_transicao_estrela(24,letra,25)
    for simbolo in simbolos:
        analisador_lexico.adicionar_transicao_estrela(24,simbolo,25)

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
gramatica.set_automato(criar_automato(alfabeto,26))
gramatica.set_entrada("b:=a+b+c>b")
gramatica.aplicar_analise()
