import pyscreenshot
from PIL import ImageGrab

class sudokuGrid:
    raw = []

    def __init__(self, rawInput: str):
        """
        main class for sudoku numbermanaging
        :param rawInput: generates a sudoku grid based
        on the rawInput list. The numers inside the list
        are the numbers from left to right of the rows
        of a normal sudokugrid, starting from the top
        """
        output = ""
        for i in rawInput:
            output = f"{output}{i},"

        output = output[:-1]
        self.raw = list(map(int, output.split(',')))

    def setLine(self, Input, line):
        """
        set a line to a given list
        :param line: represents the line to be modified
        :param Input: represents the Input List witch contains 9 caracters
        """
        self.raw[line * 9:((line * 9) + 9)] = Input

    def getLine(self, line):
        """
        returns a list containing the values of a given line
        :param line: indicates the line to return
        """
        return self.raw[line * 9:((line * 9) + 9)]

    def setColumn(self, Input, column):
        """
        set a colums to a given list
        :param column: represents the line to be modified
        :param Input: represents the Input List witch contains 9 caracters
        """
        x = 0
        for i in range(column, 81, 9):
            self.raw[i] = Input[x]
            x += 1

    def getColumn(self, column):
        """
        returns a list containing the values of a given column
        :param column: indicates the column to return
        """
        return self.raw[column: 81: 9]

    def setCube(self, Input, cube):
        """
        set a colums to a given list
        :param cube: represents the cube to be modified
        :param Input: represents the Input List witch contains 9 caracters
        """
        f = ((cube // 3) * 27) + ((cube % 3) * 3)
        self.raw[f:f + 3] = Input[0:3]
        self.raw[f + 9:f + 12] = Input[3:6]
        self.raw[f + 18:f + 21] = Input[6:9]

    def getCube(self, cube):
        """
        returns a list containing the values of a given Cube
        :param Cube: indicates the column to return
        """
        f = ((cube // 3) * 27) + ((cube % 3) * 3)
        return self.raw[f:f + 3] + self.raw[f + 9:f + 12] + self.raw[f + 18:f + 21]

    def printCube(self):
        print(' ')
        for i in range(9):
            print(self.getLine(i))
        print(' ')

class util:

    @staticmethod
    def getMissing(Input):
        """
        returns a list containing the numbers from 1 to 9 missing in Input
        :param Input: a 9 number long list of numbers to be searched
        """
        param = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        out = []
        for t in param:
            if not Input.count(t) > 0:
                out.append(t)
        return out

    @staticmethod
    def getMissingPos(Input):
        """
        :param Input: a 9 number long list of numbers to be searched
        :return returns a list containing all positions of 0
        """
        indices = []
        for e in range(len(Input)):
            if Input[e] == 0:
                indices.append(e)
        return indices

    @staticmethod
    def getRawPos(subIndex, Index, mode="r"):
        """
        :param subIndex: Index of the subclass
        :param Index: Index of the searched number inside teh subclass
        :param mode: type of subclass to search ["r" = raw, "l" = Line, "c" = Column, "C" = Cube]
        :return: returns the position of Index inside sudokuSolver.raw
        """
        if mode == "r":
            return Index
        elif mode == "l":
            return (subIndex * 9) + Index
        elif mode == "c":
            return (Index * 9) + subIndex
        elif mode == "C":
            f = ((subIndex // 3) * 27) + ((subIndex % 3) * 3)
            if Index < 3:
                return f + (Index % 3)
            elif Index < 6:
                return f + (Index % 3) + 9
            else:
                return f + (Index % 3) + 18

    @staticmethod
    def getLine(RawIndex):
        """
        :param RawIndex: Index to be searched
        :return: The Line the RawIndex touches
        """
        return RawIndex // 9

    @staticmethod
    def getColumn(RawIndex):
        """
        :param RawIndex: Index to be searched
        :return: The Column the RawIndex touches
        """
        return RawIndex % 9

    @staticmethod
    def getCube(RawIndex):
        """
        :param RawIndex: Index to be searched
        :return: The Cube the RawIndex touches
        """
        return ((RawIndex // 9) // 3) * 3 + (RawIndex % 9) // 3

    @staticmethod
    def listOverride(InputList, Input, Index):
        """
        :param InputList: Original List
        :param Input: List to be inserted
        :param Index: Index from where to start to overridden
        :return: returns a List of the sae lenght of Inputlist but
        the Items contained in it are overwritten by the Items of
        the second list, starting by a given Index
        """
        return InputList[:Index] + Input[Index - len(InputList) - 1:len(InputList) - Index] + InputList[Index + len(Input):]

    @staticmethod
    def fillMissing(Input):
        """
        Automaticly fills in the last missing gap. won't work
        if there is more than one ore none
        :param Input: Input list of 9 numbers
        :return: A full list from the Input
        """
        if len(util.getMissing(Input)) == 1:
            return util.listOverride(Input, util.getMissing(Input), util.getMissingPos(Input)[0])
        return Input




screen = read(ImageGrab.grab(317, 243, 906, 832))


sudoku = sudokuGrid('400962000760005020008070001050006800004003106300000005002000984800000200509027000')
sudoku.printCube()
ok0 = True
while ok0:
    sudoku1 = sudoku

    for i in range(0, 9):
        sudoku1.setLine(util.fillMissing(sudoku1.getLine(i)), i)
        sudoku1.setCube(util.fillMissing(sudoku1.getCube(i)), i)
        sudoku1.setColumn(util.fillMissing(sudoku1.getColumn(i)), i)

    for a in range(0, 9):
        for b in util.getMissing(sudoku1.getLine(a)):
            temp = []
            for c in util.getMissingPos(sudoku1.getLine(a)):
                rawPos = util.getRawPos(a, c, "l")
                if sudoku1.getCube(util.getCube(rawPos)).count(b) == 0 and sudoku1.getColumn(util.getColumn(rawPos)).count(b) == 0:
                    temp.append(c)
            if len(temp) == 1:
                sudoku1.setLine(util.listOverride(sudoku1.getLine(a), [b], temp[0]), a)

    if sudoku1.raw == sudoku.raw:
        ok0 = False
    sudoku = sudoku1

sudoku.printCube()
