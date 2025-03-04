gen :
	toilet --metal -t --font mono12  "gen"
	python run.py gen

test :
	toilet --metal -t --font mono12  "ast"
	python run.py test ASTGenSuite

all :
	toilet --metal -t --font mono12  "test all"
	bash ./run.sh

.PHONY : gen test all