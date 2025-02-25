from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):


    '''
    #==============================
    AST: AST.IntegerLiteral
    - value : int
    #==============================
    '''
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
    

    '''
    #==============================
    AST: AST.BooleanLiteral
    - value : bool
    #==============================
    '''
    def visitBoolean_literal(self, ctx:MiniGoParser.Boolean_literalContext):
        return BooleanLiteral(value=True) if ctx.TRUE() else BooleanLiteral(value=False)
    

    '''
    #==============================
    AST: AST.Break
    #==============================
    '''
    def visitBreak_statement(self, ctx:MiniGoParser.Break_statementContext):
        return Break()
    

    '''
    #==============================
    AST: AST.Continue
    #==============================
    '''
    def visitContinue_statement(self, ctx:MiniGoParser.Continue_statementContext):
        return Continue()
    

    '''
    #==============================
    AST: AST.Return
    - expr : Expr
    #==============================
    '''
    def visitReturn_statement(self, ctx:MiniGoParser.Return_statementContext):
        return Return(expr=self.visit(ctx.expression())) if ctx.expression() else Return(expr=None)
    

    '''
    #==============================
    AST: AST.IntType
         AST.FloatType
         AST.BoolType
         AST.StringType
    #==============================
    '''
    def visitPrimitive_type(self, ctx:MiniGoParser.Primitive_typeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.STRING():
            return StringType()


    '''
    #==============================
    AST: AST.ArrayType
    - dimens : List[Expr]
    - eleType : Type
    #==============================
    '''
    def visitArray_type(self, ctx:MiniGoParser.Array_typeContext):
        return ArrayType(dimens=self.visit(ctx.dimension_list()), eleType=self.visit(ctx.primitive_type())) if ctx.primitive_type() else ArrayType(dimens=self.visit(ctx.dimension_list()), eleType=Id(name=ctx.ID().getText()))
    

    def visitDimension_list(self, ctx:MiniGoParser.Dimension_listContext):
        return [self.visit(ctx.dimension())] if ctx.getChildCount() == 1 else [self.visit(ctx.dimension)] + self.visit(ctx.dimension_list)
    

    def visitDimension(self, ctx:MiniGoParser.DimensionContext):
        return self.visit(ctx.integer_literal()) if ctx.integer_literal() else Id(name=ctx.ID().getText())
    

    '''
    #==============================
    AST: AST.ArrayLiteral
    - dimens : List[Expr]
    - eleType : Type
    - value : NestedList
        - NestedList : PrimLit | List[NestedList]
    #==============================
    '''
    def visitArray_literal(self, ctx:MiniGoParser.Array_literalContext):
        array_type = self.visit(ctx.array_type())
        return ArrayLiteral(dimens=array_type.dimens, eleType=array_type.eleType, value=self.visit(ctx.array_element_list()))
    

    def visitArray_element_list(self, ctx:MiniGoParser.Array_element_listContext):
        return [self.visit(ctx.array_element())] if ctx.getChildCount() == 1 else [self.visit(ctx.array_element())] + self.visit(ctx.array_element_list())
    

    def visitArray_element(self, ctx:MiniGoParser.Array_elementContext):
        return self.visit(ctx.array_element_literal()) if ctx.array_element_literal() else self.visit(ctx.array_element_list())
    

    def visitArray_element_literal(self, ctx:MiniGoParser.Array_element_literalContext):
        if ctx.integer_literal():
            return self.visit(ctx.integer_literal())
        elif ctx.FLOATING_POINT():
            return FloatLiteral(value=float(ctx.FLOATING_POINT().getText()))
        elif ctx.STRING_LITERAL():
            return StringLiteral(value=ctx.STRING_LITERAL().getText())
        elif ctx.NIL():
            return NilLiteral()
        elif ctx.struct_literal():
            return self.visit(ctx.struct_literal())


    '''
    #==============================
    AST: AST.StructLiteral
    - name str
    - elements : List[Tuple[str, Expr]]
    #==============================
    '''
    def visitStruct_literal(self, ctx:MiniGoParser.Struct_literalContext):
        return StructLiteral(name=ctx.ID().getText(), elements=self.visit(ctx.struct_element_list()))
    

    def visitStruct_element_list(self, ctx:MiniGoParser.Struct_element_listContext):
        return [] if ctx.getChildCount() == 0 else self.visit(ctx.struct_element_prime())
    

    def visitStruct_element_prime(self, ctx:MiniGoParser.Struct_element_primeContext):
        return [self.visit(ctx.struct_element())] if ctx.getChildCount() == 1 else [self.visit(ctx.struct_element())] + self.visit(ctx.struct_element_prime())
    

    def visitStruct_element(self, ctx:MiniGoParser.Struct_elementContext):
        return (ctx.ID().getText(), self.visit(ctx.expression()))


    '''
    #==============================
    AST: AST.ArrayCell
    - arr : Expr
    - idx : List[Expr]
    AST: AST.FieldAccess
    - receiver : Expr
    - field : str
    AST: AST.Id
    - name : str
    #==============================
    '''
    def visitLhs(self, ctx:MiniGoParser.LhsContext):
        if ctx.field_access():
            return self.visit(ctx.field_access())
        elif ctx.array_index():
            return self.visit(ctx.array_index())
        elif ctx.ID():
            return Id(name=ctx.ID().getText())
    

    def visitField_access(self, ctx:MiniGoParser.Field_accessContext):
        return FieldAccess(receiver=self.visit(ctx.expression()), field=ctx.ID().getText())
    

    def visitArray_index(self, ctx:MiniGoParser.Array_indexContext):
        return ArrayCell(arr=self.visit(ctx.expression()), idx=self.visit(ctx.index_list()))
    

    def visitIndex_list(self, ctx:MiniGoParser.Index_listContext):
        return [self.visit(ctx.index())] if ctx.getChildCount() == 1 else [self.visit(ctx.index())] + self.visit(ctx.index_list())
    

    def visitIndex(self, ctx:MiniGoParser.IndexContext):
        return self.visit(ctx.expression())