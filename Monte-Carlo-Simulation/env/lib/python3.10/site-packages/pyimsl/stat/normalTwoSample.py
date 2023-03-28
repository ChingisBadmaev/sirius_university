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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, checkForDict, processRet
from numpy import double, dtype, shape
from ctypes import byref, c_double, c_int, c_void_p

IMSLS_MEANS = 13120
IMSLS_CONFIDENCE_MEAN = 10870
IMSLS_CI_DIFF_FOR_EQUAL_VARS = 16076
IMSLS_CI_DIFF_FOR_UNEQUAL_VARS = 16077
IMSLS_T_TEST_FOR_EQUAL_VARS = 16073
IMSLS_T_TEST_FOR_UNEQUAL_VARS = 16074
IMSLS_T_TEST_NULL = 15170
IMSLS_POOLED_VARIANCE = 13850
IMSLS_CONFIDENCE_VARIANCE = 10900
IMSLS_CI_COMMON_VARIANCE = 10530
IMSLS_CHI_SQUARED_TEST = 10510
IMSLS_CHI_SQUARED_TEST_NULL = 10520
IMSLS_STD_DEVS = 14840
IMSLS_CI_RATIO_VARIANCES = 16075
IMSLS_F_TEST = 11920
IMSLS_INTERMEDIATE_RESULTS = 50955
IMSLS_UNION = 50906
IMSLS_FINAL_RESULTS = 50956
imslstat = loadimsl(STAT)


