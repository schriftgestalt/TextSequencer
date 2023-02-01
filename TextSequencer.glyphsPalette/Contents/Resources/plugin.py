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
		width = 150
		height = 70
		self.paletteView = Window((width, height))
		self.paletteView.group = Group((0, 0, width, height))
		x,y,p = self.padding
		self.paletteView.group.stringEdit = EditText((x,y,-p,self.btnH))
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
		glyphsToInsert = splitText(self.paletteView.group.stringEdit.get(), cmap)
		layersToInsert = []
		for name in glyphsToInsert:
			if name in fontNames:
				glyph = font[name]
				layer = glyph.layers[masterId]
				layersToInsert += [layer]
		newTabLayers = []
		newTabLayers += layersToInsert
		for layer in tabLayers:
			newTabLayers += [layer] + layersToInsert
		print("")
		print("***")
		for l in newTabLayers:
			print(l)
		tab.layers = newTabLayers
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
	