# Note this make files is for help in local dev only 
create-env:
	python -m venv venv

# Local Dev Tip - Make wont activate the venv in your current shell as it executes in fresh shell
activate-env:
	.\venv\Scripts\activate 

deactivate-env:
	deactivate

install-requirements:
	pip install -r requirements.txt

run-test:
	python -m unittest discover

run-backend:
	uvicorn main:app --host 0.0.0.0 --port 8000
