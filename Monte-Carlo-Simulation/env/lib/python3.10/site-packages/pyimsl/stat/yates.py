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
from pyimsl.util.imslUtils import STAT, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, ndarray, shape
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSLS_DESIGN = 40171
IMSLS_INITIAL_ESTIMATES = 12350
IMSLS_GET_SS = 40173
IMSLS_GRAD_TOL = 12070
IMSLS_STEP_TOL = 14890
IMSLS_MAX_ITN = 12980
IMSLS_MISSING_INDEX = 40175
IMSLS_ERROR_SS = 40174
imslstat = loadimsl(STAT)


def yates(x, design=None, initialEstimates=None, getSs=None, gradTol=None, stepTol=None, maxItn=None, missingIndex=None, errorSs=None):
    """ Estimates missing observations in designed experiments using Yate's method.
    """
    imslstat.imsls_d_yates.restype = c_int
    shape = []
    evalstring = 'imslstat.imsls_d_yates('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    x_tmp = x[0]
    if (not(isinstance(x_tmp, ndarray))):
        x_tmp = toNumpyArray(x_tmp, 'x', shape=shape,
                             dtype='double', expectedShape=(0, 0))
        x[0] = x_tmp
    evalstring += 'x_tmp.ctypes.data_as(c_void_p)'
    n = len(x_tmp)
    nIndependent = len(x_tmp[0]) - 1
    if not (design is None):
        evalstring += ','
        evalstring += repr(IMSLS_DESIGN)
        evalstring += ','
        evalstring += 'c_int(design)'
    if not (initialEstimates is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_ESTIMATES)
        evalstring += ','
        evalstring += 'c_int(initialEstimates_nMissing_tmp)'
        evalstring += ','
        initialEstimates_initialEstimates_tmp = toNumpyArray(
            initialEstimates, 'initialEstimates', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'initialEstimates_initialEstimates_tmp.ctypes.data_as(c_void_p)'
        initialEstimates_nMissing_tmp = shape[0]
    if not (getSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_GET_SS)
        evalstring += ','
        checkForCallable(getSs, 'getSs')
        TMP_GETSS_GETSS = CFUNCTYPE(
            c_double, c_int, c_int, POINTER(c_int), POINTER(c_double))
        tmp_getSs_getSs = TMP_GETSS_GETSS(getSs)
        evalstring += 'tmp_getSs_getSs'
    if not (gradTol is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRAD_TOL)
        evalstring += ','
        evalstring += 'c_double(gradTol)'
    if not (stepTol is None):
        evalstring += ','
        evalstring += repr(IMSLS_STEP_TOL)
        evalstring += ','
        evalstring += 'c_double(stepTol)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (missingIndex is None):
        evalstring += ','
        evalstring += repr(IMSLS_MISSING_INDEX)
        checkForList(missingIndex, 'missingIndex')
        evalstring += ','
        missingIndex_missingIndex_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(missingIndex_missingIndex_tmp)'
    if not (errorSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_ERROR_SS)
        checkForList(errorSs, 'errorSs')
        evalstring += ','
        errorSs_errorSs_tmp = c_double()
        evalstring += 'byref(errorSs_errorSs_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (missingIndex is None):
        nMissing = result
        processRet(missingIndex_missingIndex_tmp,
                   shape=(nMissing), pyvar=missingIndex)
    if not (errorSs is None):
        processRet(errorSs_errorSs_tmp, shape=1, pyvar=errorSs)
    return result
