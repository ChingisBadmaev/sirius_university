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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import array, double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_INDICES_KEYS = 12310
IMSLS_FREQUENCIES = 11790
IMSLS_ASCENDING = 10120
IMSLS_DESCENDING = 11180
IMSLS_ACTIVE = 10030
IMSLS_PASSIVE = 13710
IMSLS_PERMUTATION = 13750
IMSLS_TABLE = 14950
IMSLS_LIST_CELLS = 12800
IMSLS_N = 13270
imslstat = loadimsl(STAT)


def sortData(x, nKeys, xColDim=None, indicesKeys=None, frequencies=None, ascending=None, descending=None, active=None, passive=None, permutation=None, table=None, listCells=None, n=None):
    """ Sorts observations by specified keys, with option to tally cases into a multi-way frequency table.
    """
    imslstat.imsls_d_sort_data.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_sort_data('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x_tmp = toNumpyArray(x, 'x', shape=shape,
                         dtype='double', expectedShape=(0, 0))
    evalstring += 'x_tmp.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nVariables = shape[1]
    evalstring += ','
    evalstring += 'c_int(nKeys)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (indicesKeys is None):
        evalstring += ','
        evalstring += repr(IMSLS_INDICES_KEYS)
        evalstring += ','
        indicesKeys = toNumpyArray(
            indicesKeys, 'indicesKeys', shape=shape, dtype='int', expectedShape=(nKeys))
        evalstring += 'indicesKeys.ctypes.data_as(c_void_p)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    checkForBoolean(ascending, 'ascending')
    if (ascending):
        evalstring += ','
        evalstring += repr(IMSLS_ASCENDING)
    checkForBoolean(descending, 'descending')
    if (descending):
        evalstring += ','
        evalstring += repr(IMSLS_DESCENDING)
    checkForBoolean(active, 'active')
    if (active):
        evalstring += ','
        evalstring += repr(IMSLS_ACTIVE)
    checkForBoolean(passive, 'passive')
    if (passive):
        evalstring += ','
        evalstring += repr(IMSLS_PASSIVE)
    if not (permutation is None):
        evalstring += ','
        evalstring += repr(IMSLS_PERMUTATION)
        checkForList(permutation, 'permutation')
        evalstring += ','
        permutation_permutation_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(permutation_permutation_tmp)'
    if not (table is None):
        evalstring += ','
        evalstring += repr(IMSLS_TABLE)
        checkForDict(table, 'table', [])
        evalstring += ','
        table_nValues_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(table_nValues_tmp)'
        evalstring += ','
        table_values_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(table_values_tmp)'
        evalstring += ','
        table_table_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(table_table_tmp)'
    if not (listCells is None):
        evalstring += ','
        evalstring += repr(IMSLS_LIST_CELLS)
        checkForDict(listCells, 'listCells', [])
        evalstring += ','
        listCells_nCells_tmp = c_int()
        evalstring += 'byref(listCells_nCells_tmp)'
        evalstring += ','
        listCells_listCells_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(listCells_listCells_tmp)'
        evalstring += ','
        listCells_tableUnbalanced_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(listCells_tableUnbalanced_tmp)'
    if not (n is None):
        evalstring += ','
        evalstring += repr(IMSLS_N)
        checkForDict(n, 'n', [])
        evalstring += ','
        n_nCells_tmp = c_int()
        evalstring += 'byref(n_nCells_tmp)'
        evalstring += ','
        n_n_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(n_n_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(x_tmp, inout=True, shape=(nObservations, nVariables), pyvar=x)
    if not (permutation is None):
        processRet(permutation_permutation_tmp, shape=(
            nObservations), pyvar=permutation)
    if not (table is None):
        tmp1 = 0
        for i in range(0, nKeys):
            tmp1 = tmp1 + table_nValues_tmp[i]
        tmp2 = []
        for i in range(0, nKeys):
            tmp2.append(table_nValues_tmp[i])
        tmp2 = tuple(tmp2)

        processRet(table_nValues_tmp, shape=(
            nKeys), key='nValues', pyvar=table)
        processRet(table_values_tmp, shape=(tmp1), key='values', pyvar=table)
        processRet(table_table_tmp, shape=(tmp2), key='table', pyvar=table)
    if not (listCells is None):
        processRet(listCells_nCells_tmp, shape=(
            1), key='nCells', pyvar=listCells)
        processRet(listCells_listCells_tmp, shape=(
            listCells_nCells_tmp, nKeys), key='listCells', pyvar=listCells)
        processRet(listCells_tableUnbalanced_tmp, shape=(
            listCells_nCells_tmp), key='tableUnbalanced', pyvar=listCells)
    if not (n is None):
        processRet(n_nCells_tmp, shape=(1), key='nCells', pyvar=n)
        processRet(n_n_tmp, shape=(n_nCells_tmp), key='n', pyvar=n)
    return
