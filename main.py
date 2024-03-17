# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0

        

    # move the lexer position and identify next possible tokens.
    def get_token(self):

        while self.position<len(self.code):
        
            curt_char = self.code[self.position]

            if curt_char != None and curt_char.isspace():
                self.position+=1
                continue

            while  curt_char in ('=', '+', '-', '*', '/', '(', ')'):
                token=curt_char
                self.position += 1
                return token

            if curt_char.isdigit():
                num = ''
                if curt_char.isdigit():
                    num += self.code[self.position]
                    self.position += 1
                return int(num)

    
            if curt_char.isalpha():
            
                variable_name = ''
                while self.code[self.position].isalpha():
                    variable_name += self.code[self.position]
                    self.position += 1
                return variable_name
        
            if curt_char in ('>', '<', '=', '!'):
                opr = curt_char
                self.position+=1
                if curt_char == '=':
                    opr += '='
                    self.position+=1
                return opr
            
            self.position += 1
        return None 
          
   



# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    # function to parse the entire program
    def parse(self):
        return self.program()
    

    # move to the next token.
    def advance(self):
        self.current_token = self.lexer.get_token()
   

    # parse the one or multiple statements
    def program(self):
        stmt = []
        self.advance()
        while self.current_token is not None:
            stmt.append(self.statement())

        return stmt

    
    # parse if, while, assignment statement.
    def statement(self):
        if self.current_token == "if":
            return self.if_statement()
        elif self.current_token == "while":
            return self.while_loop()
        else:
            return self.assignment()
    
    
    # parse assignment statements
    def assignment(self):
        variable_name = self.current_token
        self.advance()
        if self.current_token=="=":
            self.advance()
            expr=self.arithmetic_expression()
            if expr!=None: 
                return ("=",variable_name, expr)
                
        else:
            return None
    
      
    
    # parse arithmetic experssions
    def arithmetic_expression(self):
        term = self.term()
        opr=''
        while self.current_token in ("+" , "-" ):
            opr=self.current_token
            self.advance()
            next_term=self.term()
            term=(opr, term, next_term)
        return term   

   
    def term(self):
        factor = self.factor()
        opr=' '
        if self.current_token in ("*", "/"):
            opr=self.current_token
            self.advance()
            next_term=self.term()
            factor =(opr, factor, next_term)
 
        return factor


    def factor(self):

        if type(self.current_token)== int:  # Check if token is integer
            num = self.current_token
            self.advance()
            return num     
    
        elif self.current_token == '(':
            self.advance()
            expr = self.arithmetic_expression()
            if self.current_token == ')':
                self.advance()  # Move past ')'
                return expr
        else: 
            variable_name = self.current_token
            self.advance()
            return variable_name
        
    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        if self.current_token=="if":
            self.advance()
            conditi_on_=self.condition()
            self.advance()
            stmt1=self.statement()
            if self.current_token=="else":
                self.advance()
                else_stmt=self.statement()
                return("if",conditi_on_, stmt1, else_stmt )
            else:
                return("if",conditi_on_,stmt1)
                        

    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        if self.current_token=="while":
            self.advance()
            conditi_on_=self.condition()
            self.advance()
            stmt = self.statement()
            return("while",conditi_on_, stmt)


    def condition(self):
        arithmatic_expr1=self.arithmetic_expression()
        if self.current_token in ('==' , '!=' , '<' , '>' , '<=' , '>='):
            opr =self.current_token
            self.advance()
            airthmatic_expr2=self.arithmetic_expression()
            if arithmatic_expr1 and airthmatic_expr2 !=None:
                return (opr, arithmatic_expr1, airthmatic_expr2)
        
    
    
