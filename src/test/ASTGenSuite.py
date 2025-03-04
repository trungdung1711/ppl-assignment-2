import unittest
from TestUtils import TestAST
from AST import *


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
    def test_309(self):
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
        var a int = 9999;
        var b float = 0.125;
        var c boolean = false;
        var d string = "Hello World\\n"
        """
        expect = str(
            Program(
                [
                    VarDecl('a', IntType(), IntLiteral(9999)),
                    VarDecl('b', FloatType(), FloatLiteral(0.125)),
                    VarDecl('c', BoolType(), BooleanLiteral(False)),
                    VarDecl('d', StringType(), StringLiteral('"Hello World\\n"'))
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
        var arr [0b01][0b10][0b11][0b100][0b101][ID]string = [2][2][2]int{ {{1, 2}, {3, 4}}, {{5, 6}, {7, 8}} }
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
                                ]
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
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 326))


    def test_327(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 327))

    def test_328(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 328))

    def test_329(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 329))

    def test_330(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 330))

    def test_331(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 331))

    def test_332(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 332))

    def test_333(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 333))

    def test_334(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 334))

    def test_335(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 335))

    def test_336(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 336))

    def test_337(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 337))

    def test_338(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 338))

    def test_339(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 339))

    def test_340(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 340))

    def test_341(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 341))

    def test_342(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 342))

    def test_343(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 343))

    def test_344(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 344))

    def test_345(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 345))

    def test_346(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 346))

    def test_347(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 347))

    def test_348(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 348))

    def test_349(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 349))


    def test_350(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 350))


    def test_351(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 351))


    def test_352(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 352))


    def test_353(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 353))


    def test_354(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 354))


    def test_355(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 355))


    def test_356(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 356))


    def test_357(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 357))


    def test_358(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 358))

    def test_359(self):
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
        self.assertTrue(TestAST.checkASTGen(input, expect, 359))

    def test_360(self):
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