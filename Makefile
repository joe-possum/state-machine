URL := ${shell git config --get remote.origin.url}
COMMIT := ${shell git log | grep commit | head -1}

default :
	echo "Only useful target is 'install'"

install : t.py
	install -m 0755 t.py ~/bin/state-machine
	rm t.py

t.py : state-machine.py Makefile
	echo "#! /bin/env python3" > t.py
	echo -e "#\n# Installed from ${URL}\n# ${COMMIT}\n#\n" >> t.py
#	echo -e "#\n# Installed from $PWD\n#" >> t.py
	cat state-machine.py >> t.py
