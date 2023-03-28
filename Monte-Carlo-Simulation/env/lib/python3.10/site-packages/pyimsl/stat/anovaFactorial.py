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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import complex, double, dtype, int, number, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

from pyimsl.stat.binomialCoefficient import binomialCoefficient, imslstat

IMSLS_MODEL_ORDER = 13210
IMSLS_PURE_ERROR = 13980
IMSLS_POOL_INTERACTIONS = 15620
IMSLS_ANOVA_TABLE = 10080
IMSLS_TEST_EFFECTS = 14970
IMSLS_MEANS = 13120
imslstat = loadimsl(STAT)


def anovaFactorial(nLevels, y, modelOrder=None, pureError=None, poolInteractions=None, anovaTable=None, testEffects=None, means=None):
    """ Analyzes a balanced factorial design with fixed effects.
    """
    imslstat.imsls_d_anova_factorial.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_anova_factorial('
    evalstring += 'c_int(nSubscripts)'
    evalstring += ','
    nLevels = toNumpyArray(nLevels, 'nLevels', shape=shape,
                           dtype='int', expectedShape=(0))
    evalstring += 'nLevels.ctypes.data_as(c_void_p)'
    nSubscripts = shape[0]
    evalstring += ','
    testEffectsN = nSubscripts - 1
    ySize = 1
    for i in range(0, nSubscripts):
        ySize *= nLevels[i]
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(ySize))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (modelOrder is None):
        evalstring += ','
        evalstring += repr(IMSLS_MODEL_ORDER)
        evalstring += ','
        evalstring += 'c_int(modelOrder)'
    checkForBoolean(pureError, 'pureError')
    if (pureError):
        evalstring += ','
        evalstring += repr(IMSLS_PURE_ERROR)
    checkForBoolean(poolInteractions, 'poolInteractions')
    if (poolInteractions):
        evalstring += ','
        evalstring += repr(IMSLS_POOL_INTERACTIONS)
        testEffectsN = nSubscripts
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
    if not (testEffects is None):
        evalstring += ','
        evalstring += repr(IMSLS_TEST_EFFECTS)
        checkForList(testEffects, 'testEffects')
        evalstring += ','
        testEffects_testEffects_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(testEffects_testEffects_tmp)'
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEANS)
        checkForList(means, 'means')
        evalstring += ','
        means_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(means_means_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (anovaTable is None):
        processRet(anovaTable_anovaTable_tmp, shape=(15), pyvar=anovaTable)
    if not (testEffects is None):
        # The number of elements in testEffects is calculated according
        # to a fairly complex formula.  See the description in
        # the documentation.
        if (poolInteractions):
            n = nSubscripts
        else:
            n = nSubscripts - 1
        model_order = nSubscripts - 1
        if (not (modelOrder is None)):
            model_order = modelOrder
        denominator = n
        if (n > abs(model_order)):
            denominator = model_order
        nef = 0
        for i in range(0, denominator):
            nef += binomialCoefficient(n, i + 1)
        processRet(testEffects_testEffects_tmp,
                   shape=(nef, 4), pyvar=testEffects)
    if not (means is None):
        if (poolInteractions):
            n = nSubscripts
        else:
            n = nSubscripts - 1
        meansSize = 1
        for i in range(0, n):
            meansSize = meansSize * (nLevels[i] + 1)
        processRet(means_means_tmp, shape=(meansSize), pyvar=means)
    return result
