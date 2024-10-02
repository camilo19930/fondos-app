# fondos-app


genreamos la carpeta lib, la cual tiene todas las dependencias de la aplicacion
pip install -t lib -r requirements.txt
comprimimos la carpeta lib 
Compress-Archive lib/* aws_lanbda_artifact.zip

# Install lambda layers
``` 
    python3.11 -m pip install -r requirements.txt -t layers/python/lib/python3.11/site-packages 
```

# Logs lambda
sls logs -f {function-name}