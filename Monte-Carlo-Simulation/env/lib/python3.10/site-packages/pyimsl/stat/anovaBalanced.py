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
from numpy import abs, double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_ANOVA_TABLE = 10080
IMSLS_MODEL = 20100
IMSLS_CONFIDENCE = 10860
IMSLS_VARIANCE_COMPONENTS = 15310
IMSLS_EMS = 11350
IMSLS_Y_MEANS = 30033
imslstat = loadimsl(STAT)


def anovaBalanced(nLevels, y, nRandom, indexRandomFactor, nFactorsPerEffect, indexFactorPerEffect, anovaTable=None, model=None, confidence=None, varianceComponents=None, ems=None, yMeans=None):
    """ Analyzes a balanced complete experimental design for a fixed, random, or mixed model.
    """
    imslstat.imsls_d_anova_balanced.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_anova_balanced('
    evalstring += 'c_int(nFactors)'
    evalstring += ','
    nLevels = toNumpyArray(nLevels, 'nLevels', shape=shape,
                           dtype='int', expectedShape=(0))
    evalstring += 'nLevels.ctypes.data_as(c_void_p)'
    nFactors = shape[0]
    evalstring += ','
    ySize = 1
    for i in range(0, nFactors):
        ySize *= nLevels[i]
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(ySize))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(nRandom)'
    evalstring += ','
    indexRandomFactor = toNumpyArray(
        indexRandomFactor, 'indexRandomFactor', shape=shape, dtype='int', expectedShape=abs(nRandom))
    evalstring += 'indexRandomFactor.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(nModelEffects)'
    evalstring += ','
    nFactorsPerEffect = toNumpyArray(
        nFactorsPerEffect, 'nFactorsPerEffect', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'nFactorsPerEffect.ctypes.data_as(c_void_p)'
    nModelEffects = shape[0]
    evalstring += ','
    ifLen = 0
    for i in range(0, nModelEffects):
        ifLen += nFactorsPerEffect[i]
    indexFactorPerEffect = toNumpyArray(
        indexFactorPerEffect, 'indexFactorPerEffect', shape=shape, dtype='int', expectedShape=(ifLen))
    evalstring += 'indexFactorPerEffect.ctypes.data_as(c_void_p)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
    if not (model is None):
        evalstring += ','
        evalstring += repr(IMSLS_MODEL)
        evalstring += ','
        evalstring += 'c_int(model)'
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (varianceComponents is None):
        evalstring += ','
        evalstring += repr(IMSLS_VARIANCE_COMPONENTS)
        checkForList(varianceComponents, 'varianceComponents')
        evalstring += ','
        varianceComponents_varianceComponents_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(varianceComponents_varianceComponents_tmp)'
    if not (ems is None):
        evalstring += ','
        evalstring += repr(IMSLS_EMS)
        checkForList(ems, 'ems')
        evalstring += ','
        ems_ems_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(ems_ems_tmp)'
    if not (yMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_Y_MEANS)
        checkForList(yMeans, 'yMeans')
        evalstring += ','
        yMeans_yMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(yMeans_yMeans_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (anovaTable is None):
        processRet(anovaTable_anovaTable_tmp, shape=(15), pyvar=anovaTable)
    if not (varianceComponents is None):
        varianceComponents[:] = []
        processRet(varianceComponents_varianceComponents_tmp, shape=(
            nModelEffects + 1, 9), pyvar=varianceComponents)
    if not (ems is None):
        processRet(ems_ems_tmp, shape=(
            ((nModelEffects + 1) * (nModelEffects + 2) / 2)), pyvar=ems)
    if not (yMeans is None):
        yMeansLen = 1
        for i in range(0, nFactors - 1):
            yMeansLen *= nLevels[i] + 1
        processRet(yMeans_yMeans_tmp, shape=(yMeansLen), pyvar=yMeans)
    return result
