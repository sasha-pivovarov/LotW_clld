# LotW_clld
Deployment (Linux options in brackets):
Install clld and its dependencies (sudo pip install clld)
Download and unzip lotw_dev.zip
Change current directory to lotw_dev (cd lotw_dev/) (probably cat lotw_dev on Windows?)
Run the setup file to install lotw_dev as a python package (python setup.py develop)
Populate the app database (python lotw_dev/scripts/initializedb.py development.ini)
Host the app (pserve --reload development.ini)
By default the app is hosted at 127.0.0.1:6543, you can visit it using your browser at this address. Edit development.ini to change this behavior.
