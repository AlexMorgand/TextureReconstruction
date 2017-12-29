all:
	make -C src
run:
	make run -C src
documentation:
	cd doc && pdflatex main.tex
clean:
	rm -rf doc/main.aux doc/main.log doc/main.pdf src/*.oso src/*.pyc src/*.shader.osl	
