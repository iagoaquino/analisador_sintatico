from token import Token
# ainda está incompleta
class Gramatica:
    def __init__(self,position):
        self.position
        self.token = Token()
    
    def get_token(self):
        return self.token
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


      