from PyQt5 import QtCore, QtGui, QtWidgets
import biom
import sys


class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        
        self.existingFileList = []
        self.currentFileList = []
        self.tableList = []
        
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(642, 480)
        MainWindow.setFixedSize(642,480)
	
	# Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

	# topLeftFrame
        self.TopLeftFrame = QtWidgets.QFrame(self.centralwidget)
        self.TopLeftFrame.setGeometry(QtCore.QRect(0, 0, 451, 451))
        self.TopLeftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TopLeftFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TopLeftFrame.setObjectName("TopRighFrame")

	# -FileaddButton
        self.FileAddButton = QtWidgets.QPushButton(self.TopLeftFrame)
        self.FileAddButton.setGeometry(QtCore.QRect(0, 0, 451, 61))
        self.FileAddButton.setObjectName("FileAddButton")
        self.FileAddButton.clicked.connect(self.getFileList)
	
	# -Scrollable Area
        self.scrollArea = QtWidgets.QScrollArea(self.TopLeftFrame)
        self.scrollArea.setGeometry(QtCore.QRect(0, 60, 451, 391))
        self.scrollArea.setWidgetResizable(True)     
        self.scrollArea.setObjectName("scrollArea")
	
	# -scrollAreaWidgetContents
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 449, 389))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
       
        # Verticle Box
        self.vBox = QtWidgets.QVBoxLayout()
        self.vBox.setAlignment(QtCore.Qt.AlignTop)
        self.scrollAreaWidgetContents.setLayout(self.vBox)
	
	# -Setting Up widget for scrollArea to enable scroll bar
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

	# topRightFrame
        self.TopRightFrame = QtWidgets.QFrame(self.centralwidget)
        self.TopRightFrame.setGeometry(QtCore.QRect(450, 0, 191, 451))
        self.TopRightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TopRightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TopRightFrame.setObjectName("TopLeftFrame")

	# -metadatLabel
        self.MetadataLabel = QtWidgets.QLabel(self.TopRightFrame)
        self.MetadataLabel.setGeometry(QtCore.QRect(10, 0, 181, 51))
        self.MetadataLabel.setTextFormat(QtCore.Qt.AutoText)
        self.MetadataLabel.setObjectName("MetadataLabel")
	
	# Array of radiobutton for metadata
        self.metaRadioButtons = [QtWidgets.QRadioButton("Union", self.TopRightFrame), QtWidgets.QRadioButton("Intersection", self.TopRightFrame), QtWidgets.QRadioButton("NULL", self.TopRightFrame)]
        
        self.metaRadioButtons[0].setGeometry(QtCore.QRect(10, 50, 112, 23))
        self.metaRadioButtons[1].setGeometry(QtCore.QRect(10, 70, 112, 23))
        self.metaRadioButtons[2].setGeometry(QtCore.QRect(10, 90, 112, 23))
        self.metaRadioButtons[0].setChecked(True)
        self.metaRadioButtonsGroup = QtWidgets.QButtonGroup()
        for k in range(len(self.metaRadioButtons)):
	        self.metaRadioButtonsGroup.addButton(self.metaRadioButtons[k], k)
                
        # -format Lable
        self.formatLabel = QtWidgets.QLabel(self.TopRightFrame)
        self.formatLabel.setGeometry(QtCore.QRect(10, 140, 171, 31))
        self.formatLabel.setObjectName("formatLabel")

        # Array of radiobuttons for file format type
        self.formatRadioButtons = [QtWidgets.QRadioButton("JSON", self.TopRightFrame), QtWidgets.QRadioButton("HDF5", self.TopRightFrame)]
        
        self.formatRadioButtons[0].setGeometry(QtCore.QRect(10, 170, 112, 23))
        self.formatRadioButtons[1].setGeometry(QtCore.QRect(10, 190, 112, 23))
        self.formatRadioButtons[0].setChecked(True)
        self.formatRadioButtonsGroup = QtWidgets.QButtonGroup()
        for h in range(len(self.formatRadioButtons)):
                self.formatRadioButtonsGroup.addButton(self.formatRadioButtons[h], h)

	# -MergeButton
        self.MergeButton = QtWidgets.QPushButton(self.TopRightFrame)
        self.MergeButton.setGeometry(QtCore.QRect(10, 330, 171, 61))
        self.MergeButton.setObjectName("MergeButton")
        self.MergeButton.clicked.connect(self.merge)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    # Destroy Layout and Updating new file list 
    def destroyLayout(self, dindex):
        while self.vBox.count()>0:
                self.vBox.itemAt(0).widget().setParent(None)
        del self.existingFileList[dindex]
        self.fileSeq()
    
    
    # Union of Two lists 
    def union(self, list1, list2):
        final_list = list(set(list1)|set(list2))
        return sorted(final_list)


    # Getting File Name from Path
    def getFileName(self, Path):
        for j in range(len(Path)-1, -1, -1):
                if (not Path[j].isalnum()) and (Path[j] not in '!@#$%^&()_-+={}[];., '):
                        fileName = Path[j+1:len(Path)]
                        return fileName
    
    
    # file Listing ---------------------------------------------------------------
    def listFile(self, index):
    
        self.hboxwrapper = QtWidgets.QWidget()
        self.hbox = QtWidgets.QHBoxLayout()
 
        # -filelabel
        self.filelabel = QtWidgets.QLabel()
        self.filelabel.setText(str(index+1)+"."+" "+self.getFileName(self.existingFileList[index]))
        self.filelabel.setStyleSheet("background-color : rgba(245,240,240, 1); padding-left: 1em; ")
        self.filelabel.setFixedHeight(57)
        self.filelabel.setFixedWidth(350)
	
	# -fileCloser
        self.filecloser = QtWidgets.QPushButton()
        self.filecloser.setText("X")
        self.filecloser.setFixedHeight(57)
        self.filecloser.setFixedWidth(58)
        self.filecloser.clicked.connect(lambda: self.destroyLayout(index))
        
        self.hbox.addWidget(self.filelabel)
        self.hbox.addWidget(self.filecloser)
        self.hbox.setContentsMargins(0,0,0,0)
        
        self.hboxwrapper.setLayout(self.hbox)
        self.vBox.addWidget(self.hboxwrapper)
        
        self.hboxwrapper.setObjectName("hboxwrapper"+str(index))
        self.hbox.setObjectName("hbox"+str(index))
        self.filecloser.setObjectName("filecloser"+str(index))
        self.filelabel.setObjectName("filelabel"+str(index))
                        
                      
    # Generate file Sequence
    def fileSeq(self):
        for i in range(0, len(self.existingFileList)):
                self.listFile(i)
                
    
    # Getting File List After selecting File --------------------------
    def getFileList(self):
        self.fileNames = QtWidgets.QFileDialog.getOpenFileNames(MainWindow, "Select File", "", '.biom files (*.biom)')
	
        if self.fileNames[0]:
                self.filePathList = list(self.fileNames)
                self.filePathList.pop()
                self.filePathList = self.filePathList[0]
                print(self.filePathList)
                if self.currentFileList:
                        while self.vBox.count()>0:
                                self.vBox.itemAt(0).widget().setParent(None)
                self.currentFileList = self.union(self.filePathList, self.existingFileList)
                self.existingFileList = self.currentFileList
                print(self.existingFileList)
                self.fileSeq()
        else:
               QtWidgets.QMessageBox.about(MainWindow, "Import failed", "Import has failed. Please try again!")


    # retranslating UI -----------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", ".biom Merger"))
        self.FileAddButton.setText(_translate("MainWindow", "Click here to add file"))
        self.MetadataLabel.setText(_translate("MainWindow", "<html><head/><body><p>How to merge files\'<br/>metadata:</p></body></html>"))
        self.formatLabel.setText(_translate("MainWindow", "Encode file in format:"))
        self.MergeButton.setText(_translate("MainWindow", "Merge"))
        
    # merging Files
    def merge(self):
        if len(self.existingFileList)<2:
                QtWidgets.QMessageBox.about(MainWindow, "Can not merge files", "Please add minimum two files to merge.")
                return
                
        # Making list of table from file path
        try:
                for f in range(len(self.existingFileList)):
                        t = biom.load_table(self.existingFileList[f])
                        self.tableList.append(t)
        except:
                QtWidgets.QMessageBox.about(MainWindow, "Error", "Error occured while extarcting table from files.")
                return
        
        # Getting path to save new file
        self.fileSavingDialog = QtWidgets.QFileDialog.getSaveFileName(MainWindow, 'Save file as', '', '.biom files (*.biom)')
        self.fileSavingPath = self.fileSavingDialog[0]
        if not self.fileSavingPath:
                return

        # Checking Radio Buttons
        if self.metaRadioButtons[1].isChecked():
                self.meta = 'intersection'
        else: # self.metaRadioButtons[0].isChecked:
                self.meta = 'union'
           
          # Merging all files to make a new file
        self.finalTable = self.tableList[0]
        try:
                for tableindex in range(len(self.tableList)-1):
                        self.finalTable = self.finalTable.merge(self.tableList[tableindex+1], observation=self.meta, sample=self.meta)
        except:
                QtWidgets.QMessageBox.about(MainWindow, "Error", "Error occured while Merging Table")
        
        # Making File with json format     
        if self.formatRadioButtons[0].isChecked():
                if self.metaRadioButtons[2].isChecked():
                        self.finalTable.del_metadata()
                with open(self.fileSavingPath+'.biom', 'w') as fjson:
                        fjson.write(self.finalTable.to_json(" ")) 
                QtWidgets.QMessageBox.about(MainWindow, "Merge Completed", "File Saved as "+ self.getFileName(self.fileSavingPath)+".biom")                 
        # Making File with hdf5 format
        else:
                if self.metaRadioButtons[2].isChecked():
                        self.finalTable.del_metadata()
                with biom.util.biom_open(self.fileSavingPath+'.biom', 'w') as fhdf5:
                	self.finalTable.to_hdf5(fhdf5, " ")
                QtWidgets.QMessageBox.about(MainWindow, "Merge Completed", "File Saved as "+ self.getFileName(self.fileSavingPath)+".biom")
                        
                        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
