from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont,  QColor, QPalette, QIntValidator
from PyQt5.QtCore import Qt
def main():
    
    app = QApplication([])

    window = QWidget()
    window.setGeometry(100, 100, 500, 500)

    mainLayout = QGridLayout(window)
    mainLayout.setContentsMargins(10, 10, 10, 10)
    mainLayout.setSpacing(10)

    gridFrame = QFrame(window)
    gridFrame.setFrameStyle(QFrame.Panel | QFrame.Raised)
    gridFrame.setLineWidth(2)
    gridLayout = QGridLayout(gridFrame)
    gridLayout.setSpacing(0)

    title = QLabel("Sudoku Solver", gridFrame)
    title.setAlignment(Qt.AlignHCenter)
    title.setFont(QFont('Arial', 16, QFont.Bold))
    gridLayout.addWidget(title, 0, 0, 1, 10)

    inputArray = [[0] * 9 for _ in range(9)]
    cellArray = []
    for row in range(9):
        cellRow = []
        for col in range(9):
            cell = QLineEdit(gridFrame)
            cell.setFixedSize(40, 40)
            cell.setAlignment(Qt.AlignCenter)
            cell.setFont(QFont('Arial', 12))
            cell.setMaxLength(1)
            cell.setFrame(True)

            validator = QIntValidator(1, 9)
            cell.setValidator(validator)

            palette = cell.palette()
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(200, 200, 200))
            cell.setPalette(palette)

            cell.textChanged.connect(lambda text, r=row, c=col: inputArray.__setitem__(r, inputArray[r].__setitem__(c, int(text) if text else 0) or inputArray[r]))

            gridLayout.addWidget(cell, row + 1, col + 1)

            if col % 3 == 0 and col != 0:
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setLineWidth(2)
                line.setFrameShadow(QFrame.Sunken)
                gridLayout.addWidget(line, 1, col + 1, 9, 1)
            cellRow.append(cell)
        cellArray.append(cellRow)

    solveButton = QPushButton("Solve", gridFrame)
    solveButton.clicked.connect(lambda: fillBoard(cellArray, inputArray))

    gridLayout.addWidget(solveButton, 11, 1, 1, 9)
    mainLayout.addWidget(gridFrame, 0, 0, Qt.AlignCenter)
    window.setLayout(mainLayout)

    window.show()

    app.exec()

def fillBoard(cells, inputs):
    if solveBoard(inputs):
        for cellRow, inputRow in zip(cells, inputs):
            for cell, inputNode in zip(cellRow, inputRow):
                cell.setText(str(inputNode))

def solveBoard(board):
    if not findEmpty(board):
        return True 
    
    row, col = findEmpty(board)

    for i in range(1, 10):
        if isValid(board, row, col, i):
            board[row][col] = i 
            if solveBoard(board):
                return True 
            board[row][col] = 0

    return False

def findEmpty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def isValid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
        
    for i in range(9): 
        if board[i][col] == num: 
            return False 
        
    startRow = (row // 3) * 3
    startCol = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[startRow + i][startCol + j] == num:
                return False 
            
    return True

if __name__ == '__main__': main()