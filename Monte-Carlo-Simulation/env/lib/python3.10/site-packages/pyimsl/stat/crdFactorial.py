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
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_char_p, c_double, c_int, c_void_p
from pyimsl.stat.binomialCoefficient import binomialCoefficient, imslstat

IMSLS_N_MISSING = 13440
IMSLS_CV = 40134
IMSLS_GRAND_MEAN = 40112
IMSLS_FACTOR_MEANS = 40186
IMSLS_FACTOR_STD_ERRORS = 40192
IMSLS_TWO_WAY_MEANS = 40190
IMSLS_TWO_WAY_STD_ERRORS = 40188
IMSLS_TREATMENT_MEANS = 40117
IMSLS_TREATMENT_STD_ERROR = 40194
IMSLS_ANOVA_ROW_LABELS = 40200
imslstat = loadimsl(STAT)


def crdFactorial(nLocations, nFactors, nLevels, model, y, nMissing=None, cv=None, grandMean=None, factorMeans=None, factorStdErrors=None, twoWayMeans=None, twoWayStdErrors=None, treatmentMeans=None, treatmentStdError=None, anovaRowLabels=None):
    """ Analyzes data from balanced and unbalanced completely randomized experiments.
    """
    imslstat.imsls_d_crd_factorial.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_crd_factorial('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    evalstring += 'c_int(nLocations)'
    evalstring += ','
    evalstring += 'c_int(nFactors)'
    evalstring += ','
    nLevels = toNumpyArray(nLevels, 'nLevels', shape=shape,
                           dtype='int', expectedShape=(nFactors + 1))
    evalstring += 'nLevels.ctypes.data_as(c_void_p)'
    evalstring += ','
    model = toNumpyArray(model, 'model', shape=shape,
                         dtype='int', expectedShape=(0, nFactors + 1))
    evalstring += 'model.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(nObs))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nMissing_tmp = c_int()
        evalstring += 'byref(nMissing_nMissing_tmp)'
    if not (cv is None):
        evalstring += ','
        evalstring += repr(IMSLS_CV)
        checkForList(cv, 'cv')
        evalstring += ','
        cv_cv_tmp = c_double()
        evalstring += 'byref(cv_cv_tmp)'
    if not (grandMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRAND_MEAN)
        checkForList(grandMean, 'grandMean')
        evalstring += ','
        grandMean_grandMean_tmp = c_double()
        evalstring += 'byref(grandMean_grandMean_tmp)'
    if not (factorMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_FACTOR_MEANS)
        checkForList(factorMeans, 'factorMeans')
        evalstring += ','
        factorMeans_factorMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(factorMeans_factorMeans_tmp)'
    if not (factorStdErrors is None):
        evalstring += ','
        evalstring += repr(IMSLS_FACTOR_STD_ERRORS)
        checkForList(factorStdErrors, 'factorStdErrors')
        evalstring += ','
        factorStdErrors_factorStdErr_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(factorStdErrors_factorStdErr_tmp)'
    if not (twoWayMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_TWO_WAY_MEANS)
        checkForList(twoWayMeans, 'twoWayMeans')
        evalstring += ','
        twoWayMeans_twoWayMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(twoWayMeans_twoWayMeans_tmp)'
    if not (twoWayStdErrors is None):
        evalstring += ','
        evalstring += repr(IMSLS_TWO_WAY_STD_ERRORS)
        checkForList(twoWayStdErrors, 'twoWayStdErrors')
        evalstring += ','
        twoWayStdErrors_twoWayStdErr_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(twoWayStdErrors_twoWayStdErr_tmp)'
    if not (treatmentMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_TREATMENT_MEANS)
        checkForList(treatmentMeans, 'treatmentMeans')
        evalstring += ','
        treatmentMeans_treatmentMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(treatmentMeans_treatmentMeans_tmp)'
    if not (treatmentStdError is None):
        evalstring += ','
        evalstring += repr(IMSLS_TREATMENT_STD_ERROR)
        checkForList(treatmentStdError, 'treatmentStdError')
        evalstring += ','
        treatmentStdError_treatmentStdErr_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(treatmentStdError_treatmentStdErr_tmp)'
    if not (anovaRowLabels is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_ROW_LABELS)
        checkForList(anovaRowLabels, 'anovaRowLabels')
        evalstring += ','
        anovaRowLabels_anovaRowLabels_tmp = POINTER(c_char_p)(c_char_p())
        evalstring += 'byref(anovaRowLabels_anovaRowLabels_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nMissing is None):
        processRet(nMissing_nMissing_tmp, shape=1, pyvar=nMissing)
    if not (cv is None):
        processRet(cv_cv_tmp, shape=1, pyvar=cv)
    if not (grandMean is None):
        processRet(grandMean_grandMean_tmp, shape=1, pyvar=grandMean)
    if not (factorMeans is None):
        fmLen = 0
        for i in range(0, nFactors):
            fmLen += nLevels[i]
        processRet(factorMeans_factorMeans_tmp,
                   shape=(fmLen), pyvar=factorMeans)
    if not (factorStdErrors is None):
        processRet(factorStdErrors_factorStdErr_tmp,
                   shape=(nFactors, 2), pyvar=factorStdErrors)
    if not (twoWayMeans is None):
        if (nFactors > 1):
            twoWayLen = 0
            f = nFactors - 2
            for i in range(0, f + 1):
                for j in range(i + 1, f + 2):
                    twoWayLen += nLevels[i] * nLevels[j]
            processRet(twoWayMeans_twoWayMeans_tmp,
                       shape=(twoWayLen), pyvar=twoWayMeans)
    if not (twoWayStdErrors is None):
        nTwoWay = 0
        for i in range(0, nFactors):
            for j in range(i + 1, nFactors):
                nTwoWay += 1
        if (nTwoWay > 0):
            processRet(twoWayStdErrors_twoWayStdErr_tmp,
                       shape=(nTwoWay, 2), pyvar=twoWayStdErrors)
    if not (treatmentMeans is None):
        tmLen = 1
        for i in range(0, nFactors):
            tmLen *= nLevels[i]
        processRet(treatmentMeans_treatmentMeans_tmp,
                   shape=(tmLen), pyvar=treatmentMeans)
    if not (treatmentStdError is None):
        processRet(treatmentStdError_treatmentStdErr_tmp,
                   shape=(2), pyvar=treatmentStdError)

    nReplicates = nLevels[nFactors]
    a = 2
    if (nLocations > 1):
        if (nReplicates <= 1):
            a = 3
        else:
            a = 4
    nAnova = a
    model_order = nFactors - 1
    for i in range(1, model_order + 1):
        nAnova += int(binomialCoefficient(nFactors, i))

    if not (anovaRowLabels is None):
        processRet(anovaRowLabels_anovaRowLabels_tmp,
                   shape=(nAnova), pyvar=anovaRowLabels)
    return processRet(result, shape=(nAnova, 6), result=True)
