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
from pyimsl.util.imslUtils import STAT, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape, sum
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_PRINT_LEVEL = 20530
IMSLS_MAX_ITERATIONS = 12970
IMSLS_CONVERGENCE_EPS = 10980
IMSLS_RATIO = 40032
IMSLS_X_RESPONSE_COL = 40410
IMSLS_CENSOR_CODES_COL = 40409
IMSLS_STRATIFICATION_COL = 40034
IMSLS_CONSTANT_COL = 40413
IMSLS_FREQ_RESPONSE_COL = 40411
IMSLS_TIES_OPTION = 15020
IMSLS_MAXIMUM_LIKELIHOOD = 12900
IMSLS_N_MISSING = 13440
IMSLS_STATISTICS = 14780
IMSLS_X_MEAN = 15490
IMSLS_VARIANCE_COVARIANCE_MATRIX = 15330
IMSLS_INITIAL_EST_INPUT = 20210
IMSLS_UPDATE = 25920
IMSLS_DUMMY = 11270
IMSLS_STRATUM_NUMBER = 40038
IMSLS_CLASS_VARIABLES = 40040
imslstat = loadimsl(STAT)


def propHazardsGenLin(x, nVarEffects, indicesEffects, maxClass, ncoef, printLevel=None,
                      maxIterations=None, convergenceEps=None, ratio=None, xResponseCol=None, censorCodesCol=None,
                      stratificationCol=None, constantCol=None, freqResponseCol=None, tiesOption=None,
                      maximumLikelihood=None, nMissing=None, statistics=None, xMean=None, varianceCovarianceMatrix=None,
                      initialEstInput=None, update=None, dummy=None, stratumNumber=None, classVariables=None):
    """ Analyzes survival and reliability data using Cox's proportional hazards model.
    """
    imslstat.imsls_d_prop_hazards_gen_lin.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_prop_hazards_gen_lin('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nColumns)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nColumns = shape[1]
    evalstring += ','
    evalstring += 'c_int(nef)'
    evalstring += ','
    nVarEffects = toNumpyArray(
        nVarEffects, 'nVarEffects', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'nVarEffects.ctypes.data_as(c_void_p)'
    nef = shape[0]
    evalstring += ','
    indicesEffects = toNumpyArray(
        indicesEffects, 'indicesEffects', shape=shape, dtype='int', expectedShape=sum(nVarEffects))
    evalstring += 'indicesEffects.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(maxClass)'
    evalstring += ','
    checkForList(ncoef, 'ncoef')
    ncoef_tmp = c_int()
    evalstring += 'byref(ncoef_tmp)'
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
    if not (convergenceEps is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONVERGENCE_EPS)
        evalstring += ','
        evalstring += 'c_double(convergenceEps)'
    if not (ratio is None):
        evalstring += ','
        evalstring += repr(IMSLS_RATIO)
        evalstring += ','
        evalstring += 'c_double(ratio)'
    if not (xResponseCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_RESPONSE_COL)
        evalstring += ','
        evalstring += 'c_int(xResponseCol)'
    if not (censorCodesCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_CENSOR_CODES_COL)
        evalstring += ','
        evalstring += 'c_int(censorCodesCol)'
    if not (stratificationCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRATIFICATION_COL)
        evalstring += ','
        evalstring += 'c_int(stratificationCol)'
    if not (constantCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONSTANT_COL)
        evalstring += ','
        evalstring += 'c_int(constantCol)'
    if not (freqResponseCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQ_RESPONSE_COL)
        evalstring += ','
        evalstring += 'c_int(freqResponseCol)'
    if not (tiesOption is None):
        evalstring += ','
        evalstring += repr(IMSLS_TIES_OPTION)
        evalstring += ','
        evalstring += 'c_int(tiesOption)'
    if not (maximumLikelihood is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAXIMUM_LIKELIHOOD)
        checkForList(maximumLikelihood, 'maximumLikelihood')
        evalstring += ','
        maximumLikelihood_algl_tmp = c_double()
        evalstring += 'byref(maximumLikelihood_algl_tmp)'
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nrmiss_tmp = c_int()
        evalstring += 'byref(nMissing_nrmiss_tmp)'
    if not (statistics is None):
        evalstring += ','
        evalstring += repr(IMSLS_STATISTICS)
        checkForList(statistics, 'statistics')
        evalstring += ','
        statistics_case_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(statistics_case_tmp)'
    if not (xMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_MEAN)
        checkForList(xMean, 'xMean')
        evalstring += ','
        xMean_xmean_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xMean_xmean_tmp)'
    if not (varianceCovarianceMatrix is None):
        evalstring += ','
        evalstring += repr(IMSLS_VARIANCE_COVARIANCE_MATRIX)
        checkForList(varianceCovarianceMatrix, 'varianceCovarianceMatrix')
        evalstring += ','
        varianceCovarianceMatrix_cov_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(varianceCovarianceMatrix_cov_tmp)'
    if not (initialEstInput is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_EST_INPUT)
        evalstring += ','
        initialEstInput = toNumpyArray(
            initialEstInput, 'initialEstInput', shape=shape, dtype='double')
        evalstring += 'inCoef.ctypes.data_as(c_void_p)'
    if not (update is None):
        evalstring += ','
        evalstring += repr(IMSLS_UPDATE)
        checkForList(update, 'update')
        evalstring += ','
        update_gr_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(update_gr_tmp)'
    if not (dummy is None):
        evalstring += ','
        evalstring += repr(IMSLS_DUMMY)
        evalstring += ','
        evalstring += 'c_int(dummy_nClassVar_tmp)'
        evalstring += ','
        dummy_indexClassVar_tmp = toNumpyArray(
            dummy, 'dummy', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'dummy_indexClassVar_tmp.ctypes.data_as(c_void_p)'
        dummy_nClassVar_tmp = shape[0]
    if not (stratumNumber is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRATUM_NUMBER)
        checkForList(stratumNumber, 'stratumNumber')
        evalstring += ','
        stratumNumber_igrp_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(stratumNumber_igrp_tmp)'
    if not (classVariables is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_VARIABLES)
        checkForDict(classVariables, 'classVariables', [])
        evalstring += ','
        classVariables_nClassValues_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(classVariables_nClassValues_tmp)'
        evalstring += ','
        classVariables_classValues_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(classVariables_classValues_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(ncoef_tmp, shape=1, pyvar=ncoef)
    ncoef_tmp = ncoef[0]
    if not (maximumLikelihood is None):
        processRet(maximumLikelihood_algl_tmp,
                   shape=1, pyvar=maximumLikelihood)
    if not (nMissing is None):
        processRet(nMissing_nrmiss_tmp, shape=1, pyvar=nMissing)
    if not (statistics is None):
        processRet(statistics_case_tmp, shape=(
            nObservations, 5), pyvar=statistics)
    if not (xMean is None):
        processRet(xMean_xmean_tmp, shape=(ncoef_tmp), pyvar=xMean)
    if not (varianceCovarianceMatrix is None):
        processRet(varianceCovarianceMatrix_cov_tmp, shape=(
            ncoef_tmp, ncoef_tmp), pyvar=varianceCovarianceMatrix)
    if not (update is None):
        processRet(update_gr_tmp, shape=(ncoef_tmp), pyvar=update)
    if not (stratumNumber is None):
        processRet(stratumNumber_igrp_tmp, shape=(
            nObservations), pyvar=stratumNumber)
    if not (classVariables is None):
        classValuesSum = 0
        for i in range(0, dummy_nClassVar_tmp):
            classValuesSum += classVariables_nClassValues_tmp[i]
        processRet(classVariables_nClassValues_tmp, shape=(
            dummy_nClassVar_tmp), key='nclassValues', pyvar=classVariables)
        processRet(classVariables_classValues_tmp, shape=(
            classValuesSum), key='classValues', pyvar=classVariables)
    return processRet(result, shape=(ncoef_tmp * 4), result=True)
