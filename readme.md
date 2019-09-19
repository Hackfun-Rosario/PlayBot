# Telegram Playlist Bot

## Pre-requisitos
La aplicación depende de `Python >3.5`. Antes de correrla es recomendable crear un entorno virtual usando virtualenv.

### Instalar las dependencias
`pip install -r requirements.txt`

## Ejecución
La aplicación está dividida en dos partes:

1. el bot de telegram
2. el servidor web

Dentro del directorio `bin` hay 3 archivos bash para arrancar y parar los servicios.

### Iniciar el servidor
`bin/http.sh`

### Iniciar el bot
`BOT_KEY=la_key_de_tu_bot bin/bot.sh`

### Detener todos los servicios
`/bin/stop.sh`
