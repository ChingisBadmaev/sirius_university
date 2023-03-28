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
IMSLS_IDO = 20440
IMSLS_ROWS_ADD = 20441
IMSLS_ROWS_DELETE = 20442
IMSLS_GROUP_COUNTS = 12090
IMSLS_SUM_WEIGHTS = 20800
IMSLS_MEANS = 13120
IMSLS_U = 15180
IMSLS_N_ROWS_MISSING = 20400
imslstat = loadimsl(STAT)
# nRows needs to be input as it can be different than the first dim of x.
# def pooledCovariances (nVariables, x, nGroups, xColDim=None, xIndices=None, ido=None, rowsAdd=None, rowsDelete=None, groupCounts=None, sumWeights=None, means=None, u=None, nRowsMissing=None):


def pooledCovariances(nRows, nVariables, x, nGroups, xColDim=None, xIndices=None, ido=None, rowsAdd=None, rowsDelete=None, groupCounts=None, sumWeights=None, means=None, u=None, nRowsMissing=None):
    """ Compute a pooled variance-covariance from the observations.
    """
    imslstat.imsls_d_pooled_covariances.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_pooled_covariances('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                     expectedShape=(0, nVariables + 1))
    evalstring += 'x.ctypes.data_as(c_void_p)'
#    nRows=shape[0]
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
    if not (ido is None):
        evalstring += ','
        evalstring += repr(IMSLS_IDO)
        evalstring += ','
        evalstring += 'c_int(ido)'
    checkForBoolean(rowsAdd, 'rowsAdd')
    if (rowsAdd):
        evalstring += ','
        evalstring += repr(IMSLS_ROWS_ADD)
    checkForBoolean(rowsDelete, 'rowsDelete')
    if (rowsDelete):
        evalstring += ','
        evalstring += repr(IMSLS_ROWS_DELETE)
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
    if not (groupCounts is None):
        processRet(groupCounts_gcounts_tmp, shape=(nGroups), pyvar=groupCounts)
    if not (sumWeights is None):
        processRet(sumWeights_sumWeights_tmp,
                   shape=(nGroups), pyvar=sumWeights)
    if not (means is None):
        processRet(means_means_tmp, shape=(nGroups, nVariables), pyvar=means)
    if not (u is None):
        processRet(u_u_tmp, shape=(nVariables, nVariables), pyvar=u)
    if not (nRowsMissing is None):
        processRet(nRowsMissing_nrmiss_tmp, shape=(1), pyvar=nRowsMissing)
    return processRet(result, shape=(nVariables, nVariables), result=True)
