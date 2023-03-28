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
from numpy import cov, double, dtype, max, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_PRINT = 13900
IMSLS_NO_PRINT = 15660
IMSLS_WEIGHTS = 15400
IMSLS_FREQUENCIES = 11790
IMSLS_R_SQUARED = 14370
IMSLS_ADJ_R_SQUARED = 10050
IMSLS_MALLOWS_CP = 12890
IMSLS_MAX_N_BEST = 13040
IMSLS_MAX_N_GOOD_SAVED = 13050
IMSLS_CRITERIONS = 11070
IMSLS_INDEPENDENT_VARIABLES = 12290
IMSLS_COEF_STATISTICS = 15610
IMSLS_INPUT_COV = 15670
imslstat = loadimsl(STAT)


def regressionSelection(x, y, xColDim=None, t_print=None, noPrint=None, weights=None, frequencies=None, rSquared=None, adjRSquared=None, mallowsCp=None, maxNBest=None, maxNGoodSaved=None, criterions=None, independentVariables=None, coefStatistics=None, inputCov=None):
    """ Selects the best multiple linear regression models.
    """
    imslstat.imsls_d_regression_selection.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_regression_selection('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nCandidate)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nCandidate = shape[1]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(nRows))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    checkForBoolean(noPrint, 'noPrint')
    if (noPrint):
        evalstring += ','
        evalstring += repr(IMSLS_NO_PRINT)
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nRows))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (rSquared is None):
        evalstring += ','
        evalstring += repr(IMSLS_R_SQUARED)
        evalstring += ','
        evalstring += 'c_int(rSquared)'
    checkForBoolean(adjRSquared, 'adjRSquared')
    if (adjRSquared):
        evalstring += ','
        evalstring += repr(IMSLS_ADJ_R_SQUARED)
    checkForBoolean(mallowsCp, 'mallowsCp')
    if (mallowsCp):
        evalstring += ','
        evalstring += repr(IMSLS_MALLOWS_CP)
    if not (maxNBest is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_N_BEST)
        evalstring += ','
        evalstring += 'c_int(maxNBest)'
    if not (maxNGoodSaved is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_N_GOOD_SAVED)
        evalstring += ','
        evalstring += 'c_int(maxNGoodSaved)'
    if not (criterions is None):
        evalstring += ','
        evalstring += repr(IMSLS_CRITERIONS)
        checkForDict(criterions, 'criterions', [])
        evalstring += ','
        criterions_indexCriterions_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(criterions_indexCriterions_tmp)'
        evalstring += ','
        criterions_criterions_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(criterions_criterions_tmp)'
    if not (independentVariables is None):
        evalstring += ','
        evalstring += repr(IMSLS_INDEPENDENT_VARIABLES)
        checkForDict(independentVariables, 'independentVariables', [])
        evalstring += ','
        independentVariables_indexVariables_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(independentVariables_indexVariables_tmp)'
        evalstring += ','
        independentVariables_independentVariables_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(independentVariables_independentVariables_tmp)'
    if not (coefStatistics is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_STATISTICS)
        checkForDict(coefStatistics, 'coefStatistics', [])
        evalstring += ','
        coefStatistics_indexCoefficients_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(coefStatistics_indexCoefficients_tmp)'
        evalstring += ','
        coefStatistics_coefficients_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefStatistics_coefficients_tmp)'
    if not (inputCov is None):
        evalstring += ','
        evalstring += repr(IMSLS_INPUT_COV)
        checkForDict(inputCov, 'inputCov', ['nObservations', 'cov'])
        evalstring += ','
        inputCov_nObservations_tmp = inputCov['nObservations']
        evalstring += 'c_int(inputCov_nObservations_tmp)'
        evalstring += ','
        inputCov_cov_tmp = inputCov['cov']
        inputCov_cov_tmp = toNumpyArray(
            inputCov_cov_tmp, 'cov', shape=shape, dtype='double', expectedShape=(nCandidate + 1, nCandidate + 1))
        evalstring += 'inputCov_cov_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (rSquared is None):
        nsize = rSquared
    else:
        nsize = nCandidate
    if not (criterions is None):
        processRet(criterions_indexCriterions_tmp, shape=(
            nsize + 1), key='indexCriterions', pyvar=criterions)
        processRet(criterions_criterions_tmp, shape=(max(
            criterions_indexCriterions_tmp[nsize] - 1, nCandidate)), key='criterions', pyvar=criterions)
    if not (independentVariables is None):
        processRet(independentVariables_indexVariables_tmp, shape=(
            nsize + 1), createArray=True, pyvar=independentVariables)
        processRet(independentVariables_independentVariables_tmp, shape=(
            independentVariables_indexVariables_tmp[nsize] - 1), createArray=True, pyvar=independentVariables)
    if not (coefStatistics is None):
        if not (rSquared is None):
            ntbest = rSquared * maxNBest
        elif (not (mallowsCp is None)) or (not (adjRSquared is None)):
            ntbest = maxNBest
        else:
            ntbest = maxNBest * nCandidate
        processRet(coefStatistics_indexCoefficients_tmp, shape=(
            ntbest + 1), key='indexCoefficients', pyvar=coefStatistics)
        processRet(coefStatistics_coefficients_tmp, shape=(
            coefStatistics_indexCoefficients_tmp[ntbest] - 1, 5), key='coefficients', pyvar=coefStatistics)
    return
