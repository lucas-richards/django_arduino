# Getting Started

run to create requieremnts.txt file
```
pipenv run pip freeze > requirements.txt 
```

## Deployment

`python -m pip install gunicorn.`

run command for deployment
`gunicorn mysite.wsgi`

## Static files

`pip install whitenoise`
`pipenv run pip freeze > requirements.txt`

add middleware
`'whitenoise.middleware.WhiteNoiseMiddleware' `
and
`if not DEBUG:`
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

