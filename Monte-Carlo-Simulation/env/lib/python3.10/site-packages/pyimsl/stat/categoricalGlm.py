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
from numpy import array, cov, double, dtype, insert, int, shape, size, sum
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_X_COL_FREQUENCIES = 20130
IMSLS_X_COL_FIXED_PARAMETER = 20120
IMSLS_X_COL_DIST_PARAMETER = 20150
IMSLS_X_COL_VARIABLES = 20683
IMSLS_EPS = 11370
IMSLS_TOLERANCE = 15040
IMSLS_MAX_ITERATIONS = 12970
IMSLS_INTERCEPT = 12400
IMSLS_NO_INTERCEPT = 13350
IMSLS_EFFECTS = 20200
IMSLS_INITIAL_EST_INTERNAL = 20220
IMSLS_INITIAL_EST_INPUT = 20210
IMSLS_MAX_CLASS = 20230
IMSLS_CLASS_INFO = 20250
IMSLS_COEF_STAT = 20270
IMSLS_CRITERION = 20290
IMSLS_COV = 20310
IMSLS_MEANS = 13120
IMSLS_CASE_ANALYSIS = 20320
IMSLS_LAST_STEP = 12680
IMSLS_OBS_STATUS = 20380
IMSLS_ITERATIONS = 20681
IMSLS_N_ROWS_MISSING = 20400
imslstat = loadimsl(STAT)
# Hand edited
#  Nclass and nContinous had to be passed in as arguments because there was not
#  not an automatic way of figuring them out.  The additional optional parameters
#  in the input array (x) makes it harder to determine nclass and ncontinous.
#  Also the automated code was edited to insert result.value (ncoefficients) as
#  the size of some of the output variable arrays.


