import unittest
from TestUtils import TestAST
from AST import *


class ASTGenSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """func main() {
            var a int = 100
        };"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([VarDecl('a', IntType(), IntLiteral(100))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,300))


    def test_more_complex_program(self):
        """More complex program"""
        input = """var x int ;"""
        expect = str(Program([VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    

    def test_call_without_parameter(self):
        """More complex program"""
        input = """func main () {
        return
        }; 
        var x int ;"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([Return(expr=None)])),VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,302))


    def test_more_complex_expression_in_right_hand_side(self):
        """More complex expression"""
        input = """func main () {
        return
        }; 
        var x int = 100*200-500;"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([Return(expr=None)])),VarDecl("x",IntType(),BinaryOp('-', BinaryOp('*', IntLiteral(100), IntLiteral(200)), IntLiteral(500)))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,303))


    def test_variable_declaration_with_float(self):
        input = """
        var f float = 0.34
        var f1 float = 1.2e10
        var f2 float = 3.
        """
        expect = str(
            Program(
                [
                    VarDecl('f', FloatType(), FloatLiteral(0.34)),
                    VarDecl('f1', FloatType(), FloatLiteral(1.2e10)),
                    VarDecl('f2', FloatType(), FloatLiteral(3.))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,304))


    def test_variable_declaration_with_array_type_and_array_literal(self):
        input = """
            var arr [2]int = [2]int{1, 2}
            var arr1 [1][2][a]float
        """
        expect = str(
            Program(
                [
                    VarDecl(
                        'arr',
                        ArrayType(
                            [IntLiteral(2)],
                            IntType()
                        ),
                        ArrayLiteral(
                            [IntLiteral(2)],
                            IntType(),
                            [IntLiteral(1), IntLiteral(2)]
                        )
                    ),
                    VarDecl(
                        'arr1',
                        ArrayType(
                            [IntLiteral(1), IntLiteral(2), Id('a')],
                            FloatType()
                        ),
                        None
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,305))