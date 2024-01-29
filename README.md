# Getting Started

run to create requieremnts.txt file
```
pipenv run pip freeze > requirements.txt 
```

## Deployment

`python -m pip install gunicorn.`

run command for deployment
`gunicorn mysite.wsgi`
