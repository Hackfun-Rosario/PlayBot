# Telegram Playlist Bot

## Pre-requisitos
La aplicación depende de `Python >3.5`. Antes de correrla es recomendable crear un entorno virtual usando virtualenv.

### Instalar las dependencias
`pip install -r requirements.txt`

## Ejecución
La aplicación está dividida en tres partes:

1. el bot de telegram
2. el servidor web
3. el broker

Dentro del directorio `bin` hay 3 archivos bash para arrancar y parar los servicios.

### Primer paso!!!
Antes que nada hay que iniciar el broker para enviar y recibir mensajes
`bin/broker.sh`

### Siguiente paso
Es indistinto el orden para el servidor http y el bot
`bin/http.sh`

### Y por último
Reemplazar el valor de BOT_KEY por la key del bot que te da Telegram
`BOT_KEY=la_key_de_tu_bot bin/bot.sh`

### Detener todos los servicios
Este comando detiene TODOS los servicios de forma indistinta
`bin/stop.sh`
