===============================
pyARS
===============================


.. image:: https://img.shields.io/pypi/v/pyars.svg
        :target: https://pypi.python.org/pypi/pyars

.. image:: https://readthedocs.org/projects/pyars/badge/?version=latest
        :target: https://pyars.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


ARS reduction for HLA with python

* Free software: LGPL 3.0
* Documentation: https://pyars.readthedocs.io.

Install
-------

.. code-block::

	# from source
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	python setup.py install

	# from PyPi
	pip install pyars


Example
-------

.. code-block:: python3

	from pyars import ARS

	# Initialize ARS object
	ars = ARS('3290')

	allele = "A*01:01:01"

	ars.redux(allele, 'G')
	# >> 'A*01:01:01G'

	ars.redux(allele, 'lg')
	# >> 'A*01:01g'

	ars.redux(allele, 'lgx')
	# >> 'A*01:01'


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

