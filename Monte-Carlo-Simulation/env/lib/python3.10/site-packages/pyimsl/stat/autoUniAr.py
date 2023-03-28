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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_PRINT_LEVEL = 20530
IMSLS_MAX_ITERATIONS = 12970
IMSLS_METHOD = 13170
IMSLS_VAR_NOISE = 25020
IMSLS_AIC = 30042
IMSLS_MEAN_ESTIMATE = 16051
imslstat = loadimsl(STAT)


def autoUniAr(z, maxlag, p, printLevel=None, maxIterations=None, method=None, varNoise=None, aic=None, meanEstimate=None):
    """ Automatic selection and fitting of a univariate autoregressive time series model.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_auto_uni_ar.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_auto_uni_ar('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    z = toNumpyArray(z, 'z', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'z.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    evalstring += 'c_int(maxlag)'
    evalstring += ','
    p_tmp = c_int()
    evalstring += 'byref(p_tmp)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (varNoise is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_NOISE)
        checkForList(varNoise, 'varNoise')
        evalstring += ','
        varNoise_varNoise_tmp = c_double()
        evalstring += 'byref(varNoise_varNoise_tmp)'
    if not (aic is None):
        evalstring += ','
        evalstring += repr(IMSLS_AIC)
        checkForList(aic, 'aic')
        evalstring += ','
        aic_aic_tmp = c_double()
        evalstring += 'byref(aic_aic_tmp)'
    if not (meanEstimate is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEAN_ESTIMATE)
        checkForList(meanEstimate, 'meanEstimate')
        evalstring += ','
        meanEstimate_meanEstimate_tmp = meanEstimate[0]
        if (not(isinstance(meanEstimate_meanEstimate_tmp, c_double))):
            meanEstimate_meanEstimate_tmp = c_double(meanEstimate[0])
        evalstring += 'byref(meanEstimate_meanEstimate_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(p_tmp, shape=1, pyvar=p)
    if not (varNoise is None):
        processRet(varNoise_varNoise_tmp, shape=1, pyvar=varNoise)
    if not (aic is None):
        processRet(aic_aic_tmp, shape=1, pyvar=aic)
    if not (meanEstimate is None):
        processRet(meanEstimate_meanEstimate_tmp, shape=1, pyvar=meanEstimate)
    return processRet(result, shape=(1 + maxlag), result=True)
