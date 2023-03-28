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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForCallable, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, ndarray, shape, size
from ctypes import CFUNCTYPE, POINTER, c_double, c_int, c_void_p

IMSLS_TABLE_COL_DIM = 40005
IMSLS_FCN_W_DATA = 40020
imslstat = loadimsl(STAT)


def continuousTableSetup(cdf, iopt, table, tableColDim=None, fcnWData=None):
    """ Sets up table to generate pseudorandom numbers from a general continuous distribution.
    """
    imslstat.imsls_d_continuous_table_setup.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_continuous_table_setup('
    checkForCallable(cdf, 'cdf')
    TMP_CDF = CFUNCTYPE(c_double, c_double)
    tmp_cdf = TMP_CDF(cdf)
    evalstring += 'tmp_cdf'
    evalstring += ','
    evalstring += 'c_int(iopt)'
    evalstring += ','
    evalstring += 'c_int(ndata)'
    evalstring += ','
    table_tmp = table[0]
    if (not(isinstance(table_tmp, ndarray))):
        table_tmp = toNumpyArray(
            table, 'table', shape=shape, dtype='double', expectedShape=(0, 5))
        table[0] = table_tmp
    evalstring += 'table_tmp.ctypes.data_as(c_void_p)'
    ndata = len(table_tmp)
    checkForBoolean(tableColDim, 'tableColDim')
    if (tableColDim):
        evalstring += ','
        evalstring += repr(IMSLS_TABLE_COL_DIM)
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSLS_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['cdf', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['cdf']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_double, POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    table[:] = []
    processRet(table_tmp, inout=True, shape=(ndata, 5), pyvar=table)
    return
