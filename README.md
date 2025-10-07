### Inicializacion del proyecto
Las dependencias son trabajadas con con la herramienta uv
### Comando para crear el entorno virtual
 
#Creación del ejecutable para Windows
pyinstaller --windowed --name=Av-PDF --add-data "resource\\background.jpg;resource" --add-data "icono_16.png;." --add-data "icono.ico;."  --icon=icono.ico   .\main.py
