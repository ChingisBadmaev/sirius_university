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
from pyimsl.util.imslUtils import STAT, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_ROWS = 40306
IMSLS_COLUMNS = 40302
IMSLS_INDEX = 40303
IMSLS_METHOD = 13170
IMSLS_SCALE = 14400
IMSLS_X_COL_DIM = 15470
imslstat = loadimsl(STAT)


def dissimilarities(x, rows=None, columns=None, index=None, method=None, scale=None, xColDim=None):
    """ Computes a matrix of dissimilarities (or similarities) between the columns (or rows) of a matrix.
    """
    imslstat.imsls_d_dissimilarities.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_dissimilarities('
    evalstring += 'c_int(nrow)'
    evalstring += ','
    evalstring += 'c_int(ncol)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nrow = shape[0]
    ncol = shape[1]
    if columns is None:
        rows = True  # default is rows
    checkForBoolean(rows, 'rows')
    if (rows):
        evalstring += ','
        evalstring += repr(IMSLS_ROWS)
    checkForBoolean(columns, 'columns')
    if (columns):
        evalstring += ','
        evalstring += repr(IMSLS_COLUMNS)
    if not (index is None):
        evalstring += ','
        evalstring += repr(IMSLS_INDEX)
        evalstring += ','
        evalstring += 'c_int(index_ndstm_tmp)'
        evalstring += ','
        index_ind_tmp = toNumpyArray(
            index, 'index', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'index_ind_tmp.ctypes.data_as(c_void_p)'
        index_ndstm_tmp = shape[0]
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (scale is None):
        evalstring += ','
        evalstring += repr(IMSLS_SCALE)
        evalstring += ','
        evalstring += 'c_int(scale)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    checkForBoolean(rows, 'rows')
    if (rows):
        m = nrow
    else:
        m = ncol
    return processRet(result, shape=(m, m), result=True)
