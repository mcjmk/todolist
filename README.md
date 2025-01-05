# Todo list
A simple to-do list app built with Flask and JavaScript, designed to help you be more productive.


## Features:
- **Sort tasks**: by priority, urgency, or importance.
- **Mark progress**: see progress on tasks.
- **Cross out completed tasks**: with satisfaction :)


## Installation:

### 1. Clone the repository:
```bash
git clone https://github.com/mcjmk/todolist.git
cd todolist
```

### 2. Setup:

#### Using makefile:
```bash
make setup
```

#### Manually:
##### 1. Create virtual environment:
```bash
python -m venv env
```

##### 2. Activate virtual environment
- on Windows:
```bash
env\Scripts\activate
```
- on macOs/Linux:
```bash
source env/bin/activate
```

##### 3. Install dependencies:
```bash
pip install -r requirements.txt
```


## Running the App:
### Using makefile:
```bash
make run
```

### Manually (with activated venv):
```bash
python app.py
``` 

Go to http://127.0.0.1:5000/

Enjoy!

![img_1.png](img_1.png)
