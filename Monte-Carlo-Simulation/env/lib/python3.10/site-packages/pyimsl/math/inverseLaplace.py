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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, checkForDict, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import d_complex
from pyimsl.util.Translator import Translator

IMSL_PSEUDO_ACCURACY = 11124
IMSL_FIRST_LAGUERRE_PARAMETER = 11125
IMSL_SECOND_LAGUERRE_PARAMETER = 11126
IMSL_MAXIMUM_COEFFICIENTS = 11127
IMSL_ERROR_EST = 11128
IMSL_DISCRETIZATION_ERROR_EST = 11129
IMSL_TRUNCATION_ERROR_EST = 11130
IMSL_CONDITION_ERROR_EST = 11131
IMSL_DECAY_FUNCTION_COEFFICIENT = 11132
IMSL_DECAY_FUNCTION_BASE = 11133
IMSL_LOG_LARGEST_COEFFICIENTS = 11134
IMSL_LOG_SMALLEST_COEFFICIENTS = 11135
IMSL_UNDER_OVERFLOW_INDICATORS = 11136
IMSL_FCN_W_DATA = 13101

# Constants for underOverflowIndicators
NORMAL_TERMINATION = 0
TOO_LARGE = 1
TOO_SMALL = 2
TOO_LARGE_BEFORE_EXPANSION = 3
TOO_SMALL_BEFORE_EXPANSION = 4

imslmath = loadimsl(MATH)


def inverseLaplace(fcn, sigma0, t, pseudoAccuracy=None, firstLaguerreParameter=None, secondLaguerreParameter=None, maximumCoefficients=None, errorEst=None, discretizationErrorEst=None, truncationErrorEst=None, conditionErrorEst=None, decayFunctionCoefficient=None, decayFunctionBase=None, logLargestCoefficients=None, logSmallestCoefficients=None, underOverflowIndicators=None, fcnWData=None):
    """ Computes the inverse Laplace transform of a complex function.
    """
    # inverseLaplace is not implemented because it requires
    # a structure (d_complex) to be passed to a user function,
    # which is not supported by ctypes.
    #
    errStr = Translator.getString("ilnotimplemented")
    raise NotImplementedError(errStr)
