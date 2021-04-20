import sys
from game import * 

sys.path.insert(0, '../..')
sys.stderr = open('C:\\err.txt','w')

from sly import Lexer, Parser

class GameLexer(Lexer):

    def __init__(self):
        self.grid = game()

    tokens = { ADD, SUBTRACT, MULTIPLY, DIVIDE,
               THE,CURRENT,STATE, ARE, 
               LEFT, UP, DOWN, RIGHT,
               FULLSTOP, COMMA,
               ASSIGN,VALUE,TO,IN,IS,VARIABLE,VAR,VAL,
               ERROR}
    ignore = ' \t'

    # Token
    VAL = r'\d+'

    VALUE = r'VALUE'
    VAR = r'VAR'
    ADD = r'ADD'
    SUBTRACT = r'SUBTRACT'
    MULTIPLY = r'MULTIPLY'
    DIVIDE = r'DIVIDE'
    ASSIGN = r'ASSIGN'
    TO = r'TO'
    IS = r'IS'
    IN = r'IN'

    RIGHT = r'RIGHT'
    UP = r'UP'
    LEFT = r'LEFT'
    DOWN = r'DOWN'
    
    THE = r'The'
    CURRENT = r'current'
    STATE = r'state'
    ARE = r'is'

    VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'
    #SYMBOLS
    FULLSTOP = r'\.'
    COMMA = r'\,'


    # Ignored fgdklfjgkdfjgkjdfj
    ignore_newline = r'\n+'

    # Extra action for newlines
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        self.index += 1
        return t
          

class GameParser(Parser):
    tokens = GameLexer.tokens

    def __init__(self):
        self.move = ""
        self.operation = ""
        self.grid = game()

    @_('operation move end')
    def input(self,p):
        self.grid.mov(p[0],p[1]) 
        print("2048> Thanks,"+p[1] +" move done,random tile added.")

    @_('ASSIGN VAL TO coordinates end')  
    def input(self,p):
        x = int(p.coordinates[0])
        y = int(p.coordinates[1])
        self.grid.assignment(int(p[1]),x,y)
        print('2048> Thanks, assignment done.')

    @_('VAR VARIABLE IS coordinates end')
    def input(self,p):
        x = int(p.coordinates[0])
        y = int(p.coordinates[1])
        self.grid.naming(p[1],x,y)
        print("2048> Thanks, naming done.")

    @_('VALUE IN coordinates end')
    def input(self,p):
        x = int(p.coordinates[0])
        y = int(p.coordinates[1])
        print(self.grid.get_val(x,y))

    @_('statement')
    def input(self,p):
        pass

    @_('FULLSTOP')
    def end(self,p):
        return p[0]

    @_('ADD','SUBTRACT','MULTIPLY','DIVIDE')
    def operation(self,p):
        return p[0]

    @_('LEFT','RIGHT','UP','DOWN')
    def move(self,p):
        return p[0]

    @_('VAL COMMA VAL')
    def coordinates(self,p):
        x = int(p.VAL0)
        y = int(p.VAL1)
        if x>0 and x<=4 and y>0 and y<=4:
            return (x-1,y-1)
        else:
            print("2048> There is no tile like that. The tile co-ordinates must be in range 1,2,3,4")
            sys.stderr.write(str(-1))
            sys.stderr.write("\n")

    @_('THE CURRENT STATE ARE')
    def statement(self,p):
        matrix = self.grid.matrix
        self.grid.print_matrix(matrix)
        for i in range(0,4):
            for j in range(0,4):
                sys.stderr.write(str(matrix[i][j])+" ")   
        dictionary = self.grid.tiles
        for pair in dictionary.keys():
            if(len(dictionary[pair])>0):
                sys.stderr.write(str(pair[0])+","+str(pair[1]))
                for i in dictionary[pair]:
                    sys.stderr.write(i+", ")
        sys.stderr.write("\n")

    @_('ERROR')
    def statement(self,p):
        sys.stderr.write(str(-1))
        sys.stderr.write("\n")


if __name__ == '__main__':
    parser = GameParser()
    lexer = GameLexer()

    n = 4
    parser.grid.generate_grid(n)
    parser.grid.print_matrix(parser.grid.getMatrix())

    while True:
        try:
            print('2048> Please enter a command')
            text = input('----> ')
        except EOFError:
            break    
        if text:
            try:
                parser.parse(lexer.tokenize(text))
            except EOFError:
                print("EOF Error")
#