
# Lookin

ML Backend with FastAPI

## Installation


Clone project
```bash
  git clone https://github.com/CP-Lookin/ml-backend.git
```
Go to project directory
```bash
  cd backend-fastapi
```

Create virtual env
```bash
  python3 -m venv venv
```
Install all libraries
```bash
  pip install requirements.txt
``` 
Run project
```bash
  fastapi dev main.py
```


## API Reference

#### Predict images

```http
  POST /predict
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `file` | **Required**. The file to be uploaded for prediction  |



## Authors

- [@lookin](https://github.com/CP-Lookin/)

