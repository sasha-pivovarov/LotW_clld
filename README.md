# LotW_clld
Deployment (Linux options in brackets):
- Install clld and its dependencies (sudo pip install clld)
- Download and unzip lotw_dev.zip
- Change current directory to lotw_dev (cd lotw_dev/) (probably cat lotw_dev on Windows?)
- Run the setup file to install lotw_dev as a python package (python setup.py develop)
- Populate the app database (python lotw_dev/scripts/initializedb.py development.ini)
- Host the app (pserve --reload development.ini)
- By default the app is hosted at 127.0.0.1:6543, you can visit it using your browser at this address. Edit development.ini to change this behavior.

Установка на Windows:
- Скачать файлы проекта с Github (Clone or Download - Download ZIP)
- Распаковать скачанный архив и вложенный в него архив lotw_dev.zip
- Открыть командную строку
- Установить clld и её зависимости (python -m pip install clld)
- Перейти в директорию проекта (Здесь подразумевается, что проект был скачан в С:\Downloads. cd C:\Downloads\LotW_clld-master\lotw_dev)
- Запустить файл setup.py с опцией develop (python setup.py develop)
- Раздать приложение (python -m pyramid.scripts.pserve --reload development.ini).
- Перейти в браузере по адресу 127.0.0.1:6543 

Возможные проблемы:
- На шаге 4 сообщается, что python не является командой. Проверьте, есть ли на диске C папка Python27. Если есть, то нужно добавтить python в переменную PATH (set PATH=%PATH%;C:\Python27). Если такой нет, скачайте последнюю версию Python2 с сайта python.org и установите её. На этапе установки отметьте галочкой пункт "добавить Python к PATH.
- На шаге 4 сообщается об отсутствии pip. Это значит, что у вас стоит старая версия Python, которая поставлялась без него. Честно говоря, тут проще обновить Python (это, к тому же, и вообще полезно), так что скачайте последнюю версию Python2 и установите её.
