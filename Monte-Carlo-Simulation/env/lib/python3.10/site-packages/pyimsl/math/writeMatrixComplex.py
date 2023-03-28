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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, checkForStr, d_complex, fatalErrorCheck, loadimsl, toNumpyArray, toByte
from numpy import dtype, shape, transpose
from ctypes import byref, c_char_p, c_int
from .mathStructs import d_complex

IMSL_TRANSPOSE = 10001
IMSL_A_COL_DIM = 10003
IMSL_PRINT_ALL = 10040
IMSL_PRINT_LOWER = 10211
IMSL_PRINT_UPPER = 10212
IMSL_PRINT_LOWER_NO_DIAG = 10213
IMSL_PRINT_UPPER_NO_DIAG = 10214
IMSL_WRITE_FORMAT = 10044
IMSL_ROW_LABELS = 10042
IMSL_NO_ROW_LABELS = 10216
IMSL_ROW_NUMBER = 10268
IMSL_ROW_NUMBER_ZERO = 10215
IMSL_COL_LABELS = 10043
IMSL_NO_COL_LABELS = 10218
IMSL_COL_NUMBER = 10269
IMSL_COL_NUMBER_ZERO = 10217
IMSL_RETURN_STRING = 50010
IMSL_WRITE_TO_CONSOLE = 50011
imslmath = loadimsl(MATH)


def writeMatrixComplex(title, a, transpose=None, aColDim=None, printAll=None,
                       printLower=None, printUpper=None, printLowerNoDiag=None, printUpperNoDiag=None,
                       writeFormat=None, rowLabels=None, noRowLabels=None, rowNumber=None,
                       rowNumberZero=None, colLabels=None, noColLabels=None, colNumber=None,
                       colNumberZero=None, returnString=None, writeToConsole=None, column=False):
    """ Prints a rectangular matrix (or vector) stored in contiguous memory locations.
    """
    imslmath.imsl_z_write_matrix.restype = None
    shape = []
    evalstring = 'imslmath.imsl_z_write_matrix('
    checkForStr(title, 'title')
    evalstring += 'toByte(title)'
    evalstring += ','
    evalstring += 'c_int(nra)'
    evalstring += ','
    evalstring += 'c_int(nca)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='d_complex',
                     expectedShape=(0, 0))
    evalstring += 'a'
    nra = shape[0]
    nca = shape[1]
    if (nca == 1) & (not column):
        nca = nra
        nra = 1
    checkForBoolean(transpose, 'transpose')
    if (transpose):
        evalstring += ','
        evalstring += repr(IMSL_TRANSPOSE)
    if not (aColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_A_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(aColDim)'
    checkForBoolean(printAll, 'printAll')
    if (printAll):
        evalstring += ','
        evalstring += repr(IMSL_PRINT_ALL)
    checkForBoolean(printLower, 'printLower')
    if (printLower):
        evalstring += ','
        evalstring += repr(IMSL_PRINT_LOWER)
    checkForBoolean(printUpper, 'printUpper')
    if (printUpper):
        evalstring += ','
        evalstring += repr(IMSL_PRINT_UPPER)
    checkForBoolean(printLowerNoDiag, 'printLowerNoDiag')
    if (printLowerNoDiag):
        evalstring += ','
        evalstring += repr(IMSL_PRINT_LOWER_NO_DIAG)
    checkForBoolean(printUpperNoDiag, 'printUpperNoDiag')
    if (printUpperNoDiag):
        evalstring += ','
        evalstring += repr(IMSL_PRINT_UPPER_NO_DIAG)
    if not (writeFormat is None):
        evalstring += ','
        evalstring += repr(IMSL_WRITE_FORMAT)
        evalstring += ','
        checkForStr(writeFormat, 'writeFormat')
        evalstring += 'writeFormat'
    if not (rowLabels is None):
        evalstring += ','
        evalstring += repr(IMSL_ROW_LABELS)
        evalstring += ','
        rlabel = (c_char_p * len(rowLabels))()
        for i in range(0, len(rowLabels)):
            rlabel[i] = rowLabels[i]
        evalstring += 'rlabel'
    checkForBoolean(noRowLabels, 'noRowLabels')
    if (noRowLabels):
        evalstring += ','
        evalstring += repr(IMSL_NO_ROW_LABELS)
    checkForBoolean(rowNumber, 'rowNumber')
    if (rowNumber):
        evalstring += ','
        evalstring += repr(IMSL_ROW_NUMBER)
    checkForBoolean(rowNumberZero, 'rowNumberZero')
    if (rowNumberZero):
        evalstring += ','
        evalstring += repr(IMSL_ROW_NUMBER_ZERO)
    if not (colLabels is None):
        evalstring += ','
        evalstring += repr(IMSL_COL_LABELS)
        evalstring += ','
        clabel = (c_char_p * len(colLabels))()
        for i in range(0, len(colLabels)):
            clabel[i] = colLabels[i]
        evalstring += 'clabel'
    checkForBoolean(noColLabels, 'noColLabels')
    if (noColLabels):
        evalstring += ','
        evalstring += repr(IMSL_NO_COL_LABELS)
    checkForBoolean(colNumber, 'colNumber')
    if (colNumber):
        evalstring += ','
        evalstring += repr(IMSL_COL_NUMBER)
    checkForBoolean(colNumberZero, 'colNumberZero')
    if (colNumberZero):
        evalstring += ','
        evalstring += repr(IMSL_COL_NUMBER_ZERO)
    if not (returnString is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_STRING)
        checkForList(returnString, 'returnString')
        evalstring += ','
        returnString_string_tmp = c_char_p()
        evalstring += 'byref(returnString_string_tmp)'
    checkForBoolean(writeToConsole, 'writeToConsole')
    if (writeToConsole):
        evalstring += ','
        evalstring += repr(IMSL_WRITE_TO_CONSOLE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (returnString is None):
        processRet(returnString_string_tmp, shape=1, pyvar=returnString)
    return
