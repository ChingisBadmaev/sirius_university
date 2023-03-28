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
from numpy import double, dtype, int, shape, size, test
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_X_INDICES = 20443
IMSLS_PARTIAL_COV = 20691
IMSLS_PARTIAL_CORR = 20690
IMSLS_TEST = 20692
imslstat = loadimsl(STAT)


def partialCovariances(nIndependent, nDependent, x, xColDim=None, xIndices=None, partialCov=None, partialCorr=None, test=None):
    """ Computes partial covariances or partial correlations from the covariance or correlation matrix.
    """
    imslstat.imsls_d_partial_covariances.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_partial_covariances('
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    evalstring += 'c_int(nDependent)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(
        nIndependent + nDependent, nIndependent + nDependent))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (xIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INDICES)
        evalstring += ','
        xIndices = toNumpyArray(
            xIndices, 'xIndices', shape=shape, dtype='int', expectedShape=(xColDim))
        evalstring += 'xIndices.ctypes.data_as(c_void_p)'
    checkForBoolean(partialCov, 'partialCov')
    if (partialCov):
        evalstring += ','
        evalstring += repr(IMSLS_PARTIAL_COV)
    checkForBoolean(partialCorr, 'partialCorr')
    if (partialCorr):
        evalstring += ','
        evalstring += repr(IMSLS_PARTIAL_CORR)
    if not (test is None):
        evalstring += ','
        evalstring += repr(IMSLS_TEST)
        checkForDict(test, 'test', ['df'])
        evalstring += ','
        test_df_tmp = test['df']
        evalstring += 'c_int(test_df_tmp)'
        evalstring += ','
        test_dfOut_tmp = c_int()
        evalstring += 'byref(test_dfOut_tmp)'
        evalstring += ','
        test_pValues_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(test_pValues_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (test is None):
        processRet(test_dfOut_tmp, shape=(1), key='dfOut', pyvar=test)
        processRet(test_pValues_tmp, shape=(
            nDependent, nDependent), key='pValues', pyvar=test)
    return processRet(result, shape=(nDependent, nDependent), result=True)
