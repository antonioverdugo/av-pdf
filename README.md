### Av-PDF
Es una aplicación escrita en Python para lanzar pdf en eventos en directo.
Su caracteristica principal es que, cuando nos entregan un contenido en PDF, poder abrirlo ponerlo a pantalla completa y si el ordenador estuviera en modo extendido saldría la presentación pdf en el segundo monitor.  
Si el contenido en pdf llega a la última página o diapositiva, aunque se siga pulsado el pasador no sale de esa última diaspositiva. Igual pasa con la página o diapositiva 1.  
Se puede pasar a la siguiente diapositivo con el pasador y con las teclas Space, Enter, Next, Preview etc.  
Si se quisiera salir de la presentación, al igual que con PowerPoint, se pulsa la tecla Scape.  
Es una herramienta principalmente para técnicos de audivisuales.  
Otra de sus caracteristicas es que es compatible con pasadores de diapositivas como logitech y demás utilizados muy habitualmente en sector audiovisual.    
### Started - Clonar el repositorio - Animate a contribuir
git clone https://github.com/antonioverdugo/av-pdf.git
### Crear el entorno virtual
La versión de Python viene en el archivo .python-version ya que se utiliza la herramienta [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv).  
Se puede mirar en la documentacion de UV para ver como se instala la herramienta de forma global y de esta manera con el comando:  
**uv sync**  
Con el anterior comando se crea el entorno virtual y se descangan las dependencias.
UV es una gran herramienta escrita en Rust que además te permite de forma facil instalar varias versiones de python.
### Creación del ejecutable para Windows
pyinstaller --windowed --name=Av-PDF --add-data "resource\\background.jpg;resource" --add-data "icono_16.png;." --add-data "icono.ico;."  --icon=icono.ico   .\main.py
### Creación del instalador con Inno Setup
Solo se dispone de una versión para Windows.  
Se ha creado el instalador con la herramienta [Inno Setup]([https://github.com/astral-sh/uv](https://jrsoftware.org/isinfo.php)).  
La configuración de Inno Setup se puede encontrar en el archivo installer.iss
### Roadmap
Creación de una versión para mac y linux.
