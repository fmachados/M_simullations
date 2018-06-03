# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:14:32 2018

@author: Marlon
"""

import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolTip
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtCore import QCoreApplication

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = "M simulation"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 540
        self.setWindowIcon(QtGui.QIcon("M.png"))
        
        bBrowse = QPushButton("Browse", self)
        bBrowse.move(570, 35)
        
        bRun = QPushButton("Run", self)
        bRun.move(570, 480)
        bRun.setToolTip("Run application")
        
        bBrowse.setToolTip("Browse")
        #bRun.clicked.connect(self.)
        
        self.InitWindow()
    
    def InitWindow(self):
        
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Status bar...")
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        editMenu = mainMenu.addMenu("Edit")
        viewMenu = mainMenu.addMenu("View")
        helpMenu = mainMenu.addMenu("Help")
        
        newAction = QAction("New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip("New project")
        #newAction.triggered.connect(self.Close)
        
        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save project")
        #saveAction.triggered.connect(self.Close)
        
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+E")
        exitAction.setStatusTip("Close application")
        exitAction.triggered.connect(self.Close)
        
        copyAction = QAction("Copy", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.setStatusTip("Copy to clipboard")
        #copyAction.triggered.connect(editMenu.copy)
        
        pasteAction = QAction("Paste", self)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.setStatusTip("Paste from clipboard")
        #pasteAction.triggered.connect(editMenu.paste)
                
        viewAction = QAction("View status", self, checkable = True)
        viewAction.setStatusTip("View status bar")
        viewAction.setChecked(True)
        viewAction.triggered.connect(self.toggleMenu)
        
        tutorialAction = QAction("Tutorial", self)
        tutorialAction.setStatusTip("Detailed tutorial")
        #tutorialAction.triggered.connect(editMenu.paste)
        
        aboutAction = QAction("About", self)
        aboutAction.setStatusTip("About this software")
        #aboutAction.triggered.connect(editMenu.paste)
        
        citationAction = QAction("Citation", self)
        citationAction.setStatusTip("Cite this software")
        #citationAction.triggered.connect(editMenu.paste)
        
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        viewMenu.addAction(viewAction)
        helpMenu.addAction(tutorialAction)
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(citationAction)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
        
    def Close(self):
        reply = QMessageBox.question(self, "Exit message", "Close application?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            
    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()
            
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        
        copyAction = contextMenu.addAction("Copy")
        pasteAction = contextMenu.addAction("Paste")
        quitAction = contextMenu.addAction("Quit")
        
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        
        if action == quitAction:
            self.close()
        
        
                    
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())