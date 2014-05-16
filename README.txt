Instalacao
-------------

Usando python 2.4 e virtualenv::

	virtualenv env
	source env/bin/activate


Atualizamos o setuptools::

	python ez_setup.py

Rodamos o bootstrap e o buildout::
	
	python bootstrap.py
	./bin/buildout

Iniciamos a instância::

	./bin/instance fg

Criamos a estrutura de pastas (via ZMI)::

	/clientes/softwarelivre

Importamos o arquivo zexp dentro de **/clientes/softwarelivre/**
