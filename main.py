# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0

    # move the lexer position and identify next possible tokens.
    def get_token(self):

        while self.position<len(self.code):

            curt_char = self.code[self.position]
            #If the current character is whitespace (spaces, tabs, newlines), skip it and continue
            if curt_char != None and curt_char.isspace():
                self.position+=1
                continue

            # If the current character is a digit, collect all consecutive digits to form a multi-digit number
            if curt_char.isdigit():
                num_ = ''#Initializing an empty string to collect digits
                while self.position < len(self.code) and self.code[self.position].isdigit():
                    num_ += self.code[self.position]
                    self.position += 1 # Move to the next character
                return int(num_)

            ## If the current character is alphanumeric (letter or digit), collect all consecutive alphanumeric characters
            if curt_char.isalnum(): 
                stri_ng=''# Initialize an empty string to collect alphanumeric characters
                while self.position < len(self.code)  and self.code[self.position]. isalnum():
                    stri_ng += self.code[self.position] #Appending the alphanumeric character to the string
                    self.position += 1
                return stri_ng # alphanum token
            
            # If the current character is a special character (operator or parenthesis),
            if curt_char in ["(", ")", "=", "+", "/", "*", "-", " ", "<", ">", "+", "/", "*", "-"]: 
                _stri_ = curt_char
                self.position += 1
                return _stri_ 
            
            # If the current character is one that can start a comparison operator ('>', '<', '=', '!'), to check the next character and determine if it's a multi-character operator
            if curt_char in ('>', '<', '=', '!'):
                opr = curt_char
                self.position+=1
                #If the current character is '=' and the next character is also '=', 
                # then it's a '==' operator, so add the next character to the operator token
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
        stmt = []#initializes an empty list that will hold the statements of the program.
        self.advance()
        while self.current_token is not None:
            stmt.append(self.statement())

        return stmt

    
    # parse if, while, assignment statement.
    def statement(self):
        if self.current_token == "if":
            return self.if_statement() #Call the method that handles the parsing of if statements specifically.
        elif self.current_token == "while":
            return self.while_loop() # Call the method that handles the parsing of while loops specifically.
        else:
            return self.assignment() 
    
    
    # parse assignment statements
    def assignment(self):
        variable_name = self.current_token
        self.advance()
        if self.current_token=="=":#If the next token is indeed an "=" (assignment operator), then proceed to parse the right-hand side of the assignment statement.
            self.advance()
            expr=self.arithmetic_expression()
            if expr!= None: 
                return ("=",variable_name, expr) #If the 'arithmetic_expression' method successfully returns an expression (not None), then return a tuple representing the assignment operation.
        return None 
 
    
    # parse arithmetic experssions
    def arithmetic_expression(self):
        term = self.term()
        while self.current_token in ("+" , "-" ):
            opr=self.current_token #Store the current operator ('+' or '-') in 'opr'
            self.advance()
            next_term=self.term()
            term=(opr, term, next_term)
        return term   

   
    def term(self):
        factor = self.factor()
        if self.current_token in ("*", "/"):
            opr=self.current_token
            self.advance()
            next_term=self.term()
            factor =(opr, factor, next_term)
 
        return factor


    def factor(self):
        #check if the current token is an integer and if it is store the number in a variable
        if type(self.current_token)== int: 
            num_ = self.current_token
            self.advance() #Move on to the next token in the input.
            return num_    
    
        elif self.current_token == '(':
            self.advance() #Parse the arithmetic expression inside the parentheses.
            expr = self.arithmetic_expression()
            if self.current_token == ')':
                self.advance()  # Moving past ')'
                return expr
        else: 
            variable_name = self.current_token
            self.advance()
            return variable_name
        
    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        if self.current_token=="if":# Check if the current token is 'if' to confirm we are parsing an if statement.
            self.advance()
            if self.current_token is not None: #Make sure that advancing the token did not reach the end of the file/input (None).
                condition_=self.condition()
                self.advance()
                stmt1=self.statement()
                if self.current_token=="else":#Check if there is an 'else' part following the 'then' part.
                    self.advance()
                    else_stmt=self.statement()
                    return("if",condition_, stmt1, else_stmt )
                else:
                    return("if",condition_,stmt1)
                        

    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        
        if self.current_token=="while":#Check if the current token is 'while' to confirm we are parsing an while statement.
            self.advance()
            conditi_on_=self.condition()
            statemnt_=[]
            self.advance()
            if self.current_token != 'do':# If the current token is not 'do', it means that there is no explicit start of a loop body.
                statemnt_.append(self.statement())
            self.advance()
            return("while",conditi_on_, statemnt_)



    def condition(self):
        arithmetic_expr1 = self.arithmetic_expression()
        if arithmetic_expr1 is None:
            return None  # Error handling needed
        opr = self.current_token
        if opr in ('==', '!=', '<', '>', '<=', '>='):#  # If it is a comparison operator, proceed to parse the right-hand side of the condition.
            self.advance()
            arithmetic_expr2 = self.arithmetic_expression()
            if arithmetic_expr2 is None:
                return None  
            return (opr, arithmetic_expr1, arithmetic_expr2)
        else:
        # If the condition is just a single expression
            return ('expr', arithmetic_expr1) 
    
    
