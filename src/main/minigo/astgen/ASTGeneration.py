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
    

    '''
    #==============================
    AST: AST.If
    - expr : Expr
    - thenStmt : Stmt
    - elseStmt : Stmt
    #==============================
    '''
    def visitIf_statement(self, ctx:MiniGoParser.If_statementContext):
        return self.visit(ctx.if_part())


    def visitIf_part(self, ctx:MiniGoParser.If_partContext):
        return If(expr=self.visit(ctx.expression()), thenStmt=self.visit(ctx.block()), elseStmt=self.visit(ctx.else_part())) if ctx.else_part() else If(expr=self.visit(ctx.expression()), thenStmt=self.visit(ctx.block()), elseStmt=None)


    def visitElse_part(self, ctx:MiniGoParser.Else_partContext):
        return self.visit(ctx.if_part()) if ctx.if_part() else self.visit(ctx.block())
    

    '''
    #==============================
    AST: AST.FuncCall
    - funName : str
    - args : List[Expr]
    #==============================
    '''
    def visitCall_statement(self, ctx:MiniGoParser.Call_statementContext):
        return self.visit(ctx.function_call_statement()) if ctx.function_call_statement() else self.visit(ctx.method_call_statement())
    

    def visitFunction_call_statement(self, ctx:MiniGoParser.Function_call_statementContext):
        return FuncCall(funName=ctx.ID().getText(), args=self.visit(ctx.argument_list()))
    

    def visitArgument_list(self, ctx:MiniGoParser.Argument_listContext):
        return self.visit(ctx.argument_prime()) if ctx.argument_prime() else []
    

    def visitArgument_prime(self, ctx:MiniGoParser.Argument_primeContext):
        return [self.visit(ctx.argument())] if ctx.getChildCount() == 1 else [self.visit(ctx.argument())] + self.visit(ctx.argument_prime())
    

    def visitArgument(self, ctx:MiniGoParser.ArgumentContext):
        return self.visit(ctx.expression())


    '''
    #==============================
    AST: AST.MethCall
    - receiver : Expr
    - metName : str
    - args : List[Expr]
    #==============================
    '''
    def visitMethod_call_statement(self, ctx:MiniGoParser.Method_call_statementContext):
        return MethCall(receiver=self.visit(ctx.expression()), metName=ctx.ID().getText(), args=self.visit(ctx.argument_list()))


    '''
    #==============================
    AST: AST.StructType
    - name : str
    - elements : List[Tuple[str, Type]]
    - methods : List[MethodDecl]
    #==============================
    '''
    def visitType_declaration(self, ctx:MiniGoParser.Type_declarationContext):
        return self.visit(ctx.struct_declaration()) if ctx.struct_declaration() else self.visit(ctx.interface_declaration())


    def visitStruct_declaration(self, ctx:MiniGoParser.Struct_declarationContext):
        return StructType(name=ctx.ID().getText(), elements=self.visit(ctx.property_declaration_list()), methods=None)


    def visitProperty_declaration_list(self, ctx:MiniGoParser.Property_declaration_listContext):
        return [self.visit(ctx.property_declaration())] if ctx.getChildCount() == 1 else [self.visit(ctx.property_declaration())] + self.visit(ctx.property_declaration_list())


    def visitProperty_declaration(self, ctx:MiniGoParser.Property_declarationContext):
        return (ctx.ID().getText(), self.visit(ctx.type_part()))


    def visitType_part(self, ctx:MiniGoParser.Type_partContext):
        if ctx.primitive_type():
            return self.visit(ctx.primitive_type())
        elif ctx.ID():
            return Id(name=ctx.ID().getText())
        elif ctx.array_type():
            return self.visit(ctx.array_type())


    '''
    #==============================
    AST: AST.InterfaceType
    - name : str
    - methods : List[Prototype]
    #==============================
    '''
    def visitInterface_declaration(self, ctx:MiniGoParser.Interface_declarationContext):
        return InterfaceType(name=ctx.ID().getText(), methods=self.visit(ctx.prototype_list()))


    def visitPrototype_list(self, ctx:MiniGoParser.Prototype_listContext):
        return [self.visit(ctx.prototype())] if ctx.getChildCount() == 1 else [self.visit(ctx.prototype())] + self.visit(ctx.prototype_list())


    '''
    #==============================
    AST: AST.Prototype
    - name : str
    - params : List[Type]
    - retType : Type
    #==============================
    '''
    def visitPrototype(self, ctx:MiniGoParser.PrototypeContext):
        return Prototype(name=ctx.ID().getText(), params=[param_decl.parType for param_decl in self.visit(ctx.field_list())], retType=self.visit(ctx.type_part())) if ctx.type_part() else Prototype(name=ctx.ID().getText(), params=[param_decl.parType for param_decl in self.visit(ctx.field_list())], retType=VoidType())


    def visitFunction_declaration(self, ctx:MiniGoParser.Function_declarationContext):
        return self.visit(ctx.func_declaration()) if ctx.func_declaration() else self.visit(ctx.method_declaration())


    '''
    #==============================
    AST: AST.FuncDecl
    - name : str
    - params : List[ParamDecl]
    - retType : Type
    - block : Block
    #==============================
    '''
    def visitFunc_declaration(self, ctx:MiniGoParser.Func_declarationContext):
        return FuncDecl(name=ctx.ID().getText(), params=self.visit(ctx.field_list()), retType=self.visit(ctx.type_part()), body=self.visit(ctx.block())) if ctx.type_part() else FuncDecl(name=ctx.ID().getText(), params=self.visit(ctx.field_list()), retType=VoidType(), body=self.visit(ctx.block()))


    '''
    #==============================
    AST: AST.ParamDecl
    - parName : str
    - parType : Type
    #==============================
    '''
    def visitField_list(self, ctx:MiniGoParser.Field_listContext):
        return self.visit(ctx.field_prime()) if ctx.field_prime() else []


    def visitField_prime(self, ctx:MiniGoParser.Field_primeContext):
        return self.visit(ctx.field()) if ctx.getChildCount() == 1 else self.visit(ctx.field()) + self.visit(ctx.field_prime())


    def visitField(self, ctx:MiniGoParser.FieldContext):
        return [ParamDecl(parName=parName, parType=self.visit(ctx.type_part())) for parName in self.visit(ctx.name_list())]


    def visitName_list(self, ctx:MiniGoParser.Name_listContext):
        return [ctx.ID().getText()] if ctx.getChildCount() == 1 else [ctx.ID().getText()] + self.visit(ctx.name_list())


    '''
    #==============================
    AST: AST.MethodDecl
    - receiver : str
    - recType : Type
    - fun : FuncDecl
    #==============================
    '''
    def visitMethod_declaration(self, ctx:MiniGoParser.Method_declarationContext):
        return MethodDecl(receiver=ctx.ID(0).getText(), recType=self.visit(ctx.type_part(0)), fun=FuncDecl(name=ctx.ID(1).getText(), params=self.visit(ctx.field_list()), retType=self.visit(ctx.type_part(1)), body=self.visit(ctx.block()))) if ctx.type_part(1) else MethodDecl(receiver=ctx.ID(0).getText(), recType=self.visit(ctx.type_part(0)), fun=FuncDecl(name=ctx.ID(1).getText(), params=self.visit(ctx.field_list()), retType=VoidType(), body=self.visit(ctx.block())))
    

    '''
    #==============================
    AST: AST.Assign
    - lhs : LHS
    - rhs : Expr
    #==============================
    '''
    def visitAssignment_statement(self, ctx:MiniGoParser.Assignment_statementContext):
        binary_operator = self.visit(ctx.assignment_operator())
        if binary_operator is None:
            # Case ASS
            return Assign(lhs=self.visit(ctx.lhs()), rhs=self.visit(ctx.expression()))
        binary_operator.left = self.visit(ctx.lhs())
        binary_operator.right = self.visit(ctx.expression())
        return Assign(lhs=self.visit(ctx.lhs()), rhs=binary_operator)

    '''
    #==============================
    AST: AST.BinaryOp
    - op : str
    - left : Expr
    - right : Expr
    #==============================
    '''
    def visitAssignment_operator(self, ctx:MiniGoParser.Assignment_operatorContext):
        if ctx.ASS():
            return None
        elif ctx.ADD_ASS():
            return BinaryOp(op=str('+'), left=None, right=None)
        elif ctx.SUB_ASS():
            return BinaryOp(op=str('-'), left=None, right=None)
        elif ctx.MUL_ASS():
            return BinaryOp(op=str('*'), left=None, right=None)
        elif ctx.DIV_ASS():
            return BinaryOp(op=str('/'), left=None, right=None)
        elif ctx.MOD_ASS():
            return BinaryOp(op=str('%'), left=None, right=None)


    '''
    #==============================
    AST: AST.ForBasic
    - cond : Expr
    - loop : Block
    #==============================
    '''