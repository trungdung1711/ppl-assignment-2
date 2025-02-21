from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):


    def visitInteger_literal(self, ctx:MiniGoParser.Integer_literalContext):

        if ctx.DECIMAL_INTEGER():
            text = ctx.DECIMAL_INTEGER().getText()
            base = 10
        elif ctx.BINARY_INTEGER():
            text = ctx.BINARY_INTEGER().getText()
            base = 2
        elif ctx.OCTAL_INTEGER():
            text = ctx.OCTAL_INTEGER().getText()
            base = 8
        elif ctx.HEXA_INTEGER():
            text = ctx.HEXA_INTEGER().getText()
            base = 16
        
        return IntLiteral(value=int(x=text, base=base))
    

    def visitBoolean_literal(self, ctx:MiniGoParser.Boolean_literalContext):
        if ctx.TRUE():
            return BooleanLiteral(value=True)
        elif ctx.FALSE():
            return BooleanLiteral(value=False)
        

    def visitBreak_statement(self, ctx:MiniGoParser.Break_statementContext):
        pass