# /bin/bash
toilet --metal -t --font mono12  "gen"
python run.py gen


toilet --metal -t --font mono12  "lexer"
python run.py test LexerSuite


toilet --metal -t --font mono12  "parser"
python run.py test ParserSuite


toilet --metal -t --font mono12  "ast"
python run.py test ASTGenSuite