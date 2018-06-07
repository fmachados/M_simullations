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
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QCoreApplication

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = "M simulation"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 680
        self.setWindowIcon(QtGui.QIcon("M.png"))

        self.InitWindow()
    
    def InitWindow(self):
        
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
        citationAction.triggered.connect(self.Citation)
        
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        viewMenu.addAction(viewAction)
        helpMenu.addAction(tutorialAction)
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(citationAction)
                
        # fields to be used by the user
        self.lineedit = QLineEdit("Directory/Occurrence_data.csv", self)
        self.lineedit.resize(540, 30)
        self.lineedit.move(15, 50)
        
        self.lineedit = QLineEdit("Current_variables/", self)
        self.lineedit.resize(540, 30)
        self.lineedit.move(15, 120)
        
        self.lineedit = QLineEdit("5", self)
        self.lineedit.resize(250, 30)
        self.lineedit.move(15, 190)
        
        self.lineedit = QLineEdit("25", self)
        self.lineedit.resize(250, 30)
        self.lineedit.move(305, 190)
        
        self.lineedit = QLineEdit("1000", self)
        self.lineedit.resize(250, 30)
        self.lineedit.move(15, 260)
        
        self.lineedit = QLineEdit("100", self)
        self.lineedit.resize(250, 30)
        self.lineedit.move(305, 260)
        
        self.lineedit = QLineEdit("Select dispersal kernel", self)
        self.lineedit.resize(540, 30)
        self.lineedit.move(15, 330)
        
        self.lineedit = QLineEdit("Past_variables/", self)
        self.lineedit.resize(540, 30)
        self.lineedit.move(15, 400)
        
        self.lineedit = QLineEdit("500", self)
        self.lineedit.resize(250, 30)
        self.lineedit.move(15, 470)
        
        self.lineedit = QLineEdit("95", self)
        self.lineedit.resize(250, 30)
        self.lineedit.move(305, 470)
        
        self.lineedit = QLineEdit("Directory/", self)
        self.lineedit.resize(540, 30)
        self.lineedit.move(15, 540)
        
        # labels for fields
        self.label1 = QLabel("Occurrences (.csv)", self)
        self.label1.move(15, 25)
        
        self.label1 = QLabel("Current scenario", self)
        self.label1.move(15, 95)
        
        self.label1 = QLabel("Threshold (% E)", self)
        self.label1.move(15, 165)
        
        self.label1 = QLabel("% initial records", self)
        self.label1.move(305, 165)
        
        self.label1 = QLabel("Time steps", self)
        self.label1.move(15, 235)
        
        self.label1 = QLabel("Replicates", self)
        self.label1.move(305, 235)
        
        self.label1 = QLabel("Dispersal kernel", self)
        self.label1.move(15, 305)
        
        self.label1 = QLabel("Past scenario", self)
        self.label1.move(15, 375)
        
        self.label1 = QLabel("(optional)", self)
        self.label1.move(83, 375)
        
        self.label1 = QLabel("Burn in (if Past", self)
        self.label1.move(15, 445)
        
        self.label1 = QLabel("scenario is set)", self)
        self.label1.move(90, 445)
        
        self.label1 = QLabel("M confidence", self)
        self.label1.move(305, 445)
        
        self.label1 = QLabel("Output directory", self)
        self.label1.move(15, 515)
        
        # buttons for each field
        bBrowse = QPushButton("Browse", self)
        bBrowse.move(570, 50)
        bBrowse.setToolTip("Browse")
        #bBrowse.clicked.connect(self.)
        
        bBrowse = QPushButton("Browse", self)
        bBrowse.move(570, 120)
        bBrowse.setToolTip("Browse")
        #bBrowse.clicked.connect(self.)
        
        bBrowse = QPushButton("Select", self)
        bBrowse.move(570, 330)
        bBrowse.setToolTip("Select dispersal kernel")
        #bBrowse.clicked.connect(self.)
        
        bBrowse = QPushButton("Browse", self)
        bBrowse.move(570, 400)
        bBrowse.setToolTip("Browse")
        #bBrowse.clicked.connect(self.)
        
        bBrowse = QPushButton("Browse", self)
        bBrowse.move(570, 540)
        bBrowse.setToolTip("Browse")
        #bBrowse.clicked.connect(self.)
        
        bRun = QPushButton("Run", self)
        bRun.move(570, 620)
        bRun.setToolTip("Run application")
        #bRun.clicked.connect(self.)
        
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Status bar...")

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
    
    def Citation(self):
        citation = """Authors. 2018. M simulation: A sofware for constructing hypotheses 
of M areas for ecological niche modeling. Journal v:p-p."""
        QMessageBox.information(self, "Citation", citation,
                             QMessageBox.Ok, QMessageBox.Ok)

        
                    
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())