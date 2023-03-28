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
from numpy import double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_X_INDICES = 20443
IMSLS_INITIAL_EST_MEAN = 20830
IMSLS_INITIAL_EST_MEDIAN = 20840
IMSLS_INITIAL_EST_INPUT = 20210
IMSLS_ESTIMATION_METHOD = 25450
IMSLS_PERCENTAGE = 13720
IMSLS_MAX_ITERATIONS = 12970
IMSLS_TOLERANCE = 15040
IMSLS_MINIMAX_WEIGHTS = 20850
IMSLS_GROUP_COUNTS = 12090
IMSLS_SUM_WEIGHTS = 20800
IMSLS_MEANS = 13120
IMSLS_U = 15180
IMSLS_BETA = 20870
IMSLS_N_ROWS_MISSING = 20400
imslstat = loadimsl(STAT)


def robustCovariances(x, nGroups, xColDim=None, xIndices=None, initialEstMean=None, initialEstMedian=None, initialEstInput=None, estimationMethod=None, percentage=None, maxIterations=None, tolerance=None, minimaxWeights=None, groupCounts=None, sumWeights=None, means=None, u=None, beta=None, nRowsMissing=None):
    """ Computes a robust estimate of a covariance matrix and mean vector.
    """
    imslstat.imsls_d_robust_covariances.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_robust_covariances('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nVariables = shape[1] - 1
    evalstring += ','
    evalstring += 'c_int(nGroups)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (xIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INDICES)
        checkForDict(xIndices, 'xIndices', ['igrp', 'ind', 'ifrq', 'iwt'])
        evalstring += ','
        xIndices_igrp_tmp = xIndices['igrp']
        evalstring += 'c_int(xIndices_igrp_tmp)'
        evalstring += ','
        xIndices_ind_tmp = xIndices['ind']
        xIndices_ind_tmp = toNumpyArray(
            xIndices_ind_tmp, 'ind', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'xIndices_ind_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        xIndices_ifrq_tmp = xIndices['ifrq']
        evalstring += 'c_int(xIndices_ifrq_tmp)'
        evalstring += ','
        xIndices_iwt_tmp = xIndices['iwt']
        evalstring += 'c_int(xIndices_iwt_tmp)'
    checkForBoolean(initialEstMean, 'initialEstMean')
    if (initialEstMean):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_EST_MEAN)
    checkForBoolean(initialEstMedian, 'initialEstMedian')
    if (initialEstMedian):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_EST_MEDIAN)
    if not (initialEstInput is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_EST_INPUT)
        checkForDict(initialEstInput, 'initialEstInput',
                     ['inputMeans', 'inputCov'])
        evalstring += ','
        initialEstInput_inputMeans_tmp = initialEstInput['inputMeans']
        initialEstInput_inputMeans_tmp = toNumpyArray(
            initialEstInput_inputMeans_tmp, 'inputMeans', shape=shape, dtype='double', expectedShape=(nGroups, nVariables))
        evalstring += 'initialEstInput_inputMeans_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        initialEstInput_inputCov_tmp = initialEstInput['inputCov']
        initialEstInput_inputCov_tmp = toNumpyArray(
            initialEstInput_inputCov_tmp, 'inputCov', shape=shape, dtype='double', expectedShape=(nVariables, nVariables))
        evalstring += 'initialEstInput_inputCov_tmp.ctypes.data_as(c_void_p)'
    if not (estimationMethod is None):
        evalstring += ','
        evalstring += repr(IMSLS_ESTIMATION_METHOD)
        evalstring += ','
        evalstring += 'c_int(estimationMethod)'
    if not (percentage is None):
        evalstring += ','
        evalstring += repr(IMSLS_PERCENTAGE)
        evalstring += ','
        evalstring += 'c_double(percentage)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (minimaxWeights is None):
        evalstring += ','
        evalstring += repr(IMSLS_MINIMAX_WEIGHTS)
        checkForDict(minimaxWeights, 'minimaxWeights', [])
        evalstring += ','
        minimaxWeights_a_tmp = c_double()
        evalstring += 'byref(minimaxWeights_a_tmp)'
        evalstring += ','
        minimaxWeights_b_tmp = c_double()
        evalstring += 'byref(minimaxWeights_b_tmp)'
        evalstring += ','
        minimaxWeights_c_tmp = c_double()
        evalstring += 'byref(minimaxWeights_c_tmp)'
    if not (groupCounts is None):
        evalstring += ','
        evalstring += repr(IMSLS_GROUP_COUNTS)
        checkForList(groupCounts, 'groupCounts')
        evalstring += ','
        groupCounts_gcounts_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(groupCounts_gcounts_tmp)'
    if not (sumWeights is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUM_WEIGHTS)
        checkForList(sumWeights, 'sumWeights')
        evalstring += ','
        sumWeights_sumWeights_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(sumWeights_sumWeights_tmp)'
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEANS)
        checkForList(means, 'means')
        evalstring += ','
        means_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(means_means_tmp)'
    if not (u is None):
        evalstring += ','
        evalstring += repr(IMSLS_U)
        checkForList(u, 'u')
        evalstring += ','
        u_u_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(u_u_tmp)'
    if not (beta is None):
        evalstring += ','
        evalstring += repr(IMSLS_BETA)
        checkForList(beta, 'beta')
        evalstring += ','
        beta_beta_tmp = c_double()
        evalstring += 'byref(beta_beta_tmp)'
    if not (nRowsMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ROWS_MISSING)
        checkForList(nRowsMissing, 'nRowsMissing')
        evalstring += ','
        nRowsMissing_nrmiss_tmp = c_int()
        evalstring += 'byref(nRowsMissing_nrmiss_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (minimaxWeights is None):
        processRet(minimaxWeights_a_tmp, shape=(
            1), key='a', pyvar=minimaxWeights)
        processRet(minimaxWeights_b_tmp, shape=(
            1), key='b', pyvar=minimaxWeights)
        processRet(minimaxWeights_c_tmp, shape=(
            1), key='c', pyvar=minimaxWeights)
    if not (groupCounts is None):
        processRet(groupCounts_gcounts_tmp, shape=(nGroups), pyvar=groupCounts)
    if not (sumWeights is None):
        processRet(sumWeights_sumWeights_tmp,
                   shape=(nGroups), pyvar=sumWeights)
    if not (means is None):
        processRet(means_means_tmp, shape=(nGroups, nVariables), pyvar=means)
    if not (u is None):
        processRet(u_u_tmp, shape=(nVariables, nVariables), pyvar=u)
    if not (beta is None):
        processRet(beta_beta_tmp, shape=(1), pyvar=beta)
    if not (nRowsMissing is None):
        processRet(nRowsMissing_nrmiss_tmp, shape=(1), pyvar=nRowsMissing)
    return processRet(result, shape=(nVariables, nVariables), result=True)
