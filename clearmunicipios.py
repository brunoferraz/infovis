from pykml import parser

with open("toy.kml", "r", encoding="utf8") as f:
    doc = parser.parse(f)

it = doc.iter()
print(it[0])

# PESQUISAR SOBRE ITERADORES

# from pykml import parser
# from os import path
# from lxml import etree

# # f = open("BR_Localidades_2010_v1.kml", "r")
# # f = open("novo.txt", "r")
# kml_file = path.join('BR_Localidades_2010_v1.kml')

# doc = etree.ElementTree
# # with open("BR_Localidades_2010_v1.kml", "r", encoding="utf8") as f:
# with open(kml_file, "r", encoding="utf8") as f:
#     doc = parser.parse(f).getroot()


# print(doc.Document.Schema)
# print("dfsdfds")

# # it = doc.iter()
# # print(doc[0])

# # print(it)
# # for i in it:
#     # print(i)
# # print(doc.iter())