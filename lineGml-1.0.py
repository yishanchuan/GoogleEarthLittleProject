# -*- coding: utf8 -*-
import os
from igraph import *
from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from pygeocoder import Geocoder

def labelToInfo(address):
	return Geocoder.geocode(address)[0].coordinates

# resolve gml file who has longitude/latitude/label
def gmlToKml(gmlname):
	g=Graph.Read_GML(gmlpath+gmlname)
	
	#get List of longitude、latitude、ID、edge	
	listLabel=g.vs["label"]
	labelLen=len(listLabel)
	listEdge=g.get_edgelist()
	listLong=listLat=[]
	try:
		listLong=g.vs["Longitude"]
		listLat=g.vs["Latitude"]
	except Exception,e:
		# exception 'Attribute does not exist'
		print e,"!!! Filename is ",gmlname
		if 'Attribute does not exist' in e:
			try:
				for i in range(labelLen):
					listLong.append(labelToInfo(listLabel[i])[0])
					listLat.append(labelToInfo(listLabel[i])[1])
				if(len(listLat)!=labelLen or len(listLong)!=labelLen):
					print 'can\'t search the addresses'
					return None
			except Exception,e:
				print e
				return None
	except TypeError:
		print '!!!TypeError:',gmlname[:4]
		return None

	#num of nodes
	nodelen=len(listLong)

	#list's length is error, then raise exception
	if(len(listLat)!=labelLen):
		raise Exception("quantity of longitude isn't correspond with label.",len(listLong),labelLen)
	if(len(listLat)!=nodelen):
		raise Exception("longitude isn't correspond with latitude.",len(listLong),len(listLat))
	if(len<1):
		raise Exception("node number is too little.")


	#query List for tansforming gml to kml，node info leave longitude/latitude/label
	doc = KML.kml(
		KML.Document(
			KML.name(gmlname+'.kml'),
			KML.Style(
				KML.LineStyle(
					KML.color('ff0000ff'),
					KML.width('2')
					),
				KML.PolyStyle(
					KML.fill('0')
					),
				id=('inline')
				),
			KML.StyleMap(
				KML.Pair(
					KML.key('normal'),
					KML.styleUrl("#inline")
					),
				KML.Pair(
					KML.key('highlight'),
					KML.styleUrl("#inline")
					),
				id=('inline1')
				),
			KML.StyleMap(
				KML.Pair(
					KML.key('normal'),
					KML.styleUrl("#pushpin")
					),
				KML.Pair(
					KML.key('highlight'),
					KML.styleUrl("#pushpin1")
					),
				id=('pushpinm')
				),
			KML.Style(
				KML.IconStyle(
					KML.scale('1.1'),
					KML.Icon(
						KML.href('http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png')
						),
					KML.hotSpot(
						x=('20'),
						y=('2'),
						xunits=('pixels'),
						yunits=('pixels')
						),
					),
				id=('pushpin')
				),
			KML.Style(
				KML.IconStyle(
					KML.scale('1.3'),
					KML.Icon(
						KML.href('http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png')
						),
					KML.hotSpot(
						x=('20'),
						y=('2'),
						xunits=('pixels'),
						yunits=('pixels')
						),
					),
				id=('pushpin1')
				),
			KML.Folder(
				KML.name(gmlname),
				KML.open('1'),
				)
			)
		)

	#loop for vertex
	for i in range(nodelen):
		doc.Document.Folder.append(
			KML.Placemark(
				KML.name(listLabel[i]),
				KML.LookAt(
					KML.longitude(listLong[i]),
					KML.latitude(listLat[i]),
					KML.altitude(0),
					KML.heading(0),
					KML.tilt(0),
					KML.range(1000),
					GX.altitudeMode('relativeToGround')
				),
				KML.styleUrl('#pushpinm'),
				KML.Point(
					GX.drawOrder(1),
					KML.coordinates(str(listLong[i])+','+str(listLat[i])+',0')
				)
			),    
		)

	# loop for edge
	for i in range(len(listEdge)):
		doc.Document.Folder.append(
			KML.Placemark(
				KML.name('PATH'+str(i)),
				KML.styleUrl('#inline1'),
				KML.LineString(
					KML.tessellate(1),
					#GX.altitudeMode("relativeToSeaFloor"),
					KML.coordinates(
						str(listLong[listEdge[i][0]])+','+str(listLat[listEdge[i][0]])+','+'0 '+str(listLong[listEdge[i][1]])+','+str(listLat[listEdge[i][1]])+','+'0'
					)
				)
			)
		)

	#write to gmlname.file
	print gmlname[:-4]
	with open(kmlpath+gmlname[:-4]+'.kml','wt') as f:
		f.write(etree.tostring(doc, pretty_print=True))

# resolve gml file who don't have longitude and latitude
# perhaps in furture

#scan folder to get all '*.gml' files
if __name__=='__main__':
        gmlpath='./example/gml/'
        kmlpath='./example/kml/'
        fndir=[fn for fn in os.listdir(gmlpath) if fn.endswith('.gml')]
        map(gmlToKml,fndir)
		# failedFiles=[]
		# for i in range(len(fndir)):
			# returnValue=gmlToKml(fndir)
			# if(not returnValue):
				# failedFiles.append(returnValue)