def categoricalGlm(nClass, nContinuous, model, x, xColFrequencies=None, xColFixedParameter=None, xColDistParameter=None, xColVariables=None, eps=None, tolerance=None, maxIterations=None, intercept=None, noIntercept=None, effects=None, initialEstInternal=None, initialEstInput=None, maxClass=None, classInfo=None, coefStat=None, criterion=None, cov=None, means=None, caseAnalysis=None, lastStep=None, obsStatus=None, iterations=None, nRowsMissing=None):
    """ Analyzes categorical data using logistic, Probit, Poisson, and other generalized linear models.
    """
    imslstat.imsls_d_categorical_glm.restype = c_int
    shape = []
    evalstring = 'imslstat.imsls_d_categorical_glm('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nClass)'
    evalstring += ','
    evalstring += 'c_int(nContinuous)'
    evalstring += ','
    evalstring += 'c_int(model)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    xColDim = shape[1]
    evalstring += ','
    evalstring += repr(IMSLS_X_COL_DIM)
    evalstring += ','
    evalstring += 'c_int(xColDim)'
    if not (xColFrequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_FREQUENCIES)
        evalstring += ','
        evalstring += 'c_int(xColFrequencies)'
    if not (xColFixedParameter is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_FIXED_PARAMETER)
        evalstring += ','
        evalstring += 'c_int(xColFixedParameter)'
    if not (xColDistParameter is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIST_PARAMETER)
        evalstring += ','
        evalstring += 'c_int(xColDistParameter)'
    if not (xColVariables is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_VARIABLES)
        checkForDict(xColVariables, 'xColVariables',
                     ['iclass', 'icontinuous', 'iy'])
        evalstring += ','
        xColVariables_iclass_tmp = xColVariables['iclass']
        xColVariables_iclass_tmp = toNumpyArray(
            xColVariables_iclass_tmp, 'iclass', shape=shape, dtype='int', expectedShape=(nClass))
        evalstring += 'xColVariables_iclass_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        xColVariables_icontinuous_tmp = xColVariables['icontinuous']
        xColVariables_icontinuous_tmp = toNumpyArray(
            xColVariables_icontinuous_tmp, 'icontinuous', shape=shape, dtype='int', expectedShape=(nContinuous))
        evalstring += 'xColVariables_icontinuous_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        xColVariables_iy_tmp = xColVariables['iy']
        evalstring += 'c_int(xColVariables_iy_tmp)'
    if not (eps is None):
        evalstring += ','
        evalstring += repr(IMSLS_EPS)
        evalstring += ','
        evalstring += 'c_double(eps)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    checkForBoolean(intercept, 'intercept')
    if (intercept):
        evalstring += ','
        evalstring += repr(IMSLS_INTERCEPT)
    checkForBoolean(noIntercept, 'noIntercept')
    if (noIntercept):
        evalstring += ','
        evalstring += repr(IMSLS_NO_INTERCEPT)
    if not (effects is None):
        evalstring += ','
        evalstring += repr(IMSLS_EFFECTS)
        checkForDict(effects, 'effects', ['nVarEffects', 'indicesEffects'])
        evalstring += ','
        evalstring += 'c_int(effects_nEffects_tmp)'
        evalstring += ','
        effects_nVarEffects_tmp = effects['nVarEffects']
        effects_nVarEffects_tmp = toNumpyArray(
            effects_nVarEffects_tmp, 'nVarEffects', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'effects_nVarEffects_tmp.ctypes.data_as(c_void_p)'
        effects_nEffects_tmp = shape[0]
        evalstring += ','
        effects_indicesEffects_tmp = effects['indicesEffects']
        effects_indicesEffects_tmp = toNumpyArray(
            effects_indicesEffects_tmp, 'indicesEffects', shape=shape, dtype='int', expectedShape=sum(effects_nVarEffects_tmp))
        evalstring += 'effects_indicesEffects_tmp.ctypes.data_as(c_void_p)'
    checkForBoolean(initialEstInternal, 'initialEstInternal')
    if (initialEstInternal):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_EST_INTERNAL)
    if not (initialEstInput is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_EST_INPUT)
        checkForDict(initialEstInput, 'initialEstInput',
                     ['nCoefInput', 'estimates'])
        evalstring += ','
        initialEstInput_nCoefInput_tmp = initialEstInput['nCoefInput']
        evalstring += 'c_int(initialEstInput_nCoefInput_tmp)'
        evalstring += ','
        initialEstInput_estimates_tmp = initialEstInput['estimates']
        initialEstInput_estimates_tmp = toNumpyArray(
            initialEstInput_estimates_tmp, 'estimates', shape=shape, dtype='double', expectedShape=(nCoef))
        evalstring += 'initialEstInput_estimates_tmp.ctypes.data_as(c_void_p)'
    if not (maxClass is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_CLASS)
        evalstring += ','
        evalstring += 'c_int(maxClass)'
    if not (classInfo is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_INFO)
        checkForDict(classInfo, 'classInfo', [])
        evalstring += ','
        classInfo_nClassValues_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(classInfo_nClassValues_tmp)'
        evalstring += ','
        classInfo_classValues_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(classInfo_classValues_tmp)'
    if not (coefStat is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_STAT)
        checkForList(coefStat, 'coefStat')
        evalstring += ','
        coefStat_coefStatistics_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefStat_coefStatistics_tmp)'
    if not (criterion is None):
        evalstring += ','
        evalstring += repr(IMSLS_CRITERION)
        checkForList(criterion, 'criterion')
        evalstring += ','
        criterion_criterion_tmp = c_double()
        evalstring += 'byref(criterion_criterion_tmp)'
    if not (cov is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV)
        checkForList(cov, 'cov')
        evalstring += ','
        cov_cov_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cov_cov_tmp)'
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEANS)
        checkForList(means, 'means')
        evalstring += ','
        means_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(means_means_tmp)'
    if not (caseAnalysis is None):
        evalstring += ','
        evalstring += repr(IMSLS_CASE_ANALYSIS)
        checkForList(caseAnalysis, 'caseAnalysis')
        evalstring += ','
        caseAnalysis_caseAnalysis_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(caseAnalysis_caseAnalysis_tmp)'
    if not (lastStep is None):
        evalstring += ','
        evalstring += repr(IMSLS_LAST_STEP)
        checkForList(lastStep, 'lastStep')
        evalstring += ','
        lastStep_lastStep_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(lastStep_lastStep_tmp)'
    if not (obsStatus is None):
        evalstring += ','
        evalstring += repr(IMSLS_OBS_STATUS)
        checkForList(obsStatus, 'obsStatus')
        evalstring += ','
        obsStatus_obsStatus_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(obsStatus_obsStatus_tmp)'
    if not (iterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_ITERATIONS)
        checkForDict(iterations, 'iterations', [])
        evalstring += ','
        iterations_n_tmp = c_int()
        evalstring += 'byref(iterations_n_tmp)'
        evalstring += ','
        iterations_iterations_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(iterations_iterations_tmp)'
    if not (nRowsMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ROWS_MISSING)
        checkForList(nRowsMissing, 'nRowsMissing')
        evalstring += ','
        nRowsMissing_nRowsMissing_tmp = c_int()
        evalstring += 'byref(nRowsMissing_nRowsMissing_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (classInfo is None):
        processRet(classInfo_nClassValues_tmp, shape=(
            nClass), key='nClassValues', pyvar=classInfo)
        processRet(classInfo_classValues_tmp, shape=(
            sum(classInfo_nClassValues_tmp)), key='classValues', pyvar=classInfo)
    if not (coefStat is None):
        processRet(coefStat_coefStatistics_tmp,
                   shape=(result, 4), pyvar=coefStat)
    if not (criterion is None):
        processRet(criterion_criterion_tmp, shape=(1), pyvar=criterion)
    if not (cov is None):
        processRet(cov_cov_tmp, shape=(result, result), pyvar=cov)
    if not (means is None):
        if (noIntercept):
            retSize = result
        else:
            retSize = result - 1
        processRet(means_means_tmp, shape=(retSize), pyvar=means)
    if not (caseAnalysis is None):
        processRet(caseAnalysis_caseAnalysis_tmp, shape=(
            nObservations, 5), pyvar=caseAnalysis)
    if not (lastStep is None):
        processRet(lastStep_lastStep_tmp, shape=(resut), pyvar=lastStep)
    if not (obsStatus is None):
        processRet(obsStatus_obsStatus_tmp, shape=(
            nObservations), pyvar=obsStatus)
    if not (iterations is None):
        processRet(iterations_n_tmp, shape=(1), key='n', pyvar=iterations)
        processRet(iterations_iterations_tmp, shape=(
            iterations_n_tmp), key='iterations', pyvar=iterations)
    if not (nRowsMissing is None):
        processRet(nRowsMissing_nRowsMissing_tmp,
                   shape=(1), pyvar=nRowsMissing)
    return result
