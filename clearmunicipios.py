from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from lxml import etree
from pykml import parser
from os import path


# doc = etree
# with open("toy.kml", "r", encoding="utf8") as f:
#     doc = parser.parse(f)

# root 
# with open("toy.kml", "r", encoding="utf8") as f:

# with open("toy.kml", "r") as fobj:
#         xml = fobj.read()
# root = parser.fromstring(xml)
# print(root)

# data = open('toy.kml', 'rb')
# xslt_content = data.read()
# root = etree.XML(xslt_content)
# print(root.tag)

    
# with open("toy.kml", "r") as fobj:
#         xml = fobj.read()
# root = etree.XML(xml.encode())

# for i in root:
#     print(i)
#CD_GEOCODMU

from os import path
from xml.etree.ElementTree import Element, SubElement, ElementTree

# kml_file = path.join('toy.kml')
kml_file = path.join('BR_Localidades_2010_v1.kml')

doc = etree
with open(kml_file, encoding="utf8") as f:
    doc = parser.parse(f).getroot()

file1 = open("coordinates.csv","a", encoding="utf8") 


csv_str = "IBGE_CODE, NOME, LONGITUDE, LATITUDE, ALTURA \n"
for i in doc.Document.Folder.Placemark:
    nome = i.name
    ibgeCode = i.ExtendedData.SchemaData.SimpleData[9]
    coordenadas = i.Point.coordinates
    csv_str += str(ibgeCode) + ","
    csv_str += nome + ","
    csv_str += coordenadas + "\n"  

file1.write(csv_str) 
file1.close() 