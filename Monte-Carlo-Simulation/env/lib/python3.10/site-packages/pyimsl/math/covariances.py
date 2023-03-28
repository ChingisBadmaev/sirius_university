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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_X_COL_DIM = 10045
IMSL_VARIANCE_COVARIANCE_MATRIX = 10219
IMSL_CORRECTED_SSCP_MATRIX = 10220
IMSL_CORRELATION_MATRIX = 10221
IMSL_STDEV_CORRELATION_MATRIX = 10222
IMSL_MEANS = 10090
IMSL_COVARIANCE_COL_DIM = 10092
imslmath = loadimsl(MATH)


def covariances(x, xColDim=None, varianceCovarianceMatrix=None, correctedSscpMatrix=None, correlationMatrix=None, stdevCorrelationMatrix=None, means=None, covarianceColDim=None):
    """ Computes the sample variance-covariance or correlation matrix.
    """
    imslmath.imsl_d_covariances.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_covariances('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nVariables = shape[1]
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    checkForBoolean(varianceCovarianceMatrix, 'varianceCovarianceMatrix')
    if (varianceCovarianceMatrix):
        evalstring += ','
        evalstring += repr(IMSL_VARIANCE_COVARIANCE_MATRIX)
    checkForBoolean(correctedSscpMatrix, 'correctedSscpMatrix')
    if (correctedSscpMatrix):
        evalstring += ','
        evalstring += repr(IMSL_CORRECTED_SSCP_MATRIX)
    checkForBoolean(correlationMatrix, 'correlationMatrix')
    if (correlationMatrix):
        evalstring += ','
        evalstring += repr(IMSL_CORRELATION_MATRIX)
    checkForBoolean(stdevCorrelationMatrix, 'stdevCorrelationMatrix')
    if (stdevCorrelationMatrix):
        evalstring += ','
        evalstring += repr(IMSL_STDEV_CORRELATION_MATRIX)
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSL_MEANS)
        checkForList(means, 'means')
        evalstring += ','
        means_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(means_means_tmp)'
    if not (covarianceColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_COVARIANCE_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(covarianceColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (means is None):
        processRet(means_means_tmp, shape=(nVariables), pyvar=means)
    return processRet(result, shape=(nVariables, nVariables), result=True)
