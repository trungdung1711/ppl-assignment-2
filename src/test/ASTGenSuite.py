import unittest
from TestUtils import TestAST
from AST import *

'''
#==============================
Note that: at this stage, we know
that there would be no lexer errors, or 
parser errors to this phase as all the lexer (token)
errors and the grammar errors are already caught by the 
lexer and parser 
==> Thus at this stage, the token rule and grammar are 
all CORRECT => Using SIMPLE TOKEN is Ok
#==============================
'''
class ASTGenSuite(unittest.TestCase):


    '''
    #==============================
    AST: AST.Program
    - decl : List[Decl]
    #==============================
    '''
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
        var f3 float = 0.
        var f4 float = 1.E-5
        var f5 = 1.e10
        var f6 = 000.100e+3
        """
        expect = str(
            Program(
                [
                    VarDecl('f', FloatType(), FloatLiteral(0.34)),
                    VarDecl('f1', FloatType(), FloatLiteral(1.2e10)),
                    VarDecl('f2', FloatType(), FloatLiteral(3.)),
                    VarDecl('f3', FloatType(), FloatLiteral(0.)),
                    VarDecl('f4', FloatType(), FloatLiteral(1.E-5)),
                    VarDecl('f5', None, FloatLiteral(1.e10)),
                    VarDecl('f6', None, FloatLiteral(000.100e+3))
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


    def test_simple_struct_declaration_just_return_struct_type_not_GenDecl_node_like_real_Go(self):
        input = """
            type Human struct {
                name string
                age int
                money float
                son Human
            }
        """
        expect = str(
            Program(
                [
                    StructType(
                        'Human',
                        [
                            ('name', StringType()),
                            ('age', IntType()),
                            ('money', FloatType()),
                            ('son', Id('Human'))
                        ],
                        []
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,306))


    '''
    #==============================
    AST: AST.IntLiteral
    - value : int
    #==============================
    '''
    def test_integer_literal_AST_node_creation(self):
        input = \
        """
        var a int = 32;
        var b int = 0
        var c int = 0b100000
        var d int = 0B100000;
        var e int = 0o40
        var f int = 0O40
        var g int = 0x20
        var h int = 0X20;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(32)),
                    VarDecl('b', IntType(), IntLiteral(0)),
                    VarDecl('c', IntType(), IntLiteral(32)),
                    VarDecl('d', IntType(), IntLiteral(32)),
                    VarDecl('e', IntType(), IntLiteral(32)),
                    VarDecl('f', IntType(), IntLiteral(32)),
                    VarDecl('g', IntType(), IntLiteral(32)),
                    VarDecl('h', IntType(), IntLiteral(32)),
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,307))


    '''
    #==============================
    AST: AST.BooleanLiteral
    - value : bool
    #==============================
    '''
    def test_bool_literal_creation(self):
        input = \
        """
        const a = true;
        const b = false;
        var c = true;
        var d boolean = false;
        var e boolean = ((true || false) && true);
        func main() {
            return a && b && c && d && e;
        };
        """
        expect = str(
            Program(
                [
                    ConstDecl('a', None, BooleanLiteral(True)),
                    ConstDecl('b', None, BooleanLiteral(False)),
                    VarDecl('c', None, BooleanLiteral(True)),
                    VarDecl('d', BoolType(), BooleanLiteral(False)),
                    VarDecl(
                        'e', 
                        BoolType(),
                        BinaryOp(
                            '&&',
                            BinaryOp
                            (
                                '||',
                                BooleanLiteral(True),
                                BooleanLiteral(False)
                            ),
                            BooleanLiteral(True)
                        )),
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                Return(
                                    BinaryOp(
                                        '&&',
                                        BinaryOp(
                                            '&&',
                                            BinaryOp(
                                                '&&',
                                                BinaryOp(
                                                    '&&',
                                                    Id('a'),
                                                    Id('b')
                                                ),
                                                Id('c')
                                            ),
                                            Id('d')
                                        ),
                                        Id('e')
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,308))


    '''
    #==============================
    AST: AST.Break
    AST: AST.Continue
    AST: AST.Return
    - expr : Expr
    #==============================
    '''
    def test_complex_if_node_in_ast_with_the_use_of_break_continue_return_statement(self):
        input = \
        """
        func something() int {
            for index := 0; index < 100; index := index + 3 {
                if (index == 1) {
                    break;
                } else if (index == 2) {
                    return (index * 100) - index;
                } else if (index % 3 == 0) {
                    continue;
                } else {
                    return -1
                }
            }
            return index;
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'something',
                        [],
                        IntType(),
                        Block(
                            [
                                ForStep(
                                    Assign(
                                        Id('index'),
                                        IntLiteral(0)
                                    ),
                                    BinaryOp(
                                        '<',
                                        Id('index'),
                                        IntLiteral(100)
                                    ),
                                    Assign(
                                        Id('index'),
                                        BinaryOp(
                                            '+',
                                            Id('index'),
                                            IntLiteral(3)
                                        )
                                    ),
                                    Block(
                                        [
                                            If(
                                                BinaryOp('==', Id('index'), IntLiteral(1)),
                                                Block(
                                                    [Break()]
                                                ),
                                                If(
                                                    BinaryOp('==', Id('index'), IntLiteral(2)),
                                                    Block(
                                                        [
                                                            Return(
                                                                BinaryOp('-', BinaryOp('*', Id('index'), IntLiteral(100)), Id('index'))
                                                            )
                                                        ]
                                                    ),
                                                    If(
                                                        BinaryOp('==', BinaryOp('%', Id('index'), IntLiteral(3)), IntLiteral(0)),
                                                        Block(
                                                            [
                                                                Continue()
                                                            ]
                                                        ),
                                                        Block(
                                                            [
                                                                Return(
                                                                    UnaryOp(
                                                                        '-',
                                                                        IntLiteral(1)
                                                                    )
                                                                )
                                                            ]
                                                        )
                                                    )
                                                )
                                            )
                                        ]
                                    )
                                ),
                                Return(
                                    Id('index')
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 309))


    '''
    #==============================
    AST: AST.IntType
         AST.FloatType
         AST.BoolType
         AST.StringType
    #==============================
    '''
    def test_use_of_primitive_type(self):
        input = \
        """
        var a int = 100;
        var b float = 0.125;
        var c boolean = false;
        var d string = "Hello World"
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(100)),
                    VarDecl('b', FloatType(), FloatLiteral(0.125)),
                    VarDecl('c', BoolType(), BooleanLiteral(False)),
                    VarDecl('d', StringType(), StringLiteral('"Hello World"'))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 310))


    '''
    #==============================
    AST: AST.ArrayType
    - dimens : List[Expr]
    - eleType : Type
    #==============================
    '''
    def test_array_type_along_with_array_literal(self):
        input = \
        """
        var a [3]int = [3]int{1, 2, 3};
        """
        expect = str(
            Program(
                [
                    VarDecl(
                        'a',
                        ArrayType(
                            [
                                IntLiteral(3)
                            ],
                            IntType()
                        ),
                        ArrayLiteral(
                            [
                                IntLiteral(3)
                            ],
                            IntType(),
                            [
                                IntLiteral(1),
                                IntLiteral(2),
                                IntLiteral(3)
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 311))


    def test_array_type_and_complex_array_literal(self):
        input = \
        """
        var arr [3][4][5][CONST]float = [2][3]float{ {1.2, 2.2, 3.3} , {4.5, 5.6, 7.8} , 1.125 }
        """
        expect = str(
            Program(
                [
                    VarDecl(
                        'arr',
                        ArrayType(
                            [
                                IntLiteral(3),
                                IntLiteral(4),
                                IntLiteral(5),
                                Id('CONST')
                            ],
                            FloatType()
                        ),
                        ArrayLiteral(
                            [
                                IntLiteral(2),
                                IntLiteral(3)
                            ],
                            FloatType(),
                            [
                                [
                                    FloatLiteral(1.2),
                                    FloatLiteral(2.2),
                                    FloatLiteral(3.3)
                                ],
                                [
                                    FloatLiteral(4.5),
                                    FloatLiteral(5.6),
                                    FloatLiteral(7.8)
                                ],
                                FloatLiteral(1.125)
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 312))


    '''
    #==============================
    AST: AST.ArrayLiteral
    - dimens : List[Expr]
    - eleType : Type
    - value : NestedList
        - NestedList : PrimLit | List[NestedList]
    #==============================
    '''
    def test_array_type_and_array_literal_with_a_more_complex_declaration(self):
        input = \
        """
        var arr [0b01][0b10][0b11][0b100][0b101][ID]string = [2][2][2]int{ {{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}, nil }
        """
        expect = str(
            Program(
                [
                    VarDecl(
                        'arr',
                        ArrayType(
                            [
                                IntLiteral(1),
                                IntLiteral(2),
                                IntLiteral(3),
                                IntLiteral(4),
                                IntLiteral(5),
                                Id('ID')
                            ],
                            StringType()
                        ),
                        ArrayLiteral(
                            [
                                IntLiteral(2),
                                IntLiteral(2),
                                IntLiteral(2)
                            ],
                            IntType(),
                            [
                                [
                                    [
                                        IntLiteral(1),
                                        IntLiteral(2)
                                    ],
                                    [
                                        IntLiteral(3),
                                        IntLiteral(4)
                                    ]
                                ],
                                [
                                    [
                                        IntLiteral(5),
                                        IntLiteral(6)
                                    ],
                                    [
                                        IntLiteral(7),
                                        IntLiteral(8)
                                    ]
                                ],
                                NilLiteral()
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 313))


    def test_more_and_more_complex_array_type_and_array_literal(self):
        input = \
        """
        func main() [3]string {
            var arr [3]string = [3]string { "Hello", "World", "MiniGo", Human{name : "Dung", age : 18} } ;
            return arr;
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        ArrayType(
                            [
                                IntLiteral(3)
                            ],
                            StringType()
                        ),
                        Block(
                            [
                                VarDecl(
                                    'arr',
                                    ArrayType(
                                        [
                                            IntLiteral(3)
                                        ],
                                        StringType()
                                    ),
                                    ArrayLiteral(
                                        [
                                            IntLiteral(3)
                                        ],
                                        StringType(),
                                        [
                                            StringLiteral('"Hello"'),
                                            StringLiteral('"World"'),
                                            StringLiteral('"MiniGo"'),
                                            StructLiteral(
                                                'Human',
                                                [
                                                    ('name', StringLiteral('"Dung"')),
                                                    ('age', IntLiteral(18))
                                                ]
                                            )
                                        ]
                                    )
                                ),
                                Return(
                                    Id('arr')
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 314))


    def test_array_type_and_array_literal_all_literals_in_array_literal(self):
        input = \
        """
        var a [10]Human = [10]int{ 0XFF, 1.125, "Hello World\\n", true, false, nil, Human{name : "Dung", ID : "2210573"}, {1,2,3} }
        const a = [3]Human{ Human{name : "Le", ID : "2210572"}, Human{name : "Dung", ID : "2210573"}, Human{name : "Trung", ID : "2210574"} }
        var arr [3][2][1 ]int = [3][2][1]int {{{1}, {2}}, {{3},{4}}, {{5},{6}}}
        """
        expect = str(
            Program(
                [
                    VarDecl(
                        'a',
                        ArrayType(
                            [
                                IntLiteral(10)
                            ],
                            Id('Human')
                        ),
                        ArrayLiteral(
                            [
                                IntLiteral(10)
                            ],
                            IntType(),
                            [
                                IntLiteral(255),
                                FloatLiteral(1.125),
                                StringLiteral('"Hello World\\n"'),
                                BooleanLiteral(True),
                                BooleanLiteral(False),
                                NilLiteral(),
                                StructLiteral(
                                    'Human',
                                    [
                                        ('name', StringLiteral('"Dung"')),
                                        ('ID', StringLiteral('"2210573"'))
                                    ]
                                ),
                                [
                                    IntLiteral(1),
                                    IntLiteral(2),
                                    IntLiteral(3)
                                ]
                            ]
                        )
                    ),
                    ConstDecl(
                        'a',
                        None,
                        ArrayLiteral(
                            [
                                IntLiteral(3)
                            ],
                            Id('Human'),
                            [
                                StructLiteral(
                                    'Human',
                                    [
                                        ('name', StringLiteral('"Le"')),
                                        ('ID', StringLiteral('"2210572"'))
                                    ]
                                ),
                                StructLiteral(
                                    'Human',
                                    [
                                        ('name', StringLiteral('"Dung"')),
                                        ('ID', StringLiteral('"2210573"'))
                                    ]
                                ),
                                StructLiteral(
                                    'Human',
                                    [
                                        ('name', StringLiteral('"Trung"')),
                                        ('ID', StringLiteral('"2210574"'))
                                    ]
                                )
                            ]
                        )
                    ),
                    VarDecl(
                        'arr',
                        ArrayType(
                            [
                                IntLiteral(3),
                                IntLiteral(2),
                                IntLiteral(1)
                            ],
                            IntType()
                        ),
                        ArrayLiteral(
                            [
                                IntLiteral(3),
                                IntLiteral(2),
                                IntLiteral(1)
                            ],
                            IntType(),
                            [
                                [
                                    [
                                        IntLiteral(1)
                                    ],
                                    [
                                        IntLiteral(2)
                                    ]
                                ],
                                [
                                    [
                                        IntLiteral(3)
                                    ],
                                    [
                                        IntLiteral(4)
                                    ]
                                ],
                                [
                                    [
                                        IntLiteral(5)
                                    ],
                                    [
                                        IntLiteral(6)
                                    ]
                                ]
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 315))


    '''
    #==============================
    AST: AST.ConstDecl
    - conName : str
    - conType : Type
    - iniExpr : Expr
    #==============================
    '''
    def test_const_declaration(self):
        input = \
        """
        const a = 100;
        const a1 = 0o1234
        const b = 0.125;
        const c = "Hello World\\n"
        const d = true;
        const e = false;
        const f = nil;
        const g = Human{name : "Dung", ID : "2210573"};
        const h = [3]int{1,2,3};
        const i = [3][2][1]int{{{1},{2}},{{3},{4}},{{5},{6}}}
        const j = true && false;
        """
        expect = str(
            Program(
                [
                    ConstDecl('a', None, IntLiteral(100)),
                    ConstDecl('a1', None, IntLiteral(668)),
                    ConstDecl('b', None, FloatLiteral(0.125)),
                    ConstDecl('c', None, StringLiteral('"Hello World\\n"')),
                    ConstDecl('d', None, BooleanLiteral(True)),
                    ConstDecl('e', None, BooleanLiteral(False)),
                    ConstDecl('f', None, NilLiteral()),
                    ConstDecl(
                        'g',
                        None,
                        StructLiteral(
                            'Human',
                            [
                                ('name', StringLiteral('"Dung"')),
                                ('ID', StringLiteral('"2210573"'))
                            ]
                        )
                    ),
                    ConstDecl(
                        'h',
                        None,
                        ArrayLiteral(
                            [
                                IntLiteral(3)
                            ],
                            IntType(),
                            [
                                IntLiteral(1),
                                IntLiteral(2),
                                IntLiteral(3)
                            ]
                        )
                    ),
                    ConstDecl(
                        'i',
                        None,
                        ArrayLiteral(
                            [
                                IntLiteral(3),
                                IntLiteral(2),
                                IntLiteral(1)
                            ],
                            IntType(),
                            [
                                [
                                    [
                                        IntLiteral(1)
                                    ],
                                    [
                                        IntLiteral(2)
                                    ]
                                ],
                                [
                                    [
                                        IntLiteral(3)
                                    ],
                                    [
                                        IntLiteral(4)
                                    ]
                                ],
                                [
                                    [
                                        IntLiteral(5)
                                    ],
                                    [
                                        IntLiteral(6)
                                    ]
                                ]
                            ]
                        )
                    ),
                    ConstDecl(
                        'j',
                        None,
                        BinaryOp(
                            '&&',
                            BooleanLiteral(True),
                            BooleanLiteral(False)
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 316))


    '''
    #==============================
    AST: AST.StructLiteral
    - name str
    - elements : List[Tuple[str, Expr]]
    #==============================
    '''
    def test_struct_literal(self):
        input = \
        """
        type Human struct {
            money int
            is_dead boolean
        }

        func main() {
            var human Human = Human{money : 100, is_dead : false};
            return;
        }
        """
        expect = str(
            Program(
                [
                    StructType(
                        'Human',
                        [
                            ('money', IntType()),
                            ('is_dead', BoolType())
                        ],
                        []
                    ),
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                VarDecl(
                                    'human',
                                    Id('Human'),
                                    StructLiteral(
                                        'Human',
                                        [
                                            ('money', IntLiteral(100)),
                                            ('is_dead', BooleanLiteral(False))
                                        ]
                                    )
                                ),
                                Return(None)
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 317))


    def test_more_complex_struct_literal(self):
        input = \
        """
        var dad Human = Human { money : 150, is_dead : true };
        var mom Human = Human { money : 200, is_dead : true };
        var son Human = Human { money : 0, is_dead : true };
        """
        expect = str(
            Program(
                [
                    VarDecl(
                        'dad',
                        Id('Human'),
                        StructLiteral(
                            'Human',
                            [
                                ('money', IntLiteral(150)),
                                ('is_dead', BooleanLiteral(True))
                            ]
                        )
                    ),
                    VarDecl(
                        'mom',
                        Id('Human'),
                        StructLiteral(
                            'Human',
                            [
                                ('money', IntLiteral(200)),
                                ('is_dead', BooleanLiteral(True))
                            ]
                        )
                    ),
                    VarDecl(
                        'son',
                        Id('Human'),
                        StructLiteral(
                            'Human',
                            [
                                ('money', IntLiteral(0)),
                                ('is_dead', BooleanLiteral(True))
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 318))


    def test_more_more_more_complex_struct_literal(self):
        input = \
        """
        var dad Human = Human { money : 150, is_dead : true, son : Human { money : 0, is_dead : false }, wife : Human { money : 200, is_dead : true } };
        const president = Human { money : 1000000, is_dead : true };
        var baby Human = Human{};
        """
        expect = str(
            Program(
                [
                    VarDecl(
                        'dad',
                        Id('Human'),
                        StructLiteral(
                            'Human',
                            [
                                ('money', IntLiteral(150)),
                                ('is_dead', BooleanLiteral(True)),
                                ('son', StructLiteral(
                                    'Human',
                                    [
                                        ('money', IntLiteral(0)),
                                        ('is_dead', BooleanLiteral(False))
                                    ]
                                )),
                                ('wife', StructLiteral(
                                    'Human',
                                    [
                                        ('money', IntLiteral(200)),
                                        ('is_dead', BooleanLiteral(True))
                                    ]
                                ))
                            ]
                        )
                    ),
                    ConstDecl(
                        'president',
                        None,
                        StructLiteral(
                            'Human',
                            [
                                ('money', IntLiteral(1000000)),
                                ('is_dead', BooleanLiteral(True))
                            ]
                        )
                    ),
                    VarDecl(
                        'baby',
                        Id('Human'),
                        StructLiteral(
                            'Human',
                            []
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 319))


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
    def test_array_cell_in_left_hand_side(self):
        input = \
        """
        func main() {
            var arr [3]int = [3]int{1, 2, 3};
            arr[0] := arr[1] + arr[2];
            return arr[0]
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                VarDecl(
                                    'arr',
                                    ArrayType(
                                        [
                                            IntLiteral(3)
                                        ],
                                        IntType()
                                    ),
                                    ArrayLiteral(
                                        [
                                            IntLiteral(3)
                                        ],
                                        IntType(),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ]
                                    )
                                ),
                                Assign(
                                    ArrayCell(
                                        Id('arr'),
                                        [
                                            IntLiteral(0)
                                        ]
                                    ),
                                    BinaryOp(
                                        '+',
                                        ArrayCell(
                                            Id('arr'),
                                            [
                                                IntLiteral(1)
                                            ]
                                        ),
                                        ArrayCell(
                                            Id('arr'),
                                            [
                                                IntLiteral(2)
                                            ]
                                        )
                                    )
                                ),
                                Return(
                                    ArrayCell(
                                        Id('arr'),
                                        [
                                            IntLiteral(0)
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 320))


    def test_array_cell_in_complex_multiple_array(self):
        input = \
        """
        func main() {
        a.some_function()[1][2][3].eat()[1] := arr[1][2][3][4][5] + arr[5][4][3][2][1];
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                                [
                                    Assign(
                                        ArrayCell(
                                            MethCall(
                                                ArrayCell(
                                                    MethCall(
                                                        Id('a'),
                                                        'some_function',
                                                        []
                                                    ),
                                                    [
                                                        IntLiteral(1),
                                                        IntLiteral(2),
                                                        IntLiteral(3)
                                                    ]
                                                ),
                                                'eat',
                                                []
                                            ),
                                            [
                                                IntLiteral(1)
                                            ]
                                        ),
                                        BinaryOp(
                                            '+',
                                            ArrayCell(
                                                Id('arr'),
                                                [
                                                    IntLiteral(1),
                                                    IntLiteral(2),
                                                    IntLiteral(3),
                                                    IntLiteral(4),
                                                    IntLiteral(5)
                                                ]
                                            ),
                                            ArrayCell(
                                                Id('arr'),
                                                [
                                                    IntLiteral(5),
                                                    IntLiteral(4),
                                                    IntLiteral(3),
                                                    IntLiteral(2),
                                                    IntLiteral(1)
                                                ]
                                            )
                                        )
                                    )
                        ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 321))


    def test_more_complex_array_cell(self):
        input = \
        """
        func something() [2]int {
            var arr [2]int = [2]int{1, 2};
            arr[1+1] := arr[arr[0]] + arr[arr[1]];
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'something',
                        [],
                        ArrayType(
                            [
                                IntLiteral(2)
                            ],
                            IntType()
                        ),
                        Block(
                            [
                                VarDecl(
                                    'arr',
                                    ArrayType(
                                        [
                                            IntLiteral(2)
                                        ],
                                        IntType()
                                    ),
                                    ArrayLiteral(
                                        [
                                            IntLiteral(2)
                                        ],
                                        IntType(),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2)
                                        ]
                                    )
                                ),
                                Assign(
                                    ArrayCell(
                                        Id('arr'),
                                        [
                                            BinaryOp(
                                                '+',
                                                IntLiteral(1),
                                                IntLiteral(1)
                                            )
                                        ]
                                    ),
                                    BinaryOp(
                                        '+',
                                        ArrayCell(
                                            Id('arr'),
                                            [
                                                ArrayCell(
                                                    Id('arr'),
                                                    [
                                                        IntLiteral(0)
                                                    ]
                                                )
                                            ]
                                        ),
                                        ArrayCell(
                                            Id('arr'),
                                            [
                                                ArrayCell(
                                                    Id('arr'),
                                                    [
                                                        IntLiteral(1)
                                                    ]
                                                )
                                            ]
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 322))


    '''
        SOS: This test case is ambiguous
        There is an overlapping between expression and index_list
        in the parser rule array_index -> expression greedily
        eat the index of index_list
    '''
    def test_more_complex_array_cell_with_left_hand_side(self):
        input = \
        """
        func array_cell() string {
            a[1][2][3].e[1][2][3].c[1][2] := --1
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'array_cell',
                        [],
                        StringType(),
                        Block(
                            [
                                Assign(
                                    ArrayCell(
                                        FieldAccess(
                                            ArrayCell(
                                                FieldAccess(
                                                    ArrayCell(
                                                        Id('a'),
                                                        [
                                                            IntLiteral(1),
                                                            IntLiteral(2),
                                                            IntLiteral(3)
                                                        ]
                                                    ),
                                                    'e'
                                                ),
                                                [
                                                    IntLiteral(1),
                                                    IntLiteral(2),
                                                    IntLiteral(3)
                                                ]
                                            ),
                                            'c'
                                        ),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2)
                                        ]
                                    ),
                                    UnaryOp(
                                        '-',
                                        UnaryOp(
                                            '-',
                                            IntLiteral(1)
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 323))


    def test_array_cell_in_expression_only_without_left_hand_side(self):
        input = \
        """
        const arr = arr[1][2][3][4][5].a.b.c[1][2][3][4][5];
        """
        expect = str(
            Program(
                [
                    ConstDecl(
                        'arr',
                        None,
                        ArrayCell(
                            FieldAccess(
                                FieldAccess(
                                    FieldAccess(
                                        ArrayCell(
                                            Id('arr'),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2),
                                                IntLiteral(3),
                                                IntLiteral(4),
                                                IntLiteral(5)
                                            ]
                                        ),
                                        'a'
                                    ),
                                    'b'
                                ),
                                'c'
                            ),
                            [
                                IntLiteral(1),
                                IntLiteral(2),
                                IntLiteral(3),
                                IntLiteral(4),
                                IntLiteral(5)
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 324))


    def test_general_array_cell_in_both_left_and_right_hand_side(self):
        input = \
        """
        func main() int {
            a[1][2][3][4][5][6][7][8] := a[1][2][3][4][5][6][7][8] + 1;
            a[1][2] += 3
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        IntType(),
                        Block(
                            [
                                Assign(
                                    ArrayCell(
                                        Id('a'),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3),
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6),
                                            IntLiteral(7),
                                            IntLiteral(8)
                                        ]
                                    ),
                                    BinaryOp(
                                        '+',
                                        ArrayCell(
                                            Id('a'),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2),
                                                IntLiteral(3),
                                                IntLiteral(4),
                                                IntLiteral(5),
                                                IntLiteral(6),
                                                IntLiteral(7),
                                                IntLiteral(8)
                                            ]
                                        ),
                                        IntLiteral(1)
                                    )
                                ),
                                Assign(
                                    ArrayCell(
                                        Id('a'),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2)
                                        ]
                                    ),
                                    BinaryOp(
                                        '+',
                                        ArrayCell(
                                            Id('a'),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2)
                                            ]
                                        ),
                                        IntLiteral(3)
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 325))


    def test_all_cases_of_the_left_hand_side(self):
        input = \
        """
        func main() {
            dad.son[1].wife[2][2].baby.age := 1;
            arr[1][2][3].a.b.c[1][2][3] := 4
            a.b[1][2][3] += 100;
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                Assign(
                                    FieldAccess(
                                        FieldAccess(
                                            ArrayCell(
                                                FieldAccess(
                                                    ArrayCell(
                                                        FieldAccess(
                                                            Id('dad'),
                                                            'son'
                                                        ),
                                                        [
                                                            IntLiteral(1)
                                                        ]
                                                    ),
                                                    'wife'
                                                ),
                                                [
                                                    IntLiteral(2),
                                                    IntLiteral(2)
                                                ]
                                            ),
                                            'baby'
                                        ),
                                        'age'
                                    ),
                                    IntLiteral(1)
                                ),
                                Assign(
                                    ArrayCell(
                                        FieldAccess(
                                            FieldAccess(
                                                FieldAccess(
                                                    ArrayCell(
                                                        Id('arr'),
                                                        [
                                                            IntLiteral(1),
                                                            IntLiteral(2),
                                                            IntLiteral(3)
                                                        ]
                                                    ),
                                                    'a'
                                                ),
                                                'b'
                                            ),
                                            'c'
                                        ),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ]
                                    ),
                                    IntLiteral(4)
                                ),
                                Assign(
                                    ArrayCell(
                                        FieldAccess(
                                            Id('a'),
                                            'b'
                                        ),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ]
                                    ),
                                    BinaryOp(
                                        '+',
                                        ArrayCell(
                                            FieldAccess(
                                                Id('a'),
                                                'b'
                                            ),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2),
                                                IntLiteral(3)
                                            ]
                                        ),
                                        IntLiteral(100)
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 326))


    def test_complex_field_access_of_the_left_hand_side(self):
        input = \
        """
        func main() {
            (a[1][2][3].b.c.d.function(1)).f := 100 && true
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                Assign(
                                    FieldAccess(
                                        MethCall(
                                            FieldAccess(
                                                FieldAccess(
                                                    FieldAccess(
                                                        ArrayCell(
                                                            Id('a'),
                                                            [
                                                                IntLiteral(1),
                                                                IntLiteral(2),
                                                                IntLiteral(3)
                                                            ]
                                                        ),
                                                        'b'
                                                    ),
                                                    'c'
                                                ),
                                                'd'
                                            ),
                                            'function',
                                            [
                                                IntLiteral(1)
                                            ]
                                        ),
                                        'f'
                                    ),
                                    BinaryOp(
                                        '&&',
                                        IntLiteral(100),
                                        BooleanLiteral(True)
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 327))


    def test_field_access_with_all_components_of_left_hand_side(self):
        input = \
        """
        func assign_something() {
            var a int = 100;
            a := 200;
            arr[a][a+1] := 300;
            a.get_arr(1, 1+ 1, human)[1][1 + 1][3][true || false][0xFF + 0b01] := (a || b && true) > (-a + b) <= !true;
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'assign_something',
                        [],
                        VoidType(),
                        Block(
                            [
                                VarDecl(
                                    'a',
                                    IntType(),
                                    IntLiteral(100)
                                ),
                                Assign(
                                    Id('a'),
                                    IntLiteral(200)
                                ),
                                Assign(
                                    ArrayCell(
                                        Id('arr'),
                                        [
                                            Id('a'),
                                            BinaryOp(
                                                '+',
                                                Id('a'),
                                                IntLiteral(1)
                                            )
                                        ]
                                    ),
                                    IntLiteral(300)
                                ),
                                Assign(
                                    ArrayCell(
                                        MethCall(
                                            Id('a'),
                                            'get_arr',
                                            [
                                                IntLiteral(1),
                                                BinaryOp('+', IntLiteral(1), IntLiteral(1)),
                                                Id('human')
                                            ]
                                        ),
                                        [
                                            IntLiteral(1),
                                            BinaryOp('+', IntLiteral(1), IntLiteral(1)),
                                            IntLiteral(3),
                                            BinaryOp('||', BooleanLiteral(True), BooleanLiteral(False)),
                                            BinaryOp('+', IntLiteral(255), IntLiteral(1)
                                            )
                                        ]
                                    ),
                                    BinaryOp(
                                        '<=',
                                        BinaryOp(
                                            '>',
                                            BinaryOp(
                                                '||',
                                                Id('a'),
                                                BinaryOp(
                                                    '&&',
                                                    Id('b'),
                                                    BooleanLiteral(True)
                                                )
                                            ),
                                            BinaryOp(
                                                '+',
                                                UnaryOp(
                                                    '-',
                                                    Id('a')
                                                ),
                                                Id('b')
                                            )
                                        ),
                                        UnaryOp(
                                            '!',
                                            BooleanLiteral(True)
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 328))


    def test_more_lhs_with_different_simple_assignment_operator(self):
        input = \
        """
        func main() boolean {
            a.b += 1;
            a.arr[1][2] -= 1;
            a *= 1;
            b.func1().func2().a.c /= 1;
            return_array(1,2,1.2)[1][2] %= 1;
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        BoolType(),
                        Block(
                            [
                                Assign(
                                    FieldAccess(
                                        Id('a'),
                                        'b'
                                    ),
                                    BinaryOp(
                                        '+',
                                        FieldAccess(
                                            Id('a'),
                                            'b'
                                        ),
                                        IntLiteral(1)
                                    )
                                ),
                                Assign(
                                    ArrayCell(
                                        FieldAccess(
                                            Id('a'),
                                            'arr'
                                        ),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2)
                                        ]
                                    ),
                                    BinaryOp(
                                        '-',
                                        ArrayCell(
                                            FieldAccess(
                                                Id('a'),
                                                'arr'
                                            ),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2)
                                            ]
                                        ),
                                        IntLiteral(1)
                                    )
                                ),
                                Assign(
                                    Id('a'),
                                    BinaryOp(
                                        '*',
                                        Id('a'),
                                        IntLiteral(1)
                                    )
                                ),
                                Assign(
                                    FieldAccess(
                                        FieldAccess(
                                            MethCall(
                                                MethCall(
                                                    Id('b'),
                                                    'func1',
                                                    []
                                                ),
                                                'func2',
                                                []
                                            ),
                                            'a'
                                        ),
                                        'c'
                                    ),
                                    BinaryOp(
                                        '/',
                                        FieldAccess(
                                            FieldAccess(
                                                MethCall(
                                                    MethCall(
                                                        Id('b'),
                                                        'func1',
                                                        []
                                                    ),
                                                    'func2',
                                                    []
                                                ),
                                                'a'
                                            ),
                                            'c'
                                        ),
                                        IntLiteral(1)
                                    )
                                ),
                                Assign(
                                    ArrayCell(
                                        FuncCall(
                                            'return_array',
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2),
                                                FloatLiteral(1.2)
                                            ]
                                        ),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2)
                                        ]
                                    ),
                                    BinaryOp(
                                        '%',
                                        ArrayCell(
                                            FuncCall(
                                                'return_array',
                                                [
                                                    IntLiteral(1),
                                                    IntLiteral(2),
                                                    FloatLiteral(1.2)
                                                ]
                                            ),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2)
                                            ]
                                        ),
                                        IntLiteral(1)
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 329))


    def test_composite_left_hand_side(self):
        input = \
        """
        func lhs() int {
            ((a[1][2][3])[1][2][3])[1][2][3] := 100 && true
            a[1][2][3][4][5][6][7][8][9] :=nil
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'lhs',
                        [],
                        IntType(),
                        Block(
                            [
                                Assign(
                                    ArrayCell(
                                        ArrayCell(
                                            ArrayCell(
                                                Id('a'),
                                                [
                                                    IntLiteral(1),
                                                    IntLiteral(2),
                                                    IntLiteral(3)
                                                ]
                                            ),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2),
                                                IntLiteral(3)
                                            ]
                                        ),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ]
                                    ),
                                    BinaryOp(
                                        '&&',
                                        IntLiteral(100),
                                        BooleanLiteral(True)
                                    )
                                ),
                                Assign(
                                    ArrayCell(
                                        Id('a'),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3),
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6),
                                            IntLiteral(7),
                                            IntLiteral(8),
                                            IntLiteral(9)
                                        ]
                                    ),
                                    NilLiteral()
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 330))


    '''
    #==============================
    AST: AST.If
    - expr : Expr
    - thenStmt : Stmt
    - elseStmt : Stmt
    #==============================
    '''
    def test_simple_if_ast_node(self):
        input = \
        """
        func main() {
            if (a > b > c) {
                max := a;
            }
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                If(
                                    BinaryOp(
                                        '>',
                                        BinaryOp(
                                            '>',
                                            Id('a'),
                                            Id('b')
                                        ),
                                        Id('c')
                                    ),
                                    Block(
                                        [
                                            Assign(
                                                Id('max'),
                                                Id('a')
                                            )
                                        ]
                                    ),
                                    None
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 331))


    def test_simple_if_else_ast_node(self):
        input = \
        """
        func if_check() {
            if (a + 100 * 200 > 300) {
                return true;
            } else {
                return false;
            }
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'if_check',
                        [],
                        VoidType(),
                        Block(
                            [
                                If(
                                    BinaryOp(
                                        '>',
                                        BinaryOp(
                                            '+',
                                            Id('a'),
                                            BinaryOp(
                                                '*',
                                                IntLiteral(100),
                                                IntLiteral(200)
                                            )
                                        ),
                                        IntLiteral(300)
                                    ),
                                    Block(
                                        [
                                            Return(
                                                BooleanLiteral(True)
                                            )
                                        ]
                                    ),
                                    Block(
                                        [
                                            Return(
                                                BooleanLiteral(False)
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 332))


    def test_else_if_chain_ast_node(self):
        input = \
        """
        func main() {
            if (a > b) {
                return a;
                return c;
            } else if (a < b) {
                return b;
                return c;
            } else if (a == b) {
                return a + b;
                return a - b
            } else {
                return 0;
            }
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                If(
                                    BinaryOp(
                                        '>',
                                        Id('a'),
                                        Id('b')
                                    ),
                                    Block(
                                        [
                                            Return(
                                                Id('a')
                                            ),
                                            Return(
                                                Id('c')
                                            )
                                        ]
                                    ),
                                    If(
                                        BinaryOp(
                                            '<',
                                            Id('a'),
                                            Id('b')
                                        ),
                                        Block(
                                            [
                                                Return(
                                                    Id('b')
                                                ),
                                                Return(
                                                    Id('c')
                                                )
                                            ]
                                        ),
                                        If(
                                            BinaryOp(
                                                '==',
                                                Id('a'),
                                                Id('b')
                                            ),
                                            Block(
                                                [
                                                    Return(
                                                        BinaryOp(
                                                            '+',
                                                            Id('a'),
                                                            Id('b')
                                                        )
                                                    ),
                                                    Return(
                                                        BinaryOp(
                                                            '-',
                                                            Id('a'),
                                                            Id('b')
                                                        )
                                                    )
                                                ]
                                            ),
                                            Block(
                                                [
                                                    Return(
                                                        IntLiteral(0)
                                                    )
                                                ]
                                            )
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 333))


    def test_more_complex_else_if_chain_node(self):
        input = \
        """
        func if_check() {
            if (true) {
                continue;
            } else if (true) {
                continue
            } else if (true) {
                continue
            } else if (true) {
                continue
            } else if (true) {
                continue
            } else {
                return
            }
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'if_check',
                        [],
                        VoidType(),
                        Block(
                            [
                                If(
                                    BooleanLiteral(True),
                                    Block(
                                        [
                                            Continue()
                                        ]
                                    ),
                                    If(
                                        BooleanLiteral(True),
                                        Block(
                                            [
                                                Continue()
                                            ]
                                        ),
                                        If(
                                            BooleanLiteral(True),
                                            Block(
                                                [
                                                    Continue()
                                                ]
                                            ),
                                            If(
                                                BooleanLiteral(True),
                                                Block(
                                                    [
                                                        Continue()
                                                    ]
                                                ),
                                                If(
                                                    BooleanLiteral(True),
                                                    Block(
                                                        [
                                                            Continue()
                                                        ]
                                                    ),
                                                    Block(
                                                        [
                                                            Return(None)
                                                        ]
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 334))


    def test_complex_else_if_chain_with_no_else_but_else_if(self):
        input = \
        """
        func test() {
            if (a) {
                break;
            } else if (b) {
                break;
            } else if (c) {
                break;
            } else if (d) {
                break;
            } else if (e) {
                break;
            }
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'test',
                        [],
                        VoidType(),
                        Block(
                            [
                                If(
                                    Id('a'),
                                    Block(
                                        [
                                            Break()
                                        ]
                                    ),
                                    If(
                                        Id('b'),
                                        Block(
                                            [
                                                Break()
                                            ]
                                        ),
                                        If(
                                            Id('c'),
                                            Block(
                                                [
                                                    Break()
                                                ]
                                            ),
                                            If(
                                                Id('d'),
                                                Block(
                                                    [
                                                        Break()
                                                    ]
                                                ),
                                                If(
                                                    Id('e'),
                                                    Block(
                                                        [
                                                            Break()
                                                        ]
                                                    ),
                                                    None
                                                )
                                            )
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 335))


    def test_very_very_complex_if_else_chain(self):
        input = \
        """
        func test() {
            if(a) {
                if (a1) {
                    return ;
                } else if (a2) {
                    return ;
                } else {
                    return
                }

            } else if (b) {
                return
            } else if (c) {
                return
            } else {
                return
                if (d) {
                    return
                } else if (e) {
                    return
                }
            }
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'test',
                        [],
                        VoidType(),
                        Block(
                            [
                                If(
                                    Id('a'),
                                    Block(
                                        [
                                            If(
                                                Id('a1'),
                                                Block(
                                                    [
                                                        Return(None)
                                                    ]
                                                ),
                                                If(
                                                    Id('a2'),
                                                    Block(
                                                        [
                                                            Return(None)
                                                        ]
                                                    ),
                                                    Block(
                                                        [
                                                            Return(None)
                                                        ]
                                                    )
                                                )
                                            )
                                        ]
                                    ),
                                    If(
                                        Id('b'),
                                        Block(
                                            [
                                                Return(None)
                                            ]
                                        ),
                                        If(
                                            Id('c'),
                                            Block(
                                                [
                                                    Return(None)
                                                ]
                                            ),
                                            Block(
                                                [
                                                    Return(None),
                                                    If(
                                                        Id('d'),
                                                        Block(
                                                            [
                                                                Return(None)
                                                            ]
                                                        ),
                                                        If(
                                                            Id('e'),
                                                            Block(
                                                                [
                                                                    Return(None)
                                                                ]
                                                            ),
                                                            None
                                                        )
                                                    )
                                                ]
                                            )
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 336))


    '''
    #==============================
    AST: AST.FuncCall
    - funName : str
    - args : List[Expr]
    #==============================
    '''
    def test_simple_function_call_statement_no_argument(self):
        input = \
        """
        func main() {
            exit()
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                FuncCall(
                                    'exit',
                                    []
                                )
                            ]
                        )

                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 337))


    def test_simple_function_call_statement_one_argument(self):
        input = \
        """
        func main() {
            turn_on(true)
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                FuncCall(
                                    'turn_on',
                                    [
                                        BooleanLiteral(True)
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 338))


    def test_function_call_statement_with_multiple_arguments(self):
        input = \
        """
        func main() {
            matrix_multiplication([2][2]int{ {1,2}, {3,4} }, [2][1]int {{3}, {3}})
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                FuncCall(
                                    'matrix_multiplication',
                                    [
                                        ArrayLiteral(
                                            [
                                                IntLiteral(2),
                                                IntLiteral(2)
                                            ],
                                            IntType(),
                                            [
                                                [
                                                    IntLiteral(1),
                                                    IntLiteral(2)
                                                ],
                                                [
                                                    IntLiteral(3),
                                                    IntLiteral(4)
                                                ]
                                            ]
                                        ),
                                        ArrayLiteral(
                                            [
                                                IntLiteral(2),
                                                IntLiteral(1)
                                            ],
                                            IntType(),
                                            [
                                                [
                                                    IntLiteral(3)
                                                ],
                                                [
                                                    IntLiteral(3)
                                                ]
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 339))


    def test_function_call_statement_with_more_arguments_passed(self):
        input = \
        """
        func main() {
            weird_function(1, 0b10, 0o02, 0x03, 1.5, true, "hello\\n", nil, [2]int{1,2})
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                FuncCall(
                                    'weird_function',
                                    [
                                        IntLiteral(1),
                                        IntLiteral(2),
                                        IntLiteral(2),
                                        IntLiteral(3),
                                        FloatLiteral(1.5),
                                        BooleanLiteral(True),
                                        StringLiteral('"hello\\n"'),
                                        NilLiteral(),
                                        ArrayLiteral(
                                            [
                                                IntLiteral(2)
                                            ],
                                            IntType(),
                                            [
                                                IntLiteral(1),
                                                IntLiteral(2)
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 340))


    '''
    #==============================
    AST: AST.MethCall
    - receiver : Expr
    - metName : str
    - args : List[Expr]
    #==============================
    '''
    def test_method_call_statement_in_the_left_hand_side_only(self):
        input = \
        """
        func main() {
            var human Human ;
            human.walk();
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                VarDecl(
                                    'human',
                                    Id('Human'),
                                    None
                                ),
                                MethCall(
                                    Id('human'),
                                    'walk',
                                    []
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 341))


    def test_more_complex_method_call_statement(self):
        input = \
        """
        func main() {
            human.eat(Food{ calo : 100, energy : 100})
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                MethCall(
                                    Id('human'),
                                    'eat',
                                    [
                                        StructLiteral(
                                            'Food',
                                            [
                                                ('calo', IntLiteral(100)),
                                                ('energy', IntLiteral(100))
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 342))


    def test_expression_return_a_method_call(self):
        input = \
        """
        func main() {
            arr[1][2].field1.field2.function("a", "b", "c", "d")
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                MethCall(
                                    FieldAccess(
                                        FieldAccess(
                                            ArrayCell(
                                                Id('arr'),
                                                [
                                                    IntLiteral(1),
                                                    IntLiteral(2)
                                                ]
                                            ),
                                            'field1'
                                        ),
                                        'field2'
                                    ),
                                    'function',
                                    [
                                        StringLiteral('"a"'),
                                        StringLiteral('"b"'),
                                        StringLiteral('"c"'),
                                        StringLiteral('"d"')
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 343))


    def test_more_complex_method_call_statement_multiple_expression_and_multiple_arguments(self):
        input = \
        """
        func main() {
            a.b.c.d[1][2][3].e.f.g.h[1][2][3].function(false, true, 1, 2, "Hello")
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                MethCall(
                                    ArrayCell(
                                        FieldAccess(
                                            FieldAccess(
                                                FieldAccess(
                                                    FieldAccess(
                                                        ArrayCell(
                                                            FieldAccess(
                                                                FieldAccess(
                                                                    FieldAccess(
                                                                        Id('a'),
                                                                        'b'
                                                                    ),
                                                                    'c'
                                                                ),
                                                                'd'
                                                            ),
                                                            [
                                                                IntLiteral(1),
                                                                IntLiteral(2),
                                                                IntLiteral(3)
                                                            ]
                                                        ),
                                                        'e'
                                                    ),
                                                    'f'
                                                ),
                                                'g'
                                            ),
                                            'h'
                                        ),
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ]
                                    ),
                                    'function',
                                    [
                                        BooleanLiteral(False),
                                        BooleanLiteral(True),
                                        IntLiteral(1),
                                        IntLiteral(2),
                                        StringLiteral('"Hello"')
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 344))


    def test_function_call_and_method_call_together(self):
        input = \
        """
        func main() {
            function().give_birth().eat_and_drink(food, water)
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'main',
                        [],
                        VoidType(),
                        Block(
                            [
                                MethCall(
                                    MethCall(
                                        FuncCall(
                                            'function',
                                            []
                                        ),
                                        'give_birth',
                                        []
                                    ),
                                    'eat_and_drink',
                                    [
                                        Id('food'),
                                        Id('water')
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 345))


    '''
    #==============================
    AST: AST.StructType
    - name : str
    - elements : List[Tuple[str, Type]]
    - methods : List[MethodDecl]
    #==============================
    '''
    def test_simple_struct_declaration_but_just_return_StructType_which_is_different_from_real_go_when_it_actually_has_GenDecl(self):
        input = \
        """
        type House struct {
            l float;
            w float;
            m Material;
            n_f int;
        }


        func (h House) get_a() {
            return h.l * h.w
        }
        """
        expect = str(
            Program(
                [
                    StructType(
                        'House',
                        [
                            ('l', FloatType()),
                            ('w', FloatType()),
                            ('m', Id('Material')),
                            ('n_f', IntType())
                        ],
                        []
                    ),
                    MethodDecl(
                        'h',
                        Id('House'),
                        FuncDecl(
                            'get_a',
                            [],
                            VoidType(),
                            Block(
                                [
                                    Return(
                                        BinaryOp(
                                            '*',
                                            FieldAccess(
                                                Id('h'),
                                                'l'
                                            ),
                                            FieldAccess(
                                                Id('h'),
                                                'w'
                                            )
                                        )
                                    )
                                ]
                            )
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 346))


    def test_struct_declaration_with_composite_type_array_and_struct_type(self):
        input = \
        """
        type Laptop struct {
            price float;
            card Card;
            ram int;
            brand Brand;
            a [5]A
        };


        type Card struct {
            price int;
            dis int;
        }
        """
        expect = str(
            Program(
                [
                    StructType(
                        'Laptop',
                        [
                            ('price', FloatType()),
                            ('card', Id('Card')),
                            ('ram', IntType()),
                            ('brand', Id('Brand')),
                            ('a', ArrayType(
                                [
                                    IntLiteral(5)
                                ],
                                Id('A')
                            ))
                        ],
                        []
                    ),
                    StructType(
                        'Card',
                        [
                            ('price', IntType()),
                            ('dis', IntType())
                        ],
                        []
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 347))


    def test_struct_declaration_with_method_declaration(self):
        input = \
        """
        type Stack struct {
            length int;
            list [100]int
        }


        func (s Stack) pop() int {
            return list[length - 1]
        }


        func (s Stack) get(index int) int {
            return list[index]
        }
        """
        expect = str(
            Program(
                [
                    StructType(
                        'Stack',
                        [
                            ('length', IntType()),
                            ('list', ArrayType(
                                [
                                    IntLiteral(100)
                                ],
                                IntType()
                            ))
                        ],
                        []
                    ),
                    MethodDecl(
                        's',
                        Id('Stack'),
                        FuncDecl(
                            'pop',
                            [],
                            IntType(),
                            Block(
                                [
                                    Return(
                                        ArrayCell(
                                            Id('list'),
                                            [
                                                BinaryOp(
                                                    '-',
                                                    Id('length'),
                                                    IntLiteral(1)
                                                )
                                            ]
                                        )
                                    )
                                ]
                            )
                        )
                    ),
                    MethodDecl(
                        's',
                        Id('Stack'),
                        FuncDecl(
                            'get',
                            [
                                ParamDecl(
                                    'index',
                                    IntType()
                                )
                            ],
                            IntType(),
                            Block(
                                [
                                    Return(
                                        ArrayCell(
                                            Id('list'),
                                            [
                                                Id('index')
                                            ]
                                        )
                                    )
                                ]
                            )
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 348))


    def test_more_complex_struct_declaration_and_method_declaration(self):
        input = \
        """
        type Book struct{
            price float;
            n_page int;
            author [10]Author;
            year int;
            title string;
            genre Genre;
            sale int;
            point int;
        }

        func (b Book) set_book(p float, n int, a Author, y int, t string, g Genre, s,p int) {
            return;
        }

        """
        expect = str(
            Program(
                [
                    StructType(
                        'Book',
                        [
                            ('price', FloatType()),
                            ('n_page', IntType()),
                            ('author', ArrayType(
                                [
                                    IntLiteral(10)
                                ],
                                Id('Author')
                            )),
                            ('year', IntType()),
                            ('title', StringType()),
                            ('genre', Id('Genre')),
                            ('sale', IntType()),
                            ('point', IntType())
                        ],
                        []
                    ),
                    MethodDecl(
                        'b',
                        Id('Book'),
                        FuncDecl(
                            'set_book',
                            [
                                ParamDecl('p', FloatType()),
                                ParamDecl('n', IntType()),
                                ParamDecl('a', Id('Author')),
                                ParamDecl('y', IntType()),
                                ParamDecl('t', StringType()),
                                ParamDecl('g', Id('Genre')),
                                ParamDecl('s', IntType()),
                                ParamDecl('p', IntType()),
                            ],
                            VoidType(),
                            Block(
                                [
                                    Return(None)
                                ]
                            )
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 349))


    def test_complex_function_declaration_with_param_list(self):
        input = \
        """
        func stupid_func(a,b,c,d float, m,n,p Point, x, y,z string) [5]int {
            return 1;
        }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'stupid_func',
                        [
                            ParamDecl('a', FloatType()),
                            ParamDecl('b', FloatType()),
                            ParamDecl('c', FloatType()),
                            ParamDecl('d', FloatType()),
                            ParamDecl('m', Id('Point')),
                            ParamDecl('n', Id('Point')),
                            ParamDecl('p', Id('Point')),
                            ParamDecl('x', StringType()),
                            ParamDecl('y', StringType()),
                            ParamDecl('z', StringType()),
                        ],
                        ArrayType(
                            [
                                IntLiteral(5)
                            ],
                            IntType()
                        ),
                        Block(
                            [
                                Return(
                                    IntLiteral(1)
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 350))


    '''
    #==============================
    AST: AST.InterfaceType
    - name : str
    - methods : List[Prototype]
    #==============================
    '''
    '''
    #==============================
    AST: AST.Prototype
    - name : str
    - params : List[Type]
    - retType : Type
    #==============================
    '''
    def test_simple_interface_declaration_but_in_this_weird_ast_this_will_result_in_InterfaceType_not_GenDecl_in_real_go(self):
        input = \
        """
        type Animal interface {
            eat();
            walk();
            sleep();
            attack() int;
        }
        """
        expect = str(
            Program(
                [
                    InterfaceType(
                        'Animal',
                        [
                            Prototype(
                                'eat',
                                [],
                                VoidType()
                            ),
                            Prototype(
                                'walk',
                                [],
                                VoidType()
                            ),
                            Prototype(
                                'sleep',
                                [],
                                VoidType()
                            ),
                            Prototype(
                                'attack',
                                [],
                                IntType()
                            )
                        ]
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 351))


    def test_complex_prototype_in_interface_declaration(self):
        input = \
        """
        type Animal interface {
            eat(food [10]Food) float;
            attack(animal Animal) float;
            is_dead() boolean;
        }
        """
        expect = str(
            Program(
                [
                    InterfaceType(
                        'Animal',
                        [
                            Prototype(
                                'eat',
                                [
                                    ArrayType(
                                        [
                                            IntLiteral(10)
                                        ],
                                        Id('Food')
                                    )
                                ],
                                FloatType()
                            ),
                            Prototype(
                                'attack',
                                [
                                    Id('Animal')
                                ],
                                FloatType()
                            ),
                            Prototype(
                                'is_dead',
                                [

                                ],
                                BoolType()
                            )
                        ]
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 352))


    def test_more_complex_prototype_with_multiple_parameters(self):
        input = \
        """
        type Animal interface {
            do_math(a,b,c,d,e int, m,n,p,q float, u, t, v [5]boolean, a, b, c, d Animal)
        }
        """
        expect = str(
            Program(
                [
                    InterfaceType(
                        'Animal',
                        [
                            Prototype(
                                'do_math',
                                [
                                    IntType(),
                                    IntType(),
                                    IntType(),
                                    IntType(),
                                    IntType(),
                                    FloatType(),
                                    FloatType(),
                                    FloatType(),
                                    FloatType(),
                                    ArrayType(
                                        [IntLiteral(5)],
                                        BoolType()
                                    ),
                                    ArrayType(
                                        [IntLiteral(5)],
                                        BoolType()
                                    ),
                                    ArrayType(
                                        [IntLiteral(5)],
                                        BoolType()
                                    ),
                                    Id('Animal'),
                                    Id('Animal'),
                                    Id('Animal'),
                                    Id('Animal'),
                                ],
                                VoidType()
                            )
                        ]
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 353))


    def test_more_interface_types_with_complex_prototype(self):
        input = \
        """
        type Animal interface {
            get_volume(a int, b float, c Animal, d boolean, e string, m, n, p Animal) 
        }

        type Planet interface {
            is_destroyed(p int, m,n,p float, a, b, c string, e, f, g, h [1][2][3]boolean) float
        }
        """
        expect = str(
            Program(
                [
                    InterfaceType(
                        'Animal',
                        [
                            Prototype(
                                'get_volume',
                                [
                                    IntType(),
                                    FloatType(),
                                    Id('Animal'),
                                    BoolType(),
                                    StringType(),
                                    Id('Animal'),
                                    Id('Animal'),
                                    Id('Animal'),
                                ],
                                VoidType()
                            )
                        ]
                    ),
                    InterfaceType(
                        'Planet',
                        [
                            Prototype(
                                'is_destroyed',
                                [
                                    IntType(),
                                    FloatType(),
                                    FloatType(),
                                    FloatType(),
                                    StringType(),
                                    StringType(),
                                    StringType(),
                                    ArrayType(
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ],
                                        BoolType()
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ],
                                        BoolType()
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ],
                                        BoolType()
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3)
                                        ],
                                        BoolType()
                                    )
                                ],
                                FloatType()
                            )
                        ]
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 354))


    def test_prototype_weird(self):
        input = \
        """
        type Animal interface {
            cal(a,b,c,d,e,f,g,h,i [4][5][6]Animal) [4][5][6]Animal
        }
        """
        expect = str(
            Program(
                [
                    InterfaceType(
                        'Animal',
                        [
                            Prototype(
                                'cal',
                                [
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    ),
                                    ArrayType(
                                        [
                                            IntLiteral(4),
                                            IntLiteral(5),
                                            IntLiteral(6)
                                        ],
                                        Id('Animal')
                                    )
                                ],
                                ArrayType(
                                    [
                                        IntLiteral(4),
                                        IntLiteral(5),
                                        IntLiteral(6)
                                    ],
                                    Id('Animal')
                                )
                            )
                        ]
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 355))


    '''
    #==============================
    AST: AST.FuncDecl
    - name : str
    - params : List[ParamDecl]
    - retType : Type
    - block : Block
    #==============================
    '''
    '''
    #==============================
    AST: AST.ParamDecl
    - parName : str
    - parType : Type
    #==============================
    '''
    def test_basic_function_declaration(self):
        input = \
        """
            func print(test string) {
                print(test)
            }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'print',
                        [
                            ParamDecl('test', StringType())
                        ],
                        VoidType(),
                        Block(
                            [
                                FuncCall(
                                    'print',
                                    [
                                        Id('test')
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 356))


    def test_intermediate_function_declaration(self):
        input = \
        """
            func div (a int, b int) float {
                if (b == 0) {
                    return -1
                }
                return a / b
            }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'div',
                        [
                            ParamDecl('a', IntType()),
                            ParamDecl('b', IntType())
                        ],
                        FloatType(),
                        Block(
                            [
                                If(
                                    BinaryOp(
                                        '==',
                                        Id('b'),
                                        IntLiteral(0)
                                    ),
                                    Block(
                                        [
                                            Return(
                                                UnaryOp(
                                                    '-',
                                                    IntLiteral(1)
                                                )
                                            )
                                        ]
                                    ),
                                    None
                                ),
                                Return(
                                    BinaryOp(
                                        '/',
                                        Id('a'),
                                        Id('b')
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 357))


    def test_more_complex_function_declaration_with_many_parameters(self):
        input = \
        """
            func create_planet(p Planet, s Sand, w Water, l Light, h [100]Human, a,b,c,d,e Seed) Planet{
                return ((((1-2))))*2
            }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'create_planet',
                        [
                            ParamDecl('p', Id('Planet')),
                            ParamDecl('s', Id('Sand')),
                            ParamDecl('w', Id('Water')),
                            ParamDecl('l', Id('Light')),
                            ParamDecl('h', ArrayType(
                                [
                                    IntLiteral(100)
                                ],
                                Id('Human')
                            )),
                            ParamDecl('a', Id('Seed')),
                            ParamDecl('b', Id('Seed')),
                            ParamDecl('c', Id('Seed')),
                            ParamDecl('d', Id('Seed')),
                            ParamDecl('e', Id('Seed')),
                        ],
                        Id('Planet'),
                        Block(
                            [
                                Return(
                                    BinaryOp(
                                        '*',
                                        BinaryOp(
                                            '-',
                                            IntLiteral(1),
                                            IntLiteral(2)
                                        ),
                                        IntLiteral(2)
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 358))


    def test_more_more_function_declaration_with_for_basic(self):
        input = \
        """
            func loop(i,n int, a string) {
                for i < n {
                    print(i)
                    print(s)
                }
            }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'loop',
                        [
                            ParamDecl('i', IntType()),
                            ParamDecl('n', IntType()),
                            ParamDecl('a', StringType())
                        ],
                        VoidType(),
                        Block(
                            [
                                ForBasic(
                                    BinaryOp(
                                        '<',
                                        Id('i'),
                                        Id('n')
                                    ),
                                    Block(
                                        [
                                            FuncCall(
                                                'print',
                                                [
                                                    Id('i')
                                                ]
                                            ),
                                            FuncCall(
                                                'print',
                                                [
                                                    Id('s')
                                                ]
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 359))


    def test_function_declaration_for_step(self):
        input = \
        """
            func loop (a,b,c,d,e int, m,n,p float) int{
                for i:=0;i<100;i+=1 {
                    util.print(i)
                }
                return;
            }
        """
        expect = str(
            Program(
                [
                    FuncDecl(
                        'loop',
                        [
                            ParamDecl('a', IntType()),
                            ParamDecl('b', IntType()),
                            ParamDecl('c', IntType()),
                            ParamDecl('d', IntType()),
                            ParamDecl('e', IntType()),
                            ParamDecl('m', FloatType()),
                            ParamDecl('n', FloatType()),
                            ParamDecl('p', FloatType())
                        ],
                        IntType(),
                        Block(
                            [
                                ForStep(
                                    Assign(
                                        Id('i'),
                                        IntLiteral(0)
                                    ),
                                    BinaryOp(
                                        '<',
                                        Id('i'),
                                        IntLiteral(100)
                                    ),
                                    Assign(
                                        Id('i'),
                                        BinaryOp(
                                            '+',
                                            Id('i'),
                                            IntLiteral(1)
                                        )
                                    ),
                                    Block(
                                        [
                                            MethCall(
                                                Id('util'),
                                                'print',
                                                [
                                                    Id('i')
                                                ]
                                            )
                                        ]
                                    )
                                ),
                                Return(None)
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 360))


    def test_361(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 361))

    def test_362(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 362))

    def test_363(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 363))

    def test_364(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 364))

    def test_365(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 365))

    def test_366(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 366))

    def test_367(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 367))

    def test_368(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 368))

    def test_369(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 369))

    def test_370(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 370))

    def test_371(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 371))

    def test_372(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 372))

    def test_373(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 373))

    def test_374(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 374))

    def test_375(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 375))

    def test_376(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 376))

    def test_377(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 377))

    def test_378(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 378))

    def test_379(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 379))


    '''
    #==============================
    AST: Expression representation
    #==============================
    '''
    def test_380(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 380))

    def test_381(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 381))

    def test_382(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 382))

    def test_383(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 383))

    def test_384(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 384))

    def test_385(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 385))

    def test_386(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 386))

    def test_387(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 387))

    def test_388(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 388))

    def test_389(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 389))

    def test_390(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 390))

    def test_391(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 391))

    def test_392(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 392))

    def test_393(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 393))

    def test_394(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 394))

    def test_395(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 395))


    def test_396(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 396))


    def test_exp3(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 397))


    def test_exp2(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 398))


    def test_exp1(self):
        input = \
        """
        var a int = 1;
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(1))
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 399))