PHONY: win-unit-tests

win-unit-tests:
	python -m pip install virtualenv
	if exist tenv del /Q tenv
	python -m virtualenv tenv 
	$(CURR_DIR)\env\Scripts\activate.bat
	$(CURR_DIR)\env\Scripts\python setup.py install
	$(CURR_DIR)\env\Scripts\python -m unittest discover $(CURR_DIR)\tests "test_*.py"