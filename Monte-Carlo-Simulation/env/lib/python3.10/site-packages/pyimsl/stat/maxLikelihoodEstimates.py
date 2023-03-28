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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *

IMSLS_PRINT_LEVEL = 20530
IMSLS_N_PARAMETERS = 25260
IMSLS_NUMBER_OF_TRIALS = 50824
IMSLS_NUMBER_OF_FAILURES = 50825
IMSLS_MLOGLIKE = 50823
IMSLS_STD_ERRORS = 40120
IMSLS_HESSIAN = 25830
IMSLS_PARAM_LB = 50820
IMSLS_PARAM_UB = 50821
IMSLS_INITIAL_ESTIMATES = 12350
IMSLS_XSCALE = 15450
IMSLS_MAX_ITERATIONS = 12970
IMSLS_MAX_FCN = 12940
IMSLS_MAX_GRAD = 12950
imslstat = loadimsl(STAT)


def maxLikelihoodEstimates(x, ipdf, printLevel=None, nParameters=None, numberOfTrials=None, numberOfFailures=None, mloglike=None, stdErrors=None, hessian=None, paramLb=None, paramUb=None, initialEstimates=None, xscale=None, maxIterations=None, maxFcn=None, maxGrad=None):
    imslstat.imsls_d_max_likelihood_estimates.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_max_likelihood_estimates('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(ipdf)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (nParameters is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_PARAMETERS)
        checkForList(nParameters, 'nParameters')
        evalstring += ','
        nParameters_nParameters_tmp = c_int()
        evalstring += 'byref(nParameters_nParameters_tmp)'
    else:  # we need this ourselves for output sizes
        evalstring += ','
        evalstring += repr(IMSLS_N_PARAMETERS)
        evalstring += ','
        nParameters_nParameters_tmp = c_int()
        evalstring += 'byref(nParameters_nParameters_tmp)'
    if not (numberOfTrials is None):
        evalstring += ','
        evalstring += repr(IMSLS_NUMBER_OF_TRIALS)
        evalstring += ','
        evalstring += 'c_int(numberOfTrials)'
    if not (numberOfFailures is None):
        evalstring += ','
        evalstring += repr(IMSLS_NUMBER_OF_FAILURES)
        evalstring += ','
        evalstring += 'c_int(numberOfFailures)'
    if not (mloglike is None):
        evalstring += ','
        evalstring += repr(IMSLS_MLOGLIKE)
        checkForList(mloglike, 'mloglike')
        evalstring += ','
        mloglike_mloglike_tmp = c_double()
        evalstring += 'byref(mloglike_mloglike_tmp)'
    if not (stdErrors is None):
        evalstring += ','
        evalstring += repr(IMSLS_STD_ERRORS)
        checkForList(stdErrors, 'stdErrors')
        evalstring += ','
        stdErrors_se_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stdErrors_se_tmp)'
    if not (hessian is None):
        evalstring += ','
        evalstring += repr(IMSLS_HESSIAN)
        checkForList(hessian, 'hessian')
        evalstring += ','
        hessian_hess_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(hessian_hess_tmp)'
    if not (paramLb is None):
        evalstring += ','
        evalstring += repr(IMSLS_PARAM_LB)
        evalstring += ','
        paramLb = toNumpyArray(
            paramLb, 'paramLb', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'paramLb.ctypes.data_as(c_void_p)'
    if not (paramUb is None):
        evalstring += ','
        evalstring += repr(IMSLS_PARAM_UB)
        evalstring += ','
        paramUb = toNumpyArray(
            paramUb, 'paramUb', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'paramUb.ctypes.data_as(c_void_p)'
    if not (initialEstimates is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_ESTIMATES)
        evalstring += ','
        initialEstimates = toNumpyArray(
            initialEstimates, 'initialEstimates', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'initialEstimates.ctypes.data_as(c_void_p)'
    if not (xscale is None):
        evalstring += ','
        evalstring += repr(IMSLS_XSCALE)
        evalstring += ','
        xscale = toNumpyArray(xscale, 'xscale', shape=shape,
                              dtype='double', expectedShape=(0))
        evalstring += 'xscale.ctypes.data_as(c_void_p)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    if not (maxGrad is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_GRAD)
        evalstring += ','
        evalstring += 'c_int(maxGrad)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nParameters is None):
        processRet(nParameters_nParameters_tmp, shape=(1), pyvar=nParameters)
    if not (mloglike is None):
        processRet(mloglike_mloglike_tmp, shape=(1), pyvar=mloglike)
    if not (stdErrors is None):
        processRet(stdErrors_se_tmp, shape=(
            nParameters_nParameters_tmp), pyvar=stdErrors)
    if not (hessian is None):
        processRet(hessian_hess_tmp, shape=(
            nParameters_nParameters_tmp, nParameters_nParameters_tmp), pyvar=hessian)
    return processRet(result, shape=(nParameters_nParameters_tmp), result=True)
