gen :
	toilet --metal -t --font mono12  "gen"
	python run.py gen

lex :
	toilet --metal -t --font mono12  "lexer"
	python run.py test LexerSuite

par : 
	toilet --metal -t --font mono12  "parser"
	python run.py test ParserSuite

ast :
	toilet --metal -t --font mono12  "ast"
	python run.py test ASTGenSuite

all :
	toilet --metal -t --font mono12  "test all"
	bash ./run.sh

.PHONY : gen ast all lex par