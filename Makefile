PHONY: win-unit-tests

win-unit-tests:
	@echo current directory :$(CURR_DIR)
	python -m pip install virtualenv
	del /Q tenv
	python -m virtualenv tenv 
	$(CURR_DIR)\tenv\Scripts\activate.bat
	$(CURR_DIR)\tenv\Scripts\python setup.py install -f --quiet
	$(CURR_DIR)\tenv\Scripts\python -m unittest discover $(CURR_DIR)\tests "test_*.py"