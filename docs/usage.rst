=====
Usage
=====

To use pyARS in a project::

    from pyard import ARD
	ard = ARD('3290')

	# 'A*01:01:01G'
	ard.redux("A*01:01:01", 'G')
	
	# 'A*01:01g'
	ard.redux(allele, 'lg')
	
	# 'A*01:01'
	ard.redux(allele, 'lgx')
	
	# 'B*07:01+B*07:02:01G^A*01:01:01G+A*02:01/A*02:02'
	ard_gl = ard.redux_gl("A*01:01/A*01:01N+A*02:AB^B*07:01+B*07:AB", "G")
