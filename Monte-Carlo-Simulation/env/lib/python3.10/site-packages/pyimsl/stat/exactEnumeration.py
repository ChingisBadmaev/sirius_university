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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import byref, c_double, c_int, c_void_p

IMSLS_PROB_TABLE = 20610
IMSLS_P_VALUE = 20620
IMSLS_CHECK_NUMERICAL_ERROR = 20630
imslstat = loadimsl(STAT)


def exactEnumeration(table, probTable=None, pValue=None, checkNumericalError=None):
    """ Computes exact probabilities in a two-way contingency table using the total enumeration method.
    """
    imslstat.imsls_d_exact_enumeration.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_exact_enumeration('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nColumns)'
    evalstring += ','
    table = toNumpyArray(table, 'table', shape=shape,
                         dtype='double', expectedShape=(0, 0))
    evalstring += 'table.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nColumns = shape[1]
    if not (probTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_PROB_TABLE)
        checkForList(probTable, 'probTable')
        evalstring += ','
        probTable_prt_tmp = c_double()
        evalstring += 'byref(probTable_prt_tmp)'
    if not (pValue is None):
        evalstring += ','
        evalstring += repr(IMSLS_P_VALUE)
        checkForList(pValue, 'pValue')
        evalstring += ','
        pValue_pValue_tmp = c_double()
        evalstring += 'byref(pValue_pValue_tmp)'
    if not (checkNumericalError is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHECK_NUMERICAL_ERROR)
        checkForList(checkNumericalError, 'checkNumericalError')
        evalstring += ','
        checkNumericalError_check_tmp = c_double()
        evalstring += 'byref(checkNumericalError_check_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (probTable is None):
        processRet(probTable_prt_tmp, shape=1, pyvar=probTable)
    if not (pValue is None):
        processRet(pValue_pValue_tmp, shape=1, pyvar=pValue)
    if not (checkNumericalError is None):
        processRet(checkNumericalError_check_tmp,
                   shape=1, pyvar=checkNumericalError)
    return result
