from token import Token
from automato import Automato
from arvore import Arvore,No
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeros = "1234567890"
simbolos = "<>=+-*/&|:()!; "
alfabeto = letras+numeros+simbolos
# ainda está incompleta
class Gramatica:
    def __init__(self):
        self.entrada =""
        self.position = 0
        self.linha = 1
        self.token = Token("NULL","NULL",self.get_linha())
        self.automato = Automato("NULL",0)

    def set_linha(self,linha):
        self.linha = linha

    def get_linha(self):
        return self.linha
    
    def set_entrada(self,entrada):
        self.entrada = entrada
    def get_token(self):
        return self.token
    
    def formar_token(self,estado_atual,valor_token):
        token = Token("NULL","NULL",self.get_linha())
        if estado_atual == 3 or estado_atual == 5 or estado_atual == 6 or estado_atual == 9 or estado_atual == 14 or estado_atual == 16:
            #RO -> relational operator
            token = Token("RO",valor_token,self.get_linha())
        if estado_atual == 11 or estado_atual == 12:
            #MO -> multiply operator
            token = Token("MO",valor_token,self.get_linha())
        if estado_atual == 17 or estado_atual == 18:
            #AO -> adding operator
            token = Token("AO",valor_token,self.get_linha())
            #AS -> assigment symbol
        if estado_atual == 20:
            token = Token("AS",valor_token,self.get_linha())
            #not -> not
        if estado_atual == 21:
            token = Token("not",valor_token,self.get_linha())
            #AP ->open parenteses
        if estado_atual == 22:
            token = Token("OP",valor_token,self.get_linha())
        if estado_atual == 23:
            #FP -> close parenteses
            token = Token("CP",valor_token,self.get_linha())
        if estado_atual == 2:
            token = Token("ID",valor_token,self.get_linha())
        if estado_atual == 7 or estado_atual == 10:
            token = Token("RO",valor_token,self.get_linha())
        if estado_atual == 25:
            token = Token("digit",valor_token,self.get_linha())
        if estado_atual == 26:
            token = Token("EOL",valor_token,self.get_linha())
        return token
    
    def get_next_token(self):
        if self.position == len(self.entrada):
            token = Token("NULL","NULL",self.get_linha())
            self.set_token(token)
        else:
            atual_position = self.position
            estado_atual = 0
            valor_token = ""
            while atual_position != len(self.entrada):
                validador = 0
                if self.entrada[atual_position] != " ":
                    valor_token = valor_token+self.entrada[atual_position]
                estado_atual,validador = self.automato.fazer_transicao(estado_atual,self.entrada[atual_position])
                if self.automato.checar_aceitacao(estado_atual) == 1:
                    self.set_token(self.formar_token(estado_atual,valor_token))
                    estado_atual = 0
                    self.position = atual_position+1
                    break
                if validador == 0:
                    estado_atual,validador = self.automato.fazer_transicao_estrela(estado_atual,self.entrada[atual_position])
                    if validador == 1:
                        if self.entrada[atual_position] != " ":
                            valor_token = valor_token[:-1]
                        self.set_token(self.formar_token(estado_atual,valor_token))
                        estado_atual = 0
                        self.position = atual_position
                        break
                    else:
                        print("erro lexico encontrado na leitura do "+self.entrada[self.position]+" no estado: "+str(estado_atual))
                        return 0
                atual_position = atual_position + 1
                self.position = atual_position
            if self.position == len(self.entrada):
                if estado_atual == 1:
                    self.set_token(Token("ID",valor_token,self.get_linha()))
                    valor_token = ""
                elif estado_atual == 8 or estado_atual == 4:
                    self.set_token(Token("RO",valor_token,self.get_linha()))
                    valor_token = ""
                elif estado_atual == 24:
                    self.set_token(Token("digit",valor_token,self.get_linha()))
                    valor_token = ""
                elif estado_atual != 0:
                    print("erro lexico:estado atual "+ str(estado_atual))
                    return 0
    def match(self,token):
        if self.token.tipo == token:
            filho = self.token.valor
            if token == "EOL":
                self.set_linha(self.get_linha()+1)
            if self.get_next_token() == 0:
                return 0
            if self.get_token() != "NULL":
                print("token: tipo("+self.token.tipo+"),valor("+self.token.valor+"), na posição("+str(self.position)+") na linha("+str(self.token.linha)+")")
            return filho
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
        no_pai = No("NULL")
        if self.get_token().tipo == "ID":
            no_filho = self.identifier()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "identifier"
                no_pai.filhos.append(no_filho)
            no_filho = self.match("AS")
            if no_filho == 0:
                return 0
            else:
                no_pai.filhos.append(No(no_filho))
            no_filho = self.expression()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "expression"
                no_pai.filhos.append(no_filho)
            no_filho = self.match("EOL")
            if no_filho == 0:
                return 0
            else:
                no_pai.filhos.append(No(no_filho))
            
            no_filho = self.assignment()
            if no_filho == 0:
                return 0
            elif no_filho != 1:
                no_filho.valor = "assignment"
                no_pai.filhos.append(no_filho)
            return no_pai
        else:
            return 1
    
    def expression(self):
        no_pai = No("NULL")
        no_filho = self.simple_expression()
        if no_filho == 0:
            return 0
        else:
            no_filho.valor = "simple expression"
            no_pai.filhos.append(no_filho)
        no_filho = self.complemento_1()
        if no_filho == 0:
            return 0
        elif no_filho != 1:
            no_filho.valor = "complemento 1"
            no_pai.filhos.append(no_filho)
        return no_pai
    
    def complemento_1(self):
        if self.checar_final() == 0 and self.get_token().tipo == "RO":
            return 0
        elif self.checar_final != 0 and self.get_token().tipo == "RO":
            no_pai = No("NULL")
            no_filho = self.relational_operator()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "relational operator"
                no_pai.filhos.append(no_filho)
                no_filho = self.simple_expression()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "simple expression"
                no_pai.filhos.append(no_filho)
            return no_pai
        else:
            return 1

    def simple_expression(self):
        no_pai = No("NULL")
        no_filho = self.sign()
        if no_filho != 1:
            no_pai.filhos.append(no_filho)
        no_filho = self.term()
        if no_filho == 0:
            return 0
        else:
            no_filho.valor = "term"
            no_pai.filhos.append(no_filho)
        no_filho = self.complemento_2()
        if no_filho == 0:
            return 0
        elif no_filho != 1:
            no_filho.valor = "complemento 2"
            no_pai.filhos.append(no_filho)
        return no_pai

    def complemento_2(self):
        if self.checar_final == 0 and self.get_token().tipo == "AO":
            return 0
        elif self.checar_final != 0 and self.get_token().tipo == "AO":
            no_pai = No("NULL")
            no_filho = self.adding_operator()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "adding operator"
                no_pai.filhos.append(no_filho)
            no_filho = self.term()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "term"
                no_pai.filhos.append(no_filho) 
                no_filho = self.complemento_2()
                if no_filho == 0:
                    return 0
                elif no_filho != 1:
                    no_filho.valor = "complemento 2"
                    no_pai.filhos.append(no_filho)
            return no_pai
        else:
            return 1
    def term(self):
        no_pai = No("NULL")
        no_filho = self.factor()
        if no_filho == 0:
            return 0
        else:
            no_filho.valor = "factor"
            no_pai.filhos.append(no_filho)
        no_filho = self.complemento_3()
        if no_filho == 0:
            return 0
        elif no_filho !=1:
            no_filho.valor = "complemento 3"
            no_pai.filhos.append(no_filho)
        return no_pai
    def complemento_3(self):
        if self.checar_final == 0 and self.get_token().tipo == "MO":
            return 0
        elif self.checar_final != 0 and self.get_token().tipo == "MO":
            no_pai = No("NULL")
            no_filho = self.multiply_operator()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "multiply operator"
                no_pai.filhos.append(no_filho)
            no_filho = self.factor()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "factor"
                no_pai.filhos.append(no_filho) 
                no_filho = self.complemento_3()
                if no_filho == 0:
                    return 0
                elif no_filho != 1:
                    no_filho.valor = "complemento 3"
                    no_pai.filhos.append(no_filho)
            return no_pai 
        else:
            return 1
        
    def factor(self):
        if self.get_token().tipo == "ID":
            no_pai = No("NULL")
            no_filho = self.identifier()
            if no_filho == 0:
                return 0
            else:
                no_filho.valor = "identifier"
                no_pai.filhos.append(no_filho)
            return no_pai
        if self.get_token().tipo == "OP":
            no_pai = No("NULL")
            token = self.match("OP")
            if token == 0:
                return 0
            else:
                no_pai.filhos.append(No(token))
            no_filho2 = self.expression()
            if no_filho2 == 0:
                return 0
            else:
                no_filho2.valor = "Expression"
                no_pai.filhos.append(no_filho2)
            token = self.match("CP")
            if token == 0:
                return 0
            else:
                no_pai.filhos.append(No(token))
            return no_pai
        if self.get_token().tipo == "not":
            no_pai = No("null")
            token = self.match("not")
            if token == 0:
                return 0
            else:
                no_pai.filhos.append(No(token))
                no_filho = self.factor()
                if no_filho == 0:
                    return 0
                else:
                    no_filho.valor = "factor"
                    no_pai.filhos.append(no_filho)
                return no_pai
        if self.get_token().tipo == "digit":
            no_pai = No("NULL")
            token = self.match("digit")
            if token == 0:
                return 0
            else:
                no_pai.filhos.append(No(token))
            return no_pai
        else:
            return 0
                
    def identifier(self):
        no_pai = No("NULL")
        no_filho = self.match("ID")
        if no_filho == 0:
            return 0
        else:
            no_pai.filhos.append(No(no_filho))
        return no_pai
    def sign(self):
        resp = ""
        if self.get_token().tipo == "AO":
            resp = self.match("AO")
            return resp
        else:
            return 1
        
    def relational_operator(self):
        no_pai = No("NULL")
        no_filho = self.match("RO")
        if no_filho == 0:
            return 0
        else:
            no_pai.filhos.append(No(no_filho))
        return no_pai
    def adding_operator(self):
        no_pai = No("NULL")
        no_filho = self.match("AO")
        if no_filho == 0:
            return 0
        else:
            no_pai.filhos.append(No(no_filho))
        return no_pai
        
    def multiply_operator(self):
        no_pai = No("NULL")
        no_filho = self.match("MO")
        if no_filho == 0:
            return 0
        else:
            no_pai.filhos.append(No(no_filho))
        return no_pai
    def digit(self):
        no_pai = No("NULL")
        no_filho = self.match("digit")
        if no_filho == 0:
            return 0
        else:
            no_pai.filhos.append(No(no_filho))
        return no_pai
    
    def aplicar_analise(self):
        self.get_next_token()
        print("token: tipo("+self.token.tipo+"),valor("+self.token.valor+"), na posição("+str(self.position)+") na linha("+str(self.token.linha)+")")
        no_raiz = self.assignment()
        if no_raiz == 0 or self.token.tipo != "NULL":
            print("erro de sintaxe")
        elif no_raiz != 1:
            no_raiz.valor = "assigment"
            arvore = Arvore()
            arvore.definir_raiz(no_raiz)
            print("sintaxe correta")
            arvore.mostrar_arvore(arvore.raiz)
        else:
            print("entrada vazia aceita")




def criar_automato(alfabeto,qtd_estados):
    analisador_lexico = Automato(alfabeto,qtd_estados)
    analisador_lexico.adicionar_transicao(0," ",0)
    for letra in letras:
        analisador_lexico.adicionar_transicao(0,letra,1)
    for letra in letras:
        analisador_lexico.adicionar_transicao(1,letra,1)
    for numero in numeros:
        analisador_lexico.adicionar_transicao(1,numero,1)
    for simbolo in simbolos:
        analisador_lexico.adicionar_transicao_estrela(1,simbolo,2)
    #transicao do simbolo '='
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
    analisador_lexico.adicionar_transicao(0,";",26)
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
    analisador_lexico.definir_aceitacao(26)
    #analisador_lexico.mostrar_aceitacao()
    return analisador_lexico
gramatica = Gramatica()
gramatica.set_automato(criar_automato(alfabeto,27))
gramatica.set_entrada("a := b + 10;b := c;")
gramatica.aplicar_analise()
