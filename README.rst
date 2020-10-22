===============================
py-ard
===============================


.. image:: https://img.shields.io/pypi/v/py-ard.svg
        :target: https://pypi.python.org/pypi/py-ard

.. image:: https://readthedocs.org/projects/pyars/badge/?version=latest
        :target: https://pyard.readthedocs.io/en/latest/?badge=latest
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

Testing
-------

To run behavior-driven development (BDD) tests locally via the behave framework,
you'll need to set up a virtual environment. See Install from source

.. code-block::

    # Install test dependencies
    pip install --upgrade pip
    pip install -r test-requirements.txt

    # Running Behave and all BDD tests
    behave

Example
-------

.. code-block:: python3

    import pyard

    # Initialize ARD object with a version of IMGT HLA database
    ard = pyard.ARD(3290)

    # You can specify a data directory for temp files
    # ard = pyard.ARD('3290', data_dir='/tmp/py-ard')

    # Initialize with latest IMGT HLA database
    ard = pyard.ARD()

    # You can choose to refresh the MAC code for previously used versions
    # ard =  pyard.ARD(3290, refresh_mac=True)

    # Allele to reduce
    allele = "A*01:01:01"

    ard.redux(allele, 'G')
    # 'A*01:01:01G'

    ard.redux(allele, 'lg')
    # 'A*01:01g'

    ard.redux(allele, 'lgx')
    # 'A*01:01'

    ard.redux_gl("A*01:01/A*01:01N+A*02:AB^B*07:02+B*07:AB", "G")
    # 'B*07:02:01G+B*07:02:01G^A*01:01:01G+A*02:01:01G/A*02:02'

    # py-ard can also reduce serology based typings
    ard.redux_gl('HLA-A*10^HLA-A*9', 'lg')
    # 'HLA-A*24:19g/HLA-A*24:22g^HLA-A*26:01g/HLA-A*26:10g/HLA-A*26:15g/HLA-A*26:92g/HLA-A*66:01g/HLA-A*66:03g'


