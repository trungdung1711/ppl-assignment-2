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
        return BooleanLiteral(value=True) if ctx.TRUE() else BooleanLiteral(value=False)
    

    def visitBreak_statement(self, ctx:MiniGoParser.Break_statementContext):
        return Break()
    

    def visitContinue_statement(self, ctx:MiniGoParser.Continue_statementContext):
        return Continue()
    

    def visitReturn_statement(self, ctx:MiniGoParser.Return_statementContext):
        return Return(expr=self.visit(ctx.expression())) if ctx.expression() else Return(expr=None)
    

    def visitPrimitive_type(self, ctx:MiniGoParser.Primitive_typeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.STRING():
            return StringType()
        

    def visitArray_type(self, ctx:MiniGoParser.Array_typeContext):
        return ArrayType(dimens=self.visit(ctx.dimension_list()), eleType=self.visit(ctx.primitive_type())) if ctx.primitive_type() else ArrayType(dimens=self.visit(ctx.dimension_list()), eleType=Id(name=ctx.ID().getText()))
    

    def visitDimension_list(self, ctx:MiniGoParser.Dimension_listContext):
        return [self.visit(ctx.dimension())] if ctx.getChildCount() == 1 else [self.visit(ctx.dimension)] + self.visit(ctx.dimension_list)
    

    def visitDimension(self, ctx:MiniGoParser.DimensionContext):
        return self.visit(ctx.integer_literal()) if ctx.integer_literal() else Id(name=ctx.ID().getText())