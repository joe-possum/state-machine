default :
	echo "Only useful target is 'install'"

install :
	echo "#! /bin/env python3" > t.py
	echo "#\n# Installed from $PWD\n#" >> t.py
	cat state-machine.py >> t.py
	install -m 0755 t.py ~/bin/state-machine
	rm t.py
