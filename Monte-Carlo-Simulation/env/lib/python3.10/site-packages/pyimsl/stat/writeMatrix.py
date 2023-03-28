###########################################################################
# Copyright 2008-2019 Rogue Wave Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
###########################################################################
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForStr, fatalErrorCheck, loadimsl, toNumpyArray, toByte
from numpy import double, dtype, shape, transpose
from ctypes import c_char_p, c_int, c_void_p

IMSLS_TRANSPOSE = 15070
IMSLS_A_COL_DIM = 10170
IMSLS_PRINT_ALL = 13910
IMSLS_PRINT_LOWER = 13930
IMSLS_PRINT_UPPER = 13960
IMSLS_PRINT_LOWER_NO_DIAG = 13940
IMSLS_PRINT_UPPER_NO_DIAG = 13970
IMSLS_WRITE_FORMAT = 15410
IMSLS_NO_ROW_LABELS = 13360
IMSLS_ROW_NUMBER = 14340
IMSLS_ROW_NUMBER_ZERO = 14350
IMSLS_ROW_LABELS = 14330
IMSLS_NO_COL_LABELS = 13330
IMSLS_COL_NUMBER = 10760
IMSLS_COL_NUMBER_ZERO = 10770
IMSLS_COL_LABELS = 10750
imslstat = loadimsl(STAT)


def writeMatrix(title, a, transpose=None, aColDim=None, printAll=None, printLower=None,
                printUpper=None, printLowerNoDiag=None, printUpperNoDiag=None, writeFormat=None,
                noRowLabels=None, rowNumber=None, rowNumberZero=None, rowLabels=None, noColLabels=None,
                colNumber=None, colNumberZero=None, colLabels=None, column=False):
    """ Prints a rectangular matrix (or vector) stored in contiguous memory locations.
    """
    imslstat.imsls_d_write_matrix.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_write_matrix('
    checkForStr(title, 'title')
    evalstring += 'toByte(title)'
    evalstring += ','
    evalstring += 'c_int(nra)'
    evalstring += ','
    evalstring += 'c_int(nca)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    nra = shape[0]
    nca = shape[1]
    if (nca == 1) & (not column):
        nca = nra
        nra = 1
    checkForBoolean(transpose, 'transpose')
    if (transpose):
        evalstring += ','
        evalstring += repr(IMSLS_TRANSPOSE)
    if not (aColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_A_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(aColDim)'
    checkForBoolean(printAll, 'printAll')
    if (printAll):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_ALL)
    checkForBoolean(printLower, 'printLower')
    if (printLower):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LOWER)
    checkForBoolean(printUpper, 'printUpper')
    if (printUpper):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_UPPER)
    checkForBoolean(printLowerNoDiag, 'printLowerNoDiag')
    if (printLowerNoDiag):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LOWER_NO_DIAG)
    checkForBoolean(printUpperNoDiag, 'printUpperNoDiag')
    if (printUpperNoDiag):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_UPPER_NO_DIAG)
    if not (writeFormat is None):
        evalstring += ','
        evalstring += repr(IMSLS_WRITE_FORMAT)
        evalstring += ','
        checkForStr(writeFormat, 'writeFormat')
        evalstring += 'toByte(writeFormat)'
    checkForBoolean(noRowLabels, 'noRowLabels')
    if (noRowLabels):
        evalstring += ','
        evalstring += repr(IMSLS_NO_ROW_LABELS)
    checkForBoolean(rowNumber, 'rowNumber')
    if (rowNumber):
        evalstring += ','
        evalstring += repr(IMSLS_ROW_NUMBER)
    checkForBoolean(rowNumberZero, 'rowNumberZero')
    if (rowNumberZero):
        evalstring += ','
        evalstring += repr(IMSLS_ROW_NUMBER_ZERO)
    if not (rowLabels is None):
        evalstring += ','
        evalstring += repr(IMSLS_ROW_LABELS)
        evalstring += ','
        rlabel = (c_char_p * len(rowLabels))()
        for i in range(0, len(rowLabels)):
            rlabel[i] = toByte(rowLabels[i])
        evalstring += 'rlabel'
    checkForBoolean(noColLabels, 'noColLabels')
    if (noColLabels):
        evalstring += ','
        evalstring += repr(IMSLS_NO_COL_LABELS)
    checkForBoolean(colNumber, 'colNumber')
    if (colNumber):
        evalstring += ','
        evalstring += repr(IMSLS_COL_NUMBER)
    checkForBoolean(colNumberZero, 'colNumberZero')
    if (colNumberZero):
        evalstring += ','
        evalstring += repr(IMSLS_COL_NUMBER_ZERO)
    if not (colLabels is None):
        evalstring += ','
        evalstring += repr(IMSLS_COL_LABELS)
        evalstring += ','
        clabel = (c_char_p * len(colLabels))()
        for i in range(0, len(colLabels)):
            clabel[i] = toByte(colLabels[i])
        evalstring += 'clabel'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
