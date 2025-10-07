#Inicializacion del proyecto
 
#Creación del ejecutable para Windows
pyinstaller --windowed --name=Av-PDF --add-data "resource\\background.jpg;resource" --add-data "icono_16.png;." --add-data "icono.ico;."  --icon=icono.ico   .\main.py
