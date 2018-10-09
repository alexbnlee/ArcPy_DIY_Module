# coding=utf-8

import arcpy

def getLyrs():
	# 特别注意，直接拷过来代码会出错
	# 原因是拷过来的代码缩进是空格
	# 与自动缩进的 tab 键是不同的
	# 因此需要特别将空格删除，通过选中可看出区别
	"获取当前 mxd 文件的所有图层"
	mxd = arcpy.mapping.MapDocument("CURRENT")
	lyrs = arcpy.mapping.ListLayers(mxd)
	return lyrs

def getCurrentMxd():
	"获取当前 mxd 文件的 mxd"
	mxd = arcpy.mapping.MapDocument("CURRENT")
	return mxd

def getDataFrame_0():
	"获取当前 mxd 文件的第一个数据框架"
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd)[0]
	return df

def zoomToLyr( index ):
	"将地图缩放到指定的图层 —— index: 需要缩放图层的索引值"
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd)[0]
	lyrs = arcpy.mapping.ListLayers(mxd)
	df.extent = lyrs[index].getExtent()

def setEnvWorkspace( path ):
	"设置环境变量 —— path: 设置工作空间的路径"
	arcpy.env.workspace = path

def exportToJpeg( name ):
	"将地图文档出图 —— name: 输出图片的名称，需要带扩展名*.jpg"
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd)[0]
	arcpy.mapping.ExportToJPEG(mxd, arcpy.env.workspace+"\\"+name, resolution=300)

def restartArcpy():
	"重启ArcPy"
	import os
	import sys
	python = sys.executable
	os.execl(python, python, *sys.argv)

def sangJiMapping( start, end):
	"按照给定图层索引进行专题图制作"
	mxd = getCurrentMxd()
	df = getDataFrame_0()
	lyrs = getLyrs()
	loys = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
	setEnvWorkspace(r"D:\01-Working\2018\20180115-浓烟专题图\专题图-new")

	for i in range(start, end):
		lyrs[i].visible = True
		s = lyrs[i].name
		ih = s.find('-')
		iat = s.rfind('-')
		smon = s[ih-4:ih-2]
		sd = s[ih-2:ih]
		sh = s[ih+1:ih+3]
		sm = s[ih+3:ih+5]
		sat = s[iat+1]
		if sat=="A":
			loys[0].text = "卫星/传感器：MODIS-AQUA\n成像时间：2018年"+str(int(smon))+"月"+str(int(sd))+"日 "+str(sh)+":"+str(sm)+"\n制作单位：国家海洋环境监测中心"  
		else:
			loys[0].text = "卫星/传感器：MODIS-TERRA\n成像时间：2018年"+str(int(smon))+"月"+str(int(sd))+"日 "+str(sh)+":"+str(sm)+"\n制作单位：国家海洋环境监测中心"
		arcpy.RefreshActiveView()
		mxd.saveACopy(arcpy.env.workspace + "\\MODIS_2018" + str(smon).zfill(2) + str(sd).zfill(2) + ".mxd")
		exportToJpeg("MODIS_2018" + str(smon).zfill(2) + str(sd).zfill(2) + ".jpg")
		lyrs[i].visible = False

def findIndexByName( string ):
	lyrs = getLyrs()
	i = 0
	for lyr in lyrs:
		if lyr.name.find(string) >= 0:
			print "-Name: " + lyr.name
			print "-Index: " + str(i)
		i = i + 1