def normalTwoSample(x1, x2, means=None, confidenceMean=None, ciDiffForEqualVars=None, ciDiffForUnequalVars=None, tTestForEqualVars=None, tTestForUnequalVars=None, tTestNull=None, pooledVariance=None, confidenceVariance=None, ciCommonVariance=None, chiSquaredTest=None, chiSquaredTestNull=None, stdDevs=None, ciRatioVariances=None, fTest=None, intermediateResults=None, union=None, finalResults=None):
    """ Computes statistics for mean and variance inferences using samples from two normal populations.
    """
    imslstat.imsls_d_normal_two_sample.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_normal_two_sample('
    evalstring += 'c_int(n1Observations)'
    evalstring += ','
    x1 = toNumpyArray(x1, 'x1', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x1.ctypes.data_as(c_void_p)'
    n1Observations = shape[0]
    evalstring += ','
    evalstring += 'c_int(n2Observations)'
    evalstring += ','
    x2 = toNumpyArray(x2, 'x2', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x2.ctypes.data_as(c_void_p)'
    n2Observations = shape[0]
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEANS)
        checkForDict(means, 'means', [])
        evalstring += ','
        means_x1Mean_tmp = c_double()
        evalstring += 'byref(means_x1Mean_tmp)'
        evalstring += ','
        means_x2Mean_tmp = c_double()
        evalstring += 'byref(means_x2Mean_tmp)'
    if not (confidenceMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE_MEAN)
        evalstring += ','
        evalstring += 'c_double(confidenceMean)'
    if not (ciDiffForEqualVars is None):
        evalstring += ','
        evalstring += repr(IMSLS_CI_DIFF_FOR_EQUAL_VARS)
        checkForDict(ciDiffForEqualVars, 'ciDiffForEqualVars', [])
        evalstring += ','
        ciDiffForEqualVars_lowerLimit_tmp = c_double()
        evalstring += 'byref(ciDiffForEqualVars_lowerLimit_tmp)'
        evalstring += ','
        ciDiffForEqualVars_upperLimit_tmp = c_double()
        evalstring += 'byref(ciDiffForEqualVars_upperLimit_tmp)'
    if not (ciDiffForUnequalVars is None):
        evalstring += ','
        evalstring += repr(IMSLS_CI_DIFF_FOR_UNEQUAL_VARS)
        checkForList(ciDiffForUnequalVars, 'ciDiffForUnequalVars')
        evalstring += ','
        ciDiffForUnequalVars_lowerLimit_tmp = c_double()
        evalstring += 'byref(ciDiffForUnequalVars_lowerLimit_tmp)'
    if not (tTestForEqualVars is None):
        evalstring += ','
        evalstring += repr(IMSLS_T_TEST_FOR_EQUAL_VARS)
        checkForDict(tTestForEqualVars, 'tTestForEqualVars', [])
        evalstring += ','
        tTestForEqualVars_df_tmp = c_int()
        evalstring += 'byref(tTestForEqualVars_df_tmp)'
        evalstring += ','
        tTestForEqualVars_t_tmp = c_double()
        evalstring += 'byref(tTestForEqualVars_t_tmp)'
        evalstring += ','
        tTestForEqualVars_pValue_tmp = c_double()
        evalstring += 'byref(tTestForEqualVars_pValue_tmp)'
    if not (tTestForUnequalVars is None):
        evalstring += ','
        evalstring += repr(IMSLS_T_TEST_FOR_UNEQUAL_VARS)
        checkForDict(tTestForUnequalVars, 'tTestForUnequalVars', [])
        evalstring += ','
        tTestForUnequalVars_df_tmp = c_double()
        evalstring += 'byref(tTestForUnequalVars_df_tmp)'
        evalstring += ','
        tTestForUnequalVars_t_tmp = c_double()
        evalstring += 'byref(tTestForUnequalVars_t_tmp)'
        evalstring += ','
        tTestForUnequalVars_pValue_tmp = c_double()
        evalstring += 'byref(tTestForUnequalVars_pValue_tmp)'
    if not (tTestNull is None):
        evalstring += ','
        evalstring += repr(IMSLS_T_TEST_NULL)
        evalstring += ','
        evalstring += 'c_double(tTestNull)'
    if not (pooledVariance is None):
        evalstring += ','
        evalstring += repr(IMSLS_POOLED_VARIANCE)
        checkForList(pooledVariance, 'pooledVariance')
        evalstring += ','
        pooledVariance_pooledVariance_tmp = c_double()
        evalstring += 'byref(pooledVariance_pooledVariance_tmp)'
    if not (confidenceVariance is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE_VARIANCE)
        evalstring += ','
        evalstring += 'c_double(confidenceVariance)'
    if not (ciCommonVariance is None):
        evalstring += ','
        evalstring += repr(IMSLS_CI_COMMON_VARIANCE)
        checkForDict(ciCommonVariance, 'ciCommonVariance', [])
        evalstring += ','
        ciCommonVariance_lowerLimit_tmp = c_double()
        evalstring += 'byref(ciCommonVariance_lowerLimit_tmp)'
        evalstring += ','
        ciCommonVariance_upperLimit_tmp = c_double()
        evalstring += 'byref(ciCommonVariance_upperLimit_tmp)'
    if not (chiSquaredTest is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED_TEST)
        checkForDict(chiSquaredTest, 'chiSquaredTest', [])
        evalstring += ','
        chiSquaredTest_df_tmp = c_int()
        evalstring += 'byref(chiSquaredTest_df_tmp)'
        evalstring += ','
        chiSquaredTest_chiSquared_tmp = c_double()
        evalstring += 'byref(chiSquaredTest_chiSquared_tmp)'
        evalstring += ','
        chiSquaredTest_pValue_tmp = c_double()
        evalstring += 'byref(chiSquaredTest_pValue_tmp)'
    if not (chiSquaredTestNull is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED_TEST_NULL)
        evalstring += ','
        evalstring += 'c_double(chiSquaredTestNull)'
    if not (stdDevs is None):
        evalstring += ','
        evalstring += repr(IMSLS_STD_DEVS)
        checkForDict(stdDevs, 'stdDevs', [])
        evalstring += ','
        stdDevs_x1StdDev_tmp = c_double()
        evalstring += 'byref(stdDevs_x1StdDev_tmp)'
        evalstring += ','
        stdDevs_x2StdDev_tmp = c_double()
        evalstring += 'byref(stdDevs_x2StdDev_tmp)'
    if not (ciRatioVariances is None):
        evalstring += ','
        evalstring += repr(IMSLS_CI_RATIO_VARIANCES)
        checkForDict(ciRatioVariances, 'ciRatioVariances', [])
        evalstring += ','
        ciRatioVariances_lowerLimit_tmp = c_double()
        evalstring += 'byref(ciRatioVariances_lowerLimit_tmp)'
        evalstring += ','
        ciRatioVariances_upperLimit_tmp = c_double()
        evalstring += 'byref(ciRatioVariances_upperLimit_tmp)'
    if not (fTest is None):
        evalstring += ','
        evalstring += repr(IMSLS_F_TEST)
        checkForDict(fTest, 'fTest', [])
        evalstring += ','
        fTest_dfNumerator_tmp = c_int()
        evalstring += 'byref(fTest_dfNumerator_tmp)'
        evalstring += ','
        fTest_dfDenominator_tmp = c_int()
        evalstring += 'byref(fTest_dfDenominator_tmp)'
        evalstring += ','
        fTest_f_tmp = c_double()
        evalstring += 'byref(fTest_f_tmp)'
        evalstring += ','
        fTest_pValue_tmp = c_double()
        evalstring += 'byref(fTest_pValue_tmp)'

    if not (intermediateResults is None):
        evalstring += ','
        evalstring += repr(IMSLS_INTERMEDIATE_RESULTS)
        checkForList(intermediateResults, 'intermediateResults')
        evalstring += ','
        intermediateResults_stats_tmp = toNumpyArray(
            intermediateResults, 'intermediateResults', shape=shape, dtype='double', expectedShape=(25))
        evalstring += 'intermediateResults_stats_tmp.ctypes.data_as(c_void_p)'
    if not (union is None):
        evalstring += ','
        evalstring += repr(IMSLS_UNION)
        checkForDict(union, 'union', ['stats1', 'stats2'])
        evalstring += ','
        union_stats1_tmp = union['stats1']
        union_stats1_tmp = toNumpyArray(
            union_stats1_tmp, 'stats1', shape=shape, dtype='double', expectedShape=(25))
        evalstring += 'union_stats1_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        union_stats2_tmp = union['stats2']
        union_stats2_tmp = toNumpyArray(
            union_stats2_tmp, 'stats2', shape=shape, dtype='double', expectedShape=(25))
        evalstring += 'union_stats2_tmp.ctypes.data_as(c_void_p)'
    if not (finalResults is None):
        evalstring += ','
        evalstring += repr(IMSLS_FINAL_RESULTS)
        checkForList(finalResults, 'finalResults')
        evalstring += ','
        finalResults_finalStats_tmp = toNumpyArray(
            finalResults, 'finalResults', shape=shape, dtype='double', expectedShape=(25))
        evalstring += 'finalResults_finalStats_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (means is None):
        processRet(means_x1Mean_tmp, shape=(1), key='x1Mean', pyvar=means)
        processRet(means_x2Mean_tmp, shape=(1), key='x2Mean', pyvar=means)
    if not (ciDiffForEqualVars is None):
        processRet(ciDiffForEqualVars_lowerLimit_tmp, shape=(
            1), key='lowerLimit', pyvar=ciDiffForEqualVars)
        processRet(ciDiffForEqualVars_upperLimit_tmp, shape=(
            1), key='upperLimit', pyvar=ciDiffForEqualVars)
    if not (ciDiffForUnequalVars is None):
        processRet(ciDiffForUnequalVars_lowerLimit_tmp,
                   shape=(1), pyvar=ciDiffForUnequalVars)
    if not (tTestForEqualVars is None):
        processRet(tTestForEqualVars_df_tmp, shape=(
            1), key='df', pyvar=tTestForEqualVars)
        processRet(tTestForEqualVars_t_tmp, shape=(
            1), key='t', pyvar=tTestForEqualVars)
        processRet(tTestForEqualVars_pValue_tmp, shape=(
            1), key='pValue', pyvar=tTestForEqualVars)
    if not (tTestForUnequalVars is None):
        processRet(tTestForUnequalVars_df_tmp, shape=(
            1), key='df', pyvar=tTestForUnequalVars)
        processRet(tTestForUnequalVars_t_tmp, shape=(
            1), key='t', pyvar=tTestForUnequalVars)
        processRet(tTestForUnequalVars_pValue_tmp, shape=(
            1), key='pValue', pyvar=tTestForUnequalVars)
    if not (pooledVariance is None):
        processRet(pooledVariance_pooledVariance_tmp,
                   shape=(1), pyvar=pooledVariance)
    if not (ciCommonVariance is None):
        processRet(ciCommonVariance_lowerLimit_tmp, shape=(
            1), key='lowerLimit', pyvar=ciCommonVariance)
        processRet(ciCommonVariance_upperLimit_tmp, shape=(
            1), key='upperLimit', pyvar=ciCommonVariance)
    if not (chiSquaredTest is None):
        processRet(chiSquaredTest_df_tmp, shape=(
            1), key='df', pyvar=chiSquaredTest)
        processRet(chiSquaredTest_chiSquared_tmp, shape=(
            1), key='chiSquared', pyvar=chiSquaredTest)
        processRet(chiSquaredTest_pValue_tmp, shape=(
            1), key='pValue', pyvar=chiSquaredTest)
    if not (stdDevs is None):
        processRet(stdDevs_x1StdDev_tmp, shape=(
            1), key='x1StdDev', pyvar=stdDevs)
        processRet(stdDevs_x2StdDev_tmp, shape=(
            1), key='x2StdDev', pyvar=stdDevs)
    if not (ciRatioVariances is None):
        processRet(ciRatioVariances_lowerLimit_tmp, shape=(
            1), key='lowerLimit', pyvar=ciRatioVariances)
        processRet(ciRatioVariances_upperLimit_tmp, shape=(
            1), key='upperLimit', pyvar=ciRatioVariances)
    if not (fTest is None):
        processRet(fTest_dfNumerator_tmp, shape=(
            1), key='dfNumerator', pyvar=fTest)
        processRet(fTest_dfDenominator_tmp, shape=(
            1), key='dfDenominator', pyvar=fTest)
        processRet(fTest_f_tmp, shape=(1), key='f', pyvar=fTest)
        processRet(fTest_pValue_tmp, shape=(1), key='pValue', pyvar=fTest)
    if not (intermediateResults is None):
        processRet(intermediateResults_stats_tmp, shape=(
            25), inout=True, pyvar=intermediateResults)
    if not (finalResults is None):
        processRet(finalResults_finalStats_tmp, shape=(25), pyvar=finalResults)
    return result
