setup: requirements.txt
	python -m venv venv
	./venv/Scripts/pip.exe install -r requirements.txt

run:
	./venv/Scripts/python.exe app.py

clean:
	rmdir /S /Q venv
