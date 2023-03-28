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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.Translator import Translator
from numpy import double, dtype, int, shape
from ctypes import POINTER, c_double, c_int, c_void_p

PERMUTE_ROWS = 3
PERMUTE_COLUMNS = 4

imslstat = loadimsl(STAT)


def permuteMatrix(a, permutation, permute):
    """ Permutes the rows or columns of a matrix.
    """
    imslstat.imsls_d_permute_matrix.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_permute_matrix('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nColumns)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nColumns = shape[1]
    if (permute == PERMUTE_ROWS):
        nElements = nRows
    elif (permute == PERMUTE_COLUMNS):
        nElements = nColumns
    else:
        errStr = Translator.getString("permuteValueErr")
        raise ValueError(errStr)
    evalstring += ','
    permutation = toNumpyArray(
        permutation, 'permutation', shape=shape, dtype='int', expectedShape=(nElements))
    evalstring += 'permutation.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(permute)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nRows, nColumns), result=True, createArray=True)
