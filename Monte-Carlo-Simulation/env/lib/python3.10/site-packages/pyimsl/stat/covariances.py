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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_MISSING_VALUE_METHOD = 16078
IMSLS_INCIDENCE_MATRIX = 16081
IMSLS_N_OBSERVATIONS = 15640
IMSLS_VARIANCE_COVARIANCE_MATRIX = 15330
IMSLS_CORRECTED_SSCP_MATRIX = 11020
IMSLS_CORRELATION_MATRIX = 11030
IMSLS_STDEV_CORRELATION_MATRIX = 14820
IMSLS_MEANS = 13120
IMSLS_COVARIANCE_COL_DIM = 11050
IMSLS_FREQUENCIES = 11790
IMSLS_WEIGHTS = 15400
IMSLS_SUM_WEIGHTS = 20800
IMSLS_N_ROWS_MISSING = 20400
imslstat = loadimsl(STAT)


def covariances(x, xColDim=None, missingValueMethod=None, incidenceMatrix=None, nObservations=None, varianceCovarianceMatrix=None, correctedSscpMatrix=None, correlationMatrix=None, stdevCorrelationMatrix=None, means=None, covarianceColDim=None, frequencies=None, weights=None, sumWeights=None, nRowsMissing=None):
    """ Computes the sample variance-covariance or correlation matrix.
    """
    imslstat.imsls_d_covariances.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_covariances('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nVariables = shape[1]
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (missingValueMethod is None):
        evalstring += ','
        evalstring += repr(IMSLS_MISSING_VALUE_METHOD)
        evalstring += ','
        evalstring += 'c_int(missingValueMethod)'
    if not (incidenceMatrix is None):
        evalstring += ','
        evalstring += repr(IMSLS_INCIDENCE_MATRIX)
        checkForList(incidenceMatrix, 'incidenceMatrix')
        evalstring += ','
        incidenceMatrix_incidenceMatrix_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(incidenceMatrix_incidenceMatrix_tmp)'
    if not (nObservations is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_OBSERVATIONS)
        checkForList(nObservations, 'nObservations')
        evalstring += ','
        nObservations_nObservations_tmp = c_int()
        evalstring += 'byref(nObservations_nObservations_tmp)'
    checkForBoolean(varianceCovarianceMatrix, 'varianceCovarianceMatrix')
    if (varianceCovarianceMatrix):
        evalstring += ','
        evalstring += repr(IMSLS_VARIANCE_COVARIANCE_MATRIX)
    checkForBoolean(correctedSscpMatrix, 'correctedSscpMatrix')
    if (correctedSscpMatrix):
        evalstring += ','
        evalstring += repr(IMSLS_CORRECTED_SSCP_MATRIX)
    checkForBoolean(correlationMatrix, 'correlationMatrix')
    if (correlationMatrix):
        evalstring += ','
        evalstring += repr(IMSLS_CORRELATION_MATRIX)
    checkForBoolean(stdevCorrelationMatrix, 'stdevCorrelationMatrix')
    if (stdevCorrelationMatrix):
        evalstring += ','
        evalstring += repr(IMSLS_STDEV_CORRELATION_MATRIX)
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEANS)
        checkForList(means, 'means')
        evalstring += ','
        means_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(means_means_tmp)'
    if not (covarianceColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_COVARIANCE_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(covarianceColDim)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(frequencies, 'frequencies', shape=shape,
                                   dtype='double', expectedShape=(nObservations_nObservations_tmp))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(weights, 'weights', shape=shape, dtype='double', expectedShape=(
            nObservations_nObservations_tmp))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (sumWeights is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUM_WEIGHTS)
        checkForList(sumWeights, 'sumWeights')
        evalstring += ','
        sumWeights_sumwt_tmp = c_double()
        evalstring += 'byref(sumWeights_sumwt_tmp)'
    if not (nRowsMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ROWS_MISSING)
        checkForList(nRowsMissing, 'nRowsMissing')
        evalstring += ','
        nRowsMissing_nrmiss_tmp = c_int()
        evalstring += 'byref(nRowsMissing_nrmiss_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (incidenceMatrix is None):
        processRet(incidenceMatrix_incidenceMatrix_tmp, shape=(
            nVariables, nVariables), pyvar=incidenceMatrix)
    if not (nObservations is None):
        processRet(nObservations_nObservations_tmp,
                   shape=1, pyvar=nObservations)
    if not (means is None):
        processRet(means_means_tmp, shape=(nVariables), pyvar=means)
    if not (sumWeights is None):
        processRet(sumWeights_sumwt_tmp, shape=1, pyvar=sumWeights)
    if not (nRowsMissing is None):
        processRet(nRowsMissing_nrmiss_tmp, shape=1, pyvar=nRowsMissing)
    return processRet(result, shape=(nVariables, nVariables), result=True)
