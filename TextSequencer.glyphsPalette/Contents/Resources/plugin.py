# encoding: utf-8

###########################################################################################################
#
#
#   Palette Plugin
#
#   Read the docs:
#   https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
from GlyphsApp.plugins import *
from textSplitter import splitText
from vanilla import *

class TextSequencer(PalettePlugin):
	
	padding = (10,10,10)
	btnH = 20
	txtH = 17

	# @objc.python_method
	def settings(self):
		self.name = "Text Sequencer"
		# Create Vanilla window and group with controls
		width = 200
		height = 211
		self.paletteView = Window((width, height))
		self.paletteView.group = Group((0, 0, width, height))
		x,y,p = self.padding
		self.paletteView.group.mainTitle = TextBox((x,y,-p,self.btnH), "main sequence")
		y += p + self.txtH
		self.paletteView.group.stringInputMain = EditText((x,y,-p,self.btnH))
		y += p + self.btnH
		self.paletteView.group.startEndTitle = TextBox((x,y,-p,self.btnH), "start/end")
		y += p + self.txtH
		self.paletteView.group.stringInputStart = EditText((x,y,100,self.btnH))
		self.paletteView.group.stringInputEnd = EditText((x+100,y,100,self.btnH))
		y += p + self.btnH

		self.paletteView.group.leftRightTitle = TextBox((x,y,-p,self.btnH), "left/right")
		y += p + self.txtH
		self.paletteView.group.stringInputLeft = EditText((x,y,100,self.btnH))
		self.paletteView.group.stringInputRight = EditText((x+100,y,100,self.btnH))
		y += p + self.btnH
		self.paletteView.group.apply = Button((x,y,-p,self.btnH), "Insert Inbetween", callback=self.insert)
		self.dialog = self.paletteView.group.getNSView()
	
	@objc.python_method
	def insert(self, sender):

		Glyphs.clearLog()

		tab = Glyphs.font.currentTab
		if tab is None: return

		font = Glyphs.font
		cmap = {int("0x"+glyph.unicode, 0):glyph.name for glyph in font.glyphs if glyph.unicode is not None}
		fontNames = [g.name for g in font.glyphs]
		masterId = None
		try:
			currLayer = font.selectedLayers[0]
			
			if currLayer is None:
				currMaster = font.masters[tab.masterIndex]
				masterId = currMaster.id
			else:
				masterId = currLayer.associatedMasterId
		except:
			currMaster = font.masters[tab.masterIndex]
			masterId = currMaster.id
			
		assert masterId is not None, "Master Id is None"

		
		tabLayers = [layer for layer in tab.layers]
		glyphsToInsert = splitText(self.paletteView.group.stringInputMain.get(), cmap)
		glyphsToInsertStart = splitText(self.paletteView.group.stringInputStart.get(), cmap)
		glyphsToInsertEnd = splitText(self.paletteView.group.stringInputEnd.get(), cmap)
		glyphsToInsertLeft = splitText(self.paletteView.group.stringInputLeft.get(), cmap)
		glyphsToInsertRight = splitText(self.paletteView.group.stringInputRight.get(), cmap)
		

		layersToInsert = []

		for name in glyphsToInsert:
			if name in fontNames:
				glyph = font[name]
				layer = glyph.layers[masterId]
				layersToInsert += [layer]

		layersToInsertStart = []

		for name in glyphsToInsertStart:
			if name in fontNames:
				glyph = font[name]
				layer = glyph.layers[masterId]
				layersToInsertStart += [layer]

		layersToInsertEnd = []

		for name in glyphsToInsertEnd:
			if name in fontNames:
				glyph = font[name]
				layer = glyph.layers[masterId]
				layersToInsertEnd += [layer]

		layersToInsertLeft = []

		for name in glyphsToInsertLeft:
			if name in fontNames:
				glyph = font[name]
				layer = glyph.layers[masterId]
				layersToInsertLeft += [layer]

		layersToInsertRight = []

		for name in glyphsToInsertRight:
			if name in fontNames:
				glyph = font[name]
				layer = glyph.layers[masterId]
				layersToInsertRight += [layer]

		if tab.textRange == 0:
			before_selection = []
			selection = tabLayers
			after_selection = []
		else:
			before_selection = tabLayers[:tab.textCursor]
			selection = tabLayers[tab.textCursor:tab.textCursor+tab.textRange]
			after_selection = tabLayers[tab.textCursor+tab.textRange:]

		######
		newTabLayers = before_selection
		newTabLayers += layersToInsertStart
		newTabLayers += layersToInsert
		for layer in selection:
			newTabLayers += layersToInsertLeft + [layer] + layersToInsertRight + layersToInsert
		newTabLayers += layersToInsertEnd
		newTabLayers += after_selection
		print("")
		print("***")
		for l in newTabLayers:
			if l.parent.name is None: continue
			print("/"+l.parent.name, end=" ")
		print()
		tab.layers = newTabLayers
		if tab.textRange != 0:
			tab.textRange = len(layersToInsertStart) + len(layersToInsertEnd) + len(selection)*len(layersToInsert)+len(layersToInsert)+len(selection) + len(layersToInsertLeft)+len(selection)+ len(layersToInsertRight)+len(selection)
		# # display all layers of one glyph next to each other
		# for layer in newTabLayers:
		# 	tab.layers.append(layer)
	


	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
	# Temporary Fix
	# Sort ID for compatibility with v919:
	_sortID = 0
	@objc.python_method
	def setSortID_(self, id):
		try:
			self._sortID = id
		except Exception as e:
			self.logToConsole( "setSortID_: %s" % str(e) )
	
	@objc.python_method
	def sortID(self):
		return self._sortID
	