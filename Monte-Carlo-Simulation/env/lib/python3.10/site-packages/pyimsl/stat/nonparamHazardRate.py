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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, checkForDict, processRet, toNumpyArray
from numpy import double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_PRINT_LEVEL = 20530
IMSLS_CENSOR_CODES = 40400
IMSLS_WEIGHT = 15390
IMSLS_SORT_OPTION = 40401
IMSLS_K_GRID = 40408
IMSLS_BETA_GRID = 40402
IMSLS_N_MISSING = 13440
IMSLS_ALPHA = 10070
IMSLS_BETA = 20870
IMSLS_CRITERION = 20290
IMSLS_K = 40403
IMSLS_SORTED_EVENT_TIMES = 40404
IMSLS_SORTED_CENSOR_CODES = 40406
imslstat = loadimsl(STAT)


def nonparamHazardRate(t, nHazard, hazardMin, hazardIncrement, printLevel=None, censorCodes=None, weight=None, sortOption=None, kGrid=None, betaGrid=None, nMissing=None, alpha=None, beta=None, criterion=None, k=None, sortedEventTimes=None, sortedCensorCodes=None):
    """ Performs nonparametric hazard rate estimation using kernel functions and quasi-likelihoods.
    """
    imslstat.imsls_d_nonparam_hazard_rate.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_nonparam_hazard_rate('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    t = toNumpyArray(t, 't', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 't.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(nHazard)'
    evalstring += ','
    evalstring += 'c_double(hazardMin)'
    evalstring += ','
    evalstring += 'c_double(hazardIncrement)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (censorCodes is None):
        evalstring += ','
        evalstring += repr(IMSLS_CENSOR_CODES)
        evalstring += ','
        censorCodes = toNumpyArray(
            censorCodes, 'censorCodes', shape=shape, dtype='int', expectedShape=(nObservations))
        evalstring += 'censorCodes.ctypes.data_as(c_void_p)'
    if not (weight is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHT)
        evalstring += ','
        evalstring += 'c_int(weight)'
    if not (sortOption is None):
        evalstring += ','
        evalstring += repr(IMSLS_SORT_OPTION)
        evalstring += ','
        evalstring += 'c_int(sortOption)'
    if not (kGrid is None):
        evalstring += ','
        evalstring += repr(IMSLS_K_GRID)
        checkForDict(kGrid, 'kGrid', ['nK', 'kMin', 'kIncrement'])
        evalstring += ','
        kGrid_nK_tmp = kGrid['nK']
        evalstring += 'c_int(kGrid_nK_tmp)'
        evalstring += ','
        kGrid_kMin_tmp = kGrid['kMin']
        evalstring += 'c_int(kGrid_kMin_tmp)'
        evalstring += ','
        kGrid_kIncrement_tmp = kGrid['kIncrement']
        evalstring += 'c_int(kGrid_kIncrement_tmp)'
    if not (betaGrid is None):
        evalstring += ','
        evalstring += repr(IMSLS_BETA_GRID)
        checkForDict(betaGrid, 'betaGrid', [
                     'nBetaGrid', 'betaStart', 'betaIncrement'])
        evalstring += ','
        betaGrid_nBetaGrid_tmp = betaGrid['nBetaGrid']
        evalstring += 'c_int(betaGrid_nBetaGrid_tmp)'
        evalstring += ','
        betaGrid_betaStart_tmp = betaGrid['betaStart']
        evalstring += 'c_double(betaGrid_betaStart_tmp)'
        evalstring += ','
        betaGrid_betaIncrement_tmp = betaGrid['betaIncrement']
        evalstring += 'c_double(betaGrid_betaIncrement_tmp)'
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nmiss_tmp = c_int()
        evalstring += 'byref(nMissing_nmiss_tmp)'
    if not (alpha is None):
        evalstring += ','
        evalstring += repr(IMSLS_ALPHA)
        checkForList(alpha, 'alpha')
        evalstring += ','
        alpha_alpha_tmp = c_double()
        evalstring += 'byref(alpha_alpha_tmp)'
    if not (beta is None):
        evalstring += ','
        evalstring += repr(IMSLS_BETA)
        checkForList(beta, 'beta')
        evalstring += ','
        beta_beta_tmp = c_double()
        evalstring += 'byref(beta_beta_tmp)'
    if not (criterion is None):
        evalstring += ','
        evalstring += repr(IMSLS_CRITERION)
        checkForList(criterion, 'criterion')
        evalstring += ','
        criterion_vml_tmp = c_double()
        evalstring += 'byref(criterion_vml_tmp)'
    if not (k is None):
        evalstring += ','
        evalstring += repr(IMSLS_K)
        checkForList(k, 'k')
        evalstring += ','
        k_k_tmp = c_int()
        evalstring += 'byref(k_k_tmp)'
    if not (sortedEventTimes is None):
        evalstring += ','
        evalstring += repr(IMSLS_SORTED_EVENT_TIMES)
        checkForList(sortedEventTimes, 'sortedEventTimes')
        evalstring += ','
        sortedEventTimes_eventTimes_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(sortedEventTimes_eventTimes_tmp)'
    if not (sortedCensorCodes is None):
        evalstring += ','
        evalstring += repr(IMSLS_SORTED_CENSOR_CODES)
        checkForList(sortedCensorCodes, 'sortedCensorCodes')
        evalstring += ','
        sortedCensorCodes_isortedCensor_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(sortedCensorCodes_isortedCensor_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nMissing is None):
        processRet(nMissing_nmiss_tmp, shape=1, pyvar=nMissing)
    if not (alpha is None):
        processRet(alpha_alpha_tmp, shape=1, pyvar=alpha)
    if not (beta is None):
        processRet(beta_beta_tmp, shape=1, pyvar=beta)
    if not (criterion is None):
        processRet(criterion_vml_tmp, shape=1, pyvar=criterion)
    if not (k is None):
        processRet(k_k_tmp, shape=1, pyvar=k)
    if not (sortedEventTimes is None):
        processRet(sortedEventTimes_eventTimes_tmp, shape=(
            nObservations), pyvar=sortedEventTimes)
    if not (sortedCensorCodes is None):
        processRet(sortedCensorCodes_isortedCensor_tmp,
                   shape=(nObservations), pyvar=sortedCensorCodes)
    return processRet(result, shape=(nHazard), result=True)
