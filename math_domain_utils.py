class infix_to_prefix:
    '''
    Converts ConPoLe Equations in infix notation to a prefix notation for parsing by DreamSolver's system.
    '''
    precedence={'^':5,'*':4,'/':4,'+':3,'-':3,'(':2,')':1, ' ^':5,' *':4, ' /':4,' +':3,' -':3,' (':2,' )':1}
    
    def __init__(self):
        self.items=[]
        self.size=-1
    
    def push(self,value):
        self.items.append(value)
        self.size+=1
    
    def pop(self):
        if self.isempty():
            return 0
        else:
            self.size-=1
            return self.items.pop()
    
    def isempty(self):
        if(self.size==-1):
            return True
        else:
            return False
    
    def seek(self):
        if self.isempty():
            return False
        else:
            return self.items[self.size]
    
    def is0perand(self,i):
        if i.isalpha() or i in '1234567890':
            return True
        else:
            return False
    
    def reverse(self,expr):
        rev=""
        for i in expr:
            if i == '(':
                i=')'
            elif i == ')':
                i='('
            rev=i+rev
        return rev
    
    def infixtoprefix (self,expr):
        prefix=""
        for ind in range(len(expr)):
            i = expr[ind]
            if self.is0perand(i):
                if ind<len(expr)-1 and expr[ind+1]=='-':
                    prefix += ' )'+i+'-('
                else:
                    prefix += ' )'+i+'('
            elif(i in '+*/^'):
                while(len(self.items)and self.precedence[i] < self.precedence[self.seek()]):
                    prefix+=self.pop()
                self.push(" "+i)
            elif(i == '-'):
                if ind>0 and expr[ind-1]==' ' and ind<len(expr)-1 and expr[ind+1]==' ':
                    while(len(self.items)and self.precedence[i] < self.precedence[self.seek()]):
                        prefix+=self.pop()
                    self.push(" "+i)
            elif i == ')':
                self.push(i)
            elif i == '(':
                o = self.pop()
                while o!=')' and o!=0:
                    prefix += o
                    o = self.pop()
            #end of for
        while len(self.items):
            if(self.seek()=='('):
                self.pop()
            else:
                prefix+=self.pop()
                #print(prefix)
        return prefix

def numberOfArgs(s):

    """
    Computes the number of times the brackets are perfectly matched (i.e. number of `(` = number of `)` ) to count the number of arguments in that string.

    Inputs: 
    - s is an equation string in prefix notation
    Returns:
    - an integer numMatched, which is equivalent to the number of arguments

    """
    numOpenBrPair = 0
    numMatched = 0
    for i in s:
        if i=="(":
            numOpenBrPair+=1
        elif i==")":
            numOpenBrPair-=1
            if numOpenBrPair==0:
                numMatched+=1
    return numMatched

def bracketize(s):
    
    '''
    Ensure that the brackets of the generated prefix notation match the format expected by the treefy() function.
    
    Inputs:
    - s is a prefix string generated by the infix_to_prefix objects
    Returns:
    - a string whose brackets are matched in a format expected by mdp.treefy()

    '''
    if len(s) <= 0 or s[0] not in "+-*/^":
        return s
    elif s[0] == "-" and s[1] != " ":
        #print(s)
        return s
    else:
        nextOpInd = max(s.rfind("+ "), s.rfind("- "), s.rfind("* "), s.rfind("/ "), s.rfind("^ ")) 
        ind2 = None
        if nextOpInd==0:
            return "(" + s[0] + " " + s[2:] + ")"
        elif nextOpInd==2 or numberOfArgs(s[nextOpInd:])!=2:
            ind2 = s.rfind("(") 
        else:
            ind2 = nextOpInd
        ind1 = 2
        s1 = s[ind1:ind2]
        s2 = s[ind2:len(s)]
        #print("The split is: ")
        #print(s)
        #print(s1)
        #print(s2)
        return "(" + s[0] + " " + bracketize(s1) + " " + bracketize(s2) + ")"

def infix_to_prefix_conversion(equation):
    """
    Accepts infix equation string as input, generates a prefix string as output.

    Inputs:
    - equation, a string containing an equation in infix notation
    Returns:
    - a string containing an equation in prefix notation, or None if no equivalent string exists.
    """
    subtree = equation.split('=')
    subtree_rev = [sub[::-1] for sub in subtree]

    obj1 = infix_to_prefix()
    result1 = obj1.infixtoprefix(subtree_rev[0])
    obj2 = infix_to_prefix() 
    result2 = obj2.infixtoprefix(subtree_rev[1])

    if (result1!=False and result2!=False):
        result = '(= ' + bracketize(result1[::-1]) + ' ' + bracketize(result2[::-1]) + ')'  
        result = result.replace("( (", "((")
        result = result.replace(") )", "))") 
        result = result.replace("  ", " ")
        return result
    else:
        return None