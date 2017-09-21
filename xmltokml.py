# -*- coding: utf8 -*-

from igraph import *
from xml.dom.minidom as do

gmlname="Aarnet.gml"
g=Graph.Read_GML(gmlname)
#g.write_adjacency('adjacency.txt')
#g.write_graphml('66.graphml')

#获取经纬度List
listLong=g.vs["Longitude"]
listLat=g.vs["Latitude"]
listLabel=g.vs["label"]

#节点个数
nodelen=len(listLong)

#如果长度不匹配，抛异常
if(len(listLat)!=nodelen):
    raise Exception("longitude isn't correspond with latitude.",len(listLong),len(listLat))
if(len<1):
    raise Exception("node number is too little.")

doc = do.Document()
root = doc.createElement('kml')
root.setAttribute('xmlns','http://www.opengis.net/kml/2.2')
root.setAttribute('xmlns:gx','http://www.opengis.net/kml/2.2')
root.setAttribute('xmlns:kml','http://www.opengis.net/kml/2.2')
root.setAttribute('xmlns:atom','http://www.opengis.net/kml/2.2')

doc.appendChild(root)

nodeDocument = doc.createElement('Document')
