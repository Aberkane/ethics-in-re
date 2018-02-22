# parsePDF

## Author:
- **Abdel-Jaouad** Aberkane (5783909)

## Dependencies (Ubuntu):
- sudo apt-get install libpulse-dev
- sudo apt-get install swig
- sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-de
- sudo easy_install greenlet
- sudo easy_install gevent

## Documentation
The parsePDF script enables users to parse pdf's and calculate the most occuring noun chunks by making use of the spacy and textract library. 

Option 1: run the python script and add the directory in which the pdf files are stored as a argument. 

Option 2: run the python script in the directory where the pdf files are stored, in this case there is no need in passing on a argument while executing. 

Output: the script will create a folder in which the frequency of noun chunks for each article are stored in seperate text files that carry the same name as the articles. 
