.PHONY: \
	list \
	emacs \
	emacs_clean \
	python3 \
	python3_clean \
	version

list:
	@ py/mk-list.py Makefile
	@ ls -1 $$HOME/build

emacs :
	sh/co-emacs.sh

emacs_clean:
	cd $$HOME/build; rm -rf emacs

python3:
	sh/co-python.sh

python3_clean:
	cd $$HOME/build; rm -rf python-3.7

version:
	@ mk-version.py $$HOME/local/bin/emacs
	@ mk-version.py $$HOME/local/bin/python3
	@ emacs-version.py
	@ python3 --version

