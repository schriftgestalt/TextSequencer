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
import objc
from GlyphsApp import Glyphs
from GlyphsApp.plugins import PalettePlugin
from textSplitter import splitText
from vanilla import *
from AppKit import NSRoundRectBezelStyle


def BezelButton(posSize, title, callback=None, sizeStyle="small"):
    button = Button(posSize, title, callback=callback, sizeStyle=sizeStyle)
    nsObj = button.getNSButton()
    nsObj.setBezelStyle_(NSRoundRectBezelStyle)
    return button


class TextSequencer(PalettePlugin):
    padding = (10, 10, 10)
    btnH = 20
    txtH = 17

    def settings(self):
        self.name = "Text Sequencer"
        # Create Vanilla window and group with controls
        width = 200
        height = 221
        x, y, p = self.padding
        self.paletteView = Window((width, height))

        self.mainGroup = Box("auto")
        self.mainGroup.mainTitle = TextBox((2, 0, -2, self.btnH), "main sequence")
        self.mainGroup.stringInputMain = EditText((2, self.btnH, -2, self.btnH))

        self.startGroup = Box("auto")
        self.endGroup = Box("auto")

        self.startGroup.startTitle = TextBox((0, 0, -0, self.btnH), "start")
        self.endGroup.endTitle = TextBox((0, 0, -0, self.btnH), "end")
        self.startGroup.stringInputStart = EditText((2, self.btnH, -2, self.btnH))
        self.endGroup.stringInputEnd = EditText((2, self.btnH, -2, self.btnH))

        self.startEndInputs = HorizontalStackView(
            "auto",
            views=[
                dict(view=self.startGroup),
                dict(view=self.endGroup),
            ],
            spacing=4,
            edgeInsets=(0, 0, 0, 0),
        )

        self.leftGroup = Box("auto")
        self.rightGroup = Box("auto")

        self.leftGroup.leftTitle = TextBox((0, 0, -0, self.btnH), "left")
        self.rightGroup.rightTitle = TextBox((0, 0, -0, self.btnH), "right")
        self.leftGroup.stringInputLeft = EditText((2, self.btnH, -2, self.btnH))
        self.rightGroup.stringInputRight = EditText((2, self.btnH, -2, self.btnH))

        self.leftRightInputs = HorizontalStackView(
            "auto",
            views=[
                dict(view=self.leftGroup),
                dict(view=self.rightGroup),
            ],
            spacing=4,
            edgeInsets=(0, 0, 0, 0),
        )

        self.apply = BezelButton("auto", "Insert", callback=self.insert)

        self.paletteView.group = VerticalStackView(
            (x, y, width - p, height - p),
            views=[
                dict(view=self.mainGroup),
                dict(view=self.startEndInputs),
                dict(view=self.leftRightInputs),
                dict(view=self.apply, height=36),
            ],
            spacing=4,
            edgeInsets=(4, 4, 4, 4),
        )

        self.dialog = self.paletteView.group.getNSStackView()

        self.setupFocusOrder()

    @objc.python_method
    def setupFocusOrder(self):
        self.mainGroup.stringInputMain._nsObject.setNextKeyView_(
            self.startGroup.stringInputStart._nsObject
        )
        self.startGroup.stringInputStart._nsObject.setNextKeyView_(
            self.endGroup.stringInputEnd._nsObject
        )
        self.endGroup.stringInputEnd._nsObject.setNextKeyView_(
            self.leftGroup.stringInputLeft._nsObject
        )
        self.leftGroup.stringInputLeft._nsObject.setNextKeyView_(
            self.rightGroup.stringInputRight._nsObject
        )
        self.rightGroup.stringInputRight._nsObject.setNextKeyView_(self.apply._nsObject)
        self.apply._nsObject.setNextKeyView_(self.mainGroup.stringInputMain._nsObject)

    @objc.python_method
    def insert(self, sender):
        Glyphs.clearLog()

        tab = Glyphs.font.currentTab
        if tab is None:
            return

        font = Glyphs.font
        cmap = {
            glyph.unicodeChar: glyph.name
            for glyph in font.glyphs
            if glyph.unicode is not None
        }
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
        glyphsToInsert = splitText(self.mainGroup.stringInputMain.get(), cmap)
        glyphsToInsertStart = splitText(self.startGroup.stringInputStart.get(), cmap)
        glyphsToInsertEnd = splitText(self.endGroup.stringInputEnd.get(), cmap)
        glyphsToInsertLeft = splitText(self.leftGroup.stringInputLeft.get(), cmap)
        glyphsToInsertRight = splitText(self.rightGroup.stringInputRight.get(), cmap)

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
            before_selection = tabLayers[: tab.textCursor]
            selection = tabLayers[tab.textCursor: tab.textCursor + tab.textRange]
            after_selection = tabLayers[tab.textCursor + tab.textRange:]

        newTabLayers = before_selection
        newTabLayers += layersToInsertStart
        newTabLayers += layersToInsert
        for layer in selection:
            newTabLayers += (
                layersToInsertLeft + [layer] + layersToInsertRight + layersToInsert
            )
        newTabLayers += layersToInsertEnd
        newTabLayers += after_selection
        print("")
        print("***")
        for layer in newTabLayers:
            if layer.parent.name is None:
                continue
            print("/" + layer.parent.name, end=" ")
        print()
        tab.layers = newTabLayers
        if tab.textRange != 0:
            tab.textRange = (
                len(layersToInsertStart)
                + len(layersToInsertEnd)
                + len(selection) * len(layersToInsert)
                + len(layersToInsert)
                + len(selection)
                + len(layersToInsertLeft)
                + len(selection)
                + len(layersToInsertRight)
                + len(selection)
            )

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
            self.logToConsole("setSortID_: %s" % str(e))

    @objc.python_method
    def sortID(self):
        return self._sortID
