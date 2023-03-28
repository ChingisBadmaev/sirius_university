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
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from pyimsl.stat.binomialCoefficient import binomialCoefficient

IMSLS_ANOVA_TABLE = 10080
IMSLS_GROUP_MEANS = 12110
IMSLS_GROUP_STD_DEVS = 12130
IMSLS_GROUP_COUNTS = 12090
IMSLS_CONFIDENCE = 10860
IMSLS_TUKEY = 15090
IMSLS_DUNN_SIDAK = 11280
IMSLS_BONFERRONI = 10270
IMSLS_SCHEFFE = 15870
IMSLS_ONE_AT_A_TIME = 13560
imslstat = loadimsl(STAT)


def anovaOneway(n, y, anovaTable=None, groupMeans=None, groupStdDevs=None, groupCounts=None, confidence=None, tukey=None, dunnSidak=None, bonferroni=None, scheffe=None, oneAtATime=None):
    """ Analyzes a one-way classification model.
    """
    imslstat.imsls_d_anova_oneway.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_anova_oneway('
    evalstring += 'c_int(nGroups)'
    evalstring += ','
    n = toNumpyArray(n, 'n', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'n.ctypes.data_as(c_void_p)'
    nGroups = shape[0]
    evalstring += ','
    ySize = 0
    for i in range(0, nGroups):
        ySize += n[i]
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(ySize))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
    if not (groupMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_GROUP_MEANS)
        checkForList(groupMeans, 'groupMeans')
        evalstring += ','
        groupMeans_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(groupMeans_means_tmp)'
    if not (groupStdDevs is None):
        evalstring += ','
        evalstring += repr(IMSLS_GROUP_STD_DEVS)
        checkForList(groupStdDevs, 'groupStdDevs')
        evalstring += ','
        groupStdDevs_stdDevs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(groupStdDevs_stdDevs_tmp)'
    if not (groupCounts is None):
        evalstring += ','
        evalstring += repr(IMSLS_GROUP_COUNTS)
        checkForList(groupCounts, 'groupCounts')
        evalstring += ','
        groupCounts_counts_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(groupCounts_counts_tmp)'
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (tukey is None):
        evalstring += ','
        evalstring += repr(IMSLS_TUKEY)
        checkForList(tukey, 'tukey')
        evalstring += ','
        tukey_ciDiffMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(tukey_ciDiffMeans_tmp)'
    if not (dunnSidak is None):
        evalstring += ','
        evalstring += repr(IMSLS_DUNN_SIDAK)
        checkForList(dunnSidak, 'dunnSidak')
        evalstring += ','
        dunnSidak_ciDiffMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dunnSidak_ciDiffMeans_tmp)'
    if not (bonferroni is None):
        evalstring += ','
        evalstring += repr(IMSLS_BONFERRONI)
        checkForList(bonferroni, 'bonferroni')
        evalstring += ','
        bonferroni_ciDiffMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(bonferroni_ciDiffMeans_tmp)'
    if not (scheffe is None):
        evalstring += ','
        evalstring += repr(IMSLS_SCHEFFE)
        checkForList(scheffe, 'scheffe')
        evalstring += ','
        scheffe_ciDiffMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(scheffe_ciDiffMeans_tmp)'
    if not (oneAtATime is None):
        evalstring += ','
        evalstring += repr(IMSLS_ONE_AT_A_TIME)
        checkForList(oneAtATime, 'oneAtATime')
        evalstring += ','
        oneAtATime_ciDiffMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(oneAtATime_ciDiffMeans_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (anovaTable is None):
        processRet(anovaTable_anovaTable_tmp, shape=(15), pyvar=anovaTable)
    if not (groupMeans is None):
        processRet(groupMeans_means_tmp, shape=(nGroups), pyvar=groupMeans)
    if not (groupStdDevs is None):
        processRet(groupStdDevs_stdDevs_tmp,
                   shape=(nGroups), pyvar=groupStdDevs)
    if not (groupCounts is None):
        processRet(groupCounts_counts_tmp, shape=(nGroups), pyvar=groupCounts)

    retSize = binomialCoefficient(nGroups, 2)
    if not (tukey is None):
        processRet(tukey_ciDiffMeans_tmp, shape=(retSize, 5), pyvar=tukey)
    if not (dunnSidak is None):
        processRet(dunnSidak_ciDiffMeans_tmp,
                   shape=(retSize, 5), pyvar=dunnSidak)
    if not (bonferroni is None):
        processRet(bonferroni_ciDiffMeans_tmp,
                   shape=(retSize, 5), pyvar=bonferroni)
    if not (scheffe is None):
        processRet(scheffe_ciDiffMeans_tmp, shape=(retSize, 5), pyvar=scheffe)
    if not (oneAtATime is None):
        processRet(oneAtATime_ciDiffMeans_tmp,
                   shape=(retSize, 5), pyvar=oneAtATime)
    return result