#
    imslmath.imsl_d_inverse_laplace.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_inverse_laplace('
    checkForCallable(fcn, 'fcn')
#    TMP_FCN=CFUNCTYPE(c_void_p,c_void_p)
    TMP_FCN = CFUNCTYPE(c_void_p, d_complex)
#    TMP_FCN=CFUNCTYPE(d_complex,d_complex)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_double(sigma0)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    t = toNumpyArray(t, 't', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 't.ctypes.data_as(c_void_p)'
    n = shape[0]
    if not (pseudoAccuracy is None):
        evalstring += ','
        evalstring += repr(IMSL_PSEUDO_ACCURACY)
        evalstring += ','
        evalstring += 'c_double(pseudoAccuracy)'
    if not (firstLaguerreParameter is None):
        evalstring += ','
        evalstring += repr(IMSL_FIRST_LAGUERRE_PARAMETER)
        evalstring += ','
        evalstring += 'c_double(firstLaguerreParameter)'
    if not (secondLaguerreParameter is None):
        evalstring += ','
        evalstring += repr(IMSL_SECOND_LAGUERRE_PARAMETER)
        evalstring += ','
        evalstring += 'c_double(secondLaguerreParameter)'
    if not (maximumCoefficients is None):
        evalstring += ','
        evalstring += repr(IMSL_MAXIMUM_COEFFICIENTS)
        evalstring += ','
        evalstring += 'c_int(maximumCoefficients)'
    if not (errorEst is None):
        evalstring += ','
        evalstring += repr(IMSL_ERROR_EST)
        checkForList(errorEst, 'errorEst')
        evalstring += ','
        errorEst_errorEst_tmp = c_double()
        evalstring += 'byref(errorEst_errorEst_tmp)'
    if not (discretizationErrorEst is None):
        evalstring += ','
        evalstring += repr(IMSL_DISCRETIZATION_ERROR_EST)
        checkForList(discretizationErrorEst, 'discretizationErrorEst')
        evalstring += ','
        discretizationErrorEst_discErrorEst_tmp = c_double()
        evalstring += 'byref(discretizationErrorEst_discErrorEst_tmp)'
    if not (truncationErrorEst is None):
        evalstring += ','
        evalstring += repr(IMSL_TRUNCATION_ERROR_EST)
        checkForList(truncationErrorEst, 'truncationErrorEst')
        evalstring += ','
        truncationErrorEst_truncErrorEst_tmp = c_double()
        evalstring += 'byref(truncationErrorEst_truncErrorEst_tmp)'
    if not (conditionErrorEst is None):
        evalstring += ','
        evalstring += repr(IMSL_CONDITION_ERROR_EST)
        checkForList(conditionErrorEst, 'conditionErrorEst')
        evalstring += ','
        conditionErrorEst_condErrorEst_tmp = c_double()
        evalstring += 'byref(conditionErrorEst_condErrorEst_tmp)'
    if not (decayFunctionCoefficient is None):
        evalstring += ','
        evalstring += repr(IMSL_DECAY_FUNCTION_COEFFICIENT)
        checkForList(decayFunctionCoefficient, 'decayFunctionCoefficient')
        evalstring += ','
        decayFunctionCoefficient_k_tmp = c_double()
        evalstring += 'byref(decayFunctionCoefficient_k_tmp)'
    if not (decayFunctionBase is None):
        evalstring += ','
        evalstring += repr(IMSL_DECAY_FUNCTION_BASE)
        checkForList(decayFunctionBase, 'decayFunctionBase')
        evalstring += ','
        decayFunctionBase_r_tmp = c_double()
        evalstring += 'byref(decayFunctionBase_r_tmp)'
    if not (logLargestCoefficients is None):
        evalstring += ','
        evalstring += repr(IMSL_LOG_LARGEST_COEFFICIENTS)
        checkForList(logLargestCoefficients, 'logLargestCoefficients')
        evalstring += ','
        logLargestCoefficients_logLargestCoefs_tmp = c_double()
        evalstring += 'byref(logLargestCoefficients_logLargestCoefs_tmp)'
    if not (logSmallestCoefficients is None):
        evalstring += ','
        evalstring += repr(IMSL_LOG_SMALLEST_COEFFICIENTS)
        checkForList(logSmallestCoefficients, 'logSmallestCoefficients')
        evalstring += ','
        logSmallestCoefficients_logSmallestCoefs_tmp = c_double()
        evalstring += 'byref(logSmallestCoefficients_logSmallestCoefs_tmp)'
    if not (underOverflowIndicators is None):
        evalstring += ','
        evalstring += repr(IMSL_UNDER_OVERFLOW_INDICATORS)
        checkForList(underOverflowIndicators, 'underOverflowIndicators')
        evalstring += ','
        underOverflowIndicators_indicators_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(underOverflowIndicators_indicators_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcn', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcn']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(
            d_complex, d_complex, POINTER(c_double))
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
    fatalErrorCheck(MATH)
    if not (errorEst is None):
        processRet(errorEst_errorEst_tmp, shape=1, pyvar=errorEst)
    if not (discretizationErrorEst is None):
        processRet(discretizationErrorEst_discErrorEst_tmp,
                   shape=1, pyvar=discretizationErrorEst)
    if not (truncationErrorEst is None):
        processRet(truncationErrorEst_truncErrorEst_tmp,
                   shape=1, pyvar=truncationErrorEst)
    if not (conditionErrorEst is None):
        processRet(conditionErrorEst_condErrorEst_tmp,
                   shape=1, pyvar=conditionErrorEst)
    if not (decayFunctionCoefficient is None):
        processRet(decayFunctionCoefficient_k_tmp,
                   shape=1, pyvar=decayFunctionCoefficient)
    if not (decayFunctionBase is None):
        processRet(decayFunctionBase_r_tmp, shape=1, pyvar=decayFunctionBase)
    if not (logLargestCoefficients is None):
        processRet(logLargestCoefficients_logLargestCoefs_tmp,
                   shape=1, pyvar=logLargestCoefficients)
    if not (logSmallestCoefficients is None):
        processRet(logSmallestCoefficients_logSmallestCoefs_tmp,
                   shape=1, pyvar=logSmallestCoefficients)
    if not (underOverflowIndicators is None):
        processRet(underOverflowIndicators_indicators_tmp,
                   shape=(n), pyvar=underOverflowIndicators)
    return processRet(result, shape=(n), result=True)
