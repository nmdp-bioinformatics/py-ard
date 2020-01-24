===============================
py-ard
===============================


.. image:: https://img.shields.io/pypi/v/pyard.svg
        :target: https://pypi.python.org/pypi/pyard

.. image:: https://readthedocs.org/projects/pyars/badge/?version=latest
        :target: https://pyars.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


ARD reduction for HLA with python

* Free software: LGPL 3.0
* Documentation: https://pyard.readthedocs.io.


Install from source
-------------------

.. code-block::

	python3 -m venv venv
	source venv/bin/activate

	python setup.py install

Install from PyPi
-----------------

.. code-block::

	pip install py-ard


Example
-------

.. code-block:: python3

	from pyard import ARD

	# Initialize ARD object
	ard = ARD('3290')

	# Initialize with latest DB
	ard = ARD()

	allele = "A*01:01:01"

	ard.redux(allele, 'G')
	# >> 'A*01:01:01G'

	ard.redux(allele, 'lg')
	# >> 'A*01:01g'

	ard.redux(allele, 'lgx')
	# 'A*01:01'

	ard_gl = ard.redux_gl("A*01:01/A*01:01N+A*02:AB^B*07:02+B*07:AB", "G")
	# >>> ard_gl
	# 'B*07:02:01G+B*07:02:01G^A*01:01:01G+A*02:01:01G/A*02:02'


