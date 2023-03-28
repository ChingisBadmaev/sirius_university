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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_COVARIANCE_MATRIX = 15820
IMSLS_CORRELATION_MATRIX = 11030
IMSLS_CUM_PERCENT = 11080
IMSLS_EIGENVECTORS = 11320
IMSLS_CORRELATIONS = 10810
IMSLS_STD_DEV = 14830
IMSLS_COV_COL_DIM = 11055
imslstat = loadimsl(STAT)


def principalComponents(covariances, covarianceMatrix=None, correlationMatrix=None, cumPercent=None, eigenvectors=None, correlations=None, stdDev=None, covColDim=None):
    """ Computes principal components.
    """
    imslstat.imsls_d_principal_components.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_principal_components('
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    covariances = toNumpyArray(
        covariances, 'covariances', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'covariances.ctypes.data_as(c_void_p)'
    nVariables = shape[0]
    checkForBoolean(covarianceMatrix, 'covarianceMatrix')
    if (covarianceMatrix):
        evalstring += ','
        evalstring += repr(IMSLS_COVARIANCE_MATRIX)
    checkForBoolean(correlationMatrix, 'correlationMatrix')
    if (correlationMatrix):
        evalstring += ','
        evalstring += repr(IMSLS_CORRELATION_MATRIX)
    if not (cumPercent is None):
        evalstring += ','
        evalstring += repr(IMSLS_CUM_PERCENT)
        checkForList(cumPercent, 'cumPercent')
        evalstring += ','
        cumPercent_cumPercent_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cumPercent_cumPercent_tmp)'
    if not (eigenvectors is None):
        evalstring += ','
        evalstring += repr(IMSLS_EIGENVECTORS)
        checkForList(eigenvectors, 'eigenvectors')
        evalstring += ','
        eigenvectors_eigenvectors_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(eigenvectors_eigenvectors_tmp)'
    if not (correlations is None):
        evalstring += ','
        evalstring += repr(IMSLS_CORRELATIONS)
        checkForList(correlations, 'correlations')
        evalstring += ','
        correlations_correlations_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(correlations_correlations_tmp)'
    if not (stdDev is None):
        evalstring += ','
        evalstring += repr(IMSLS_STD_DEV)
        checkForDict(stdDev, 'stdDev', ['nDegreesFreedom'])
        evalstring += ','
        stdDev_nDegreesFreedom_tmp = stdDev['nDegreesFreedom']
        evalstring += 'c_int(stdDev_nDegreesFreedom_tmp)'
        evalstring += ','
        stdDev_stdDev_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stdDev_stdDev_tmp)'
    if not (covColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(covColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (cumPercent is None):
        processRet(cumPercent_cumPercent_tmp,
                   shape=(nVariables), pyvar=cumPercent)
    if not (eigenvectors is None):
        processRet(eigenvectors_eigenvectors_tmp, shape=(
            nVariables, nVariables), pyvar=eigenvectors)
    if not (correlations is None):
        processRet(correlations_correlations_tmp, shape=(
            nVariables, nVariables), pyvar=correlations)
    if not (stdDev is None):
        processRet(stdDev_stdDev_tmp, key='stdDev',
                   shape=(nVariables), pyvar=stdDev)
    return processRet(result, shape=(nVariables), result=True)
