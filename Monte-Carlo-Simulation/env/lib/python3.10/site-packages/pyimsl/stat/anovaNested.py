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
from numpy import array, double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_ANOVA_TABLE = 10080
IMSLS_CONFIDENCE = 10860
IMSLS_VARIANCE_COMPONENTS = 15310
IMSLS_EMS = 11350
IMSLS_Y_MEANS = 30033
imslstat = loadimsl(STAT)


def anovaNested(nFactors, equalOption, nLevels, y, anovaTable=None, confidence=None, varianceComponents=None, ems=None, yMeans=None):
    """ Analyzes a completely nested random model with possibly unequal numbers in the subgroups.
    """
    imslstat.imsls_d_anova_nested.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_anova_nested('
    evalstring += 'c_int(nFactors)'
    evalstring += ','
    evalstring += 'c_int(equalOption)'
    evalstring += ','
    nLevels = toNumpyArray(nLevels, 'nLevels', shape=shape, dtype='int')
    evalstring += 'nLevels.ctypes.data_as(c_void_p)'
    evalstring += ','
    if (equalOption == 1):
        lnl = 0
        lnlnf = 1
        for i in range(0, nFactors - 1):
            tmp = nLevels[0]
            for j in range(1, i):
                tmp *= nLevels[j]
            lnl += tmp
            lnlnf *= nLevels[i]
        nobs = lnlnf * nLevels[nFactors - 1]
    else:
        if (nFactors > 2):
            mlast = 1
            m = 1
            l = 0
            n = 1
            for i in range(1, nFactors):
                i_ = i - 1
                for j in range(1, n + 1):
                    j_ = j - 1
                    m += nLevels[l + j_]
                l += n
                n = m - mlast
                mlast = m
        else:
            n = nLevels[0]
            m = n + 1
        lnl = m
        lnlnf = n
        nunits = 0
        for i in range(m - n, m):
            nunits += nLevels[i]
        nobs = nunits

    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(nobs))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
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
        ems_expectMeanSq_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(ems_expectMeanSq_tmp)'
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
        processRet(varianceComponents_varianceComponents_tmp,
                   shape=(nFactors, 9), pyvar=varianceComponents)
    if not (ems is None):
        # The length of the ems array is omitted from the documentation,
        # but I think it's 6 based on the example.
        #
        processRet(ems_expectMeanSq_tmp, shape=(6), pyvar=ems)
    if not (yMeans is None):
        if (equalOption == 0):
            yMeansLen = 1
            for i in range(0, lnl - lnlnf):
                yMeansLen += nLevels[i]
        else:
            yMeansLen = 1
            for i in range(0, nFactors - 1):
                tmp = nLevels[0]
                for j in range(1, i + 1):
                    tmp *= nLevels[j]
                yMeansLen += tmp
        processRet(yMeans_yMeans_tmp, shape=(yMeansLen), pyvar=yMeans)
    return result
