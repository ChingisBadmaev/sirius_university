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

IMSLS_CONFIDENCE_MEAN = 10870
IMSLS_CI_MEAN = 10560
IMSLS_STD_DEV = 14830
IMSLS_T_TEST = 15130
IMSLS_T_TEST_NULL = 15170
IMSLS_CONFIDENCE_VARIANCE = 10900
IMSLS_CI_VARIANCE = 10590
IMSLS_CHI_SQUARED_TEST = 10510
IMSLS_CHI_SQUARED_TEST_NULL = 10520
imslstat = loadimsl(STAT)


def normalOneSample(x, confidenceMean=None, ciMean=None, stdDev=None, tTest=None, tTestNull=None, confidenceVariance=None, ciVariance=None, chiSquaredTest=None, chiSquaredTestNull=None):
    """ Computes statistics for mean and variance inferences using a sample from a normal population.
    """
    imslstat.imsls_d_normal_one_sample.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_normal_one_sample('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (confidenceMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE_MEAN)
        evalstring += ','
        evalstring += 'c_double(confidenceMean)'
    if not (ciMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_CI_MEAN)
        checkForDict(ciMean, 'ciMean', [])
        evalstring += ','
        ciMean_lowerLimit_tmp = c_double()
        evalstring += 'byref(ciMean_lowerLimit_tmp)'
        evalstring += ','
        ciMean_upperLimit_tmp = c_double()
        evalstring += 'byref(ciMean_upperLimit_tmp)'
    if not (stdDev is None):
        evalstring += ','
        evalstring += repr(IMSLS_STD_DEV)
        checkForList(stdDev, 'stdDev')
        evalstring += ','
        stdDev_stdDev_tmp = c_double()
        evalstring += 'byref(stdDev_stdDev_tmp)'
    if not (tTest is None):
        evalstring += ','
        evalstring += repr(IMSLS_T_TEST)
        checkForDict(tTest, 'tTest', [])
        evalstring += ','
        tTest_df_tmp = c_int()
        evalstring += 'byref(tTest_df_tmp)'
        evalstring += ','
        tTest_t_tmp = c_double()
        evalstring += 'byref(tTest_t_tmp)'
        evalstring += ','
        tTest_pValue_tmp = c_double()
        evalstring += 'byref(tTest_pValue_tmp)'
    if not (tTestNull is None):
        evalstring += ','
        evalstring += repr(IMSLS_T_TEST_NULL)
        evalstring += ','
        evalstring += 'c_double(tTestNull)'
    if not (confidenceVariance is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE_VARIANCE)
        evalstring += ','
        evalstring += 'c_double(confidenceVariance)'
    if not (ciVariance is None):
        evalstring += ','
        evalstring += repr(IMSLS_CI_VARIANCE)
        checkForDict(ciVariance, 'ciVariance', [])
        evalstring += ','
        ciVariance_lowerLimit_tmp = c_double()
        evalstring += 'byref(ciVariance_lowerLimit_tmp)'
        evalstring += ','
        ciVariance_upperLimit_tmp = c_double()
        evalstring += 'byref(ciVariance_upperLimit_tmp)'
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
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (ciMean is None):
        processRet(ciMean_lowerLimit_tmp, shape=(
            1), key='lowerLimit', pyvar=ciMean)
        processRet(ciMean_upperLimit_tmp, shape=(
            1), key='upperLimit', pyvar=ciMean)
    if not (stdDev is None):
        processRet(stdDev_stdDev_tmp, shape=(1), pyvar=stdDev)
    if not (tTest is None):
        processRet(tTest_df_tmp, shape=(1), key='df', pyvar=tTest)
        processRet(tTest_t_tmp, shape=(1), key='t', pyvar=tTest)
        processRet(tTest_pValue_tmp, shape=(1), key='pValue', pyvar=tTest)
    if not (ciVariance is None):
        processRet(ciVariance_lowerLimit_tmp, shape=(
            1), key='lowerLimit', pyvar=ciVariance)
        processRet(ciVariance_upperLimit_tmp, shape=(
            1), key='upperLimit', pyvar=ciVariance)
    if not (chiSquaredTest is None):
        processRet(chiSquaredTest_df_tmp, shape=(
            1), key='df', pyvar=chiSquaredTest)
        processRet(chiSquaredTest_chiSquared_tmp, shape=(
            1), key='chiSquared', pyvar=chiSquaredTest)
        processRet(chiSquaredTest_pValue_tmp, shape=(
            1), key='pValue', pyvar=chiSquaredTest)
    return result
