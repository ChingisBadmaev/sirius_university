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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import cov, double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_X_INDICES = 20443
IMSLS_METHOD = 13170
IMSLS_IDO = 20440
IMSLS_ROWS_ADD = 20441
IMSLS_ROWS_DELETE = 20442
IMSLS_PRIOR_EQUAL = 20460
IMSLS_PRIOR_PROPORTIONAL = 20444
IMSLS_PRIOR_INPUT = 20445
IMSLS_PRIOR_OUTPUT = 20446
IMSLS_GROUP_COUNTS = 12090
IMSLS_MEANS = 13120
IMSLS_COV = 20310
IMSLS_COEF = 20448
IMSLS_CLASS_MEMBERSHIP = 20450
IMSLS_CLASS_TABLE = 20452
IMSLS_PROB = 20458
IMSLS_MAHALANOBIS = 20454
IMSLS_STATS = 20456
IMSLS_N_ROWS_MISSING = 20400
imslstat = loadimsl(STAT)


def discriminantAnalysis(nRows, nVariables, x, nGroups, xColDim=None, xIndices=None, method=None, ido=None, rowsAdd=None, rowsDelete=None, priorEqual=None, priorProportional=None, priorInput=None, priorOutput=None, groupCounts=None, means=None, cov=None, coef=None, classMembership=None, classTable=None, prob=None, mahalanobis=None, stats=None, nRowsMissing=None):
    """ Performs a linear or a quadratic discriminant function analysis among several known groups.
    """
    imslstat.imsls_d_discriminant_analysis.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_discriminant_analysis('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    # 1-D array turn it into 1xnvariables+1
    # if(len(shape(x)) == 1 and len(x) == nVariables+1):
    #   x.resize(1,nVariables+1)
    extraXCols = 0
    if not (xIndices is None):
        checkForDict(xIndices, 'xIndices', ['igrp', 'ind', 'ifrq', 'iwt'])
        xIndices_ifrq_tmp = xIndices['ifrq']
        xIndices_iwt_tmp = xIndices['iwt']
        print("xIndices_ifrq_tmp = ", xIndices_ifrq_tmp)
        if xIndices_ifrq_tmp != (-1):
            extraXCols += 1
        if xIndices_iwt_tmp != (-1):
            extraXCols += 1

    x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                     expectedShape=(0, nVariables + 1 + extraXCols))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    # nRows=shape[0]
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
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
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
    checkForBoolean(priorEqual, 'priorEqual')
    if (priorEqual):
        evalstring += ','
        evalstring += repr(IMSLS_PRIOR_EQUAL)
    checkForBoolean(priorProportional, 'priorProportional')
    if (priorProportional):
        evalstring += ','
        evalstring += repr(IMSLS_PRIOR_PROPORTIONAL)
    if not (priorInput is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRIOR_INPUT)
        evalstring += ','
        priorInput = toNumpyArray(
            priorInput, 'priorInput', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'priorInput.ctypes.data_as(c_void_p)'
    if not (priorOutput is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRIOR_OUTPUT)
        checkForList(priorOutput, 'priorOutput')
        evalstring += ','
        priorOutput_priorOutput_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(priorOutput_priorOutput_tmp)'
    if not (groupCounts is None):
        evalstring += ','
        evalstring += repr(IMSLS_GROUP_COUNTS)
        checkForList(groupCounts, 'groupCounts')
        evalstring += ','
        groupCounts_groupCounts_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(groupCounts_groupCounts_tmp)'
    if not (means is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEANS)
        checkForList(means, 'means')
        evalstring += ','
        means_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(means_means_tmp)'
    if not (cov is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV)
        checkForList(cov, 'cov')
        evalstring += ','
        cov_cov_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cov_cov_tmp)'
    if not (coef is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF)
        checkForList(coef, 'coef')
        evalstring += ','
        coef_coef_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coef_coef_tmp)'
    if not (classMembership is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_MEMBERSHIP)
        checkForList(classMembership, 'classMembership')
        evalstring += ','
        classMembership_classMembership_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(classMembership_classMembership_tmp)'
    if not (classTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_TABLE)
        checkForList(classTable, 'classTable')
        evalstring += ','
        classTable_classTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(classTable_classTable_tmp)'
    if not (prob is None):
        evalstring += ','
        evalstring += repr(IMSLS_PROB)
        checkForList(prob, 'prob')
        evalstring += ','
        prob_prob_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(prob_prob_tmp)'
    if not (mahalanobis is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAHALANOBIS)
        checkForList(mahalanobis, 'mahalanobis')
        evalstring += ','
        mahalanobis_mahalanobis_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(mahalanobis_mahalanobis_tmp)'
    if not (stats is None):
        evalstring += ','
        evalstring += repr(IMSLS_STATS)
        checkForList(stats, 'stats')
        evalstring += ','
        stats_stats_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stats_stats_tmp)'
    if not (nRowsMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ROWS_MISSING)
        checkForList(nRowsMissing, 'nRowsMissing')
        evalstring += ','
        nRowsMissing_nRowsMissing_tmp = c_int()
        evalstring += 'byref(nRowsMissing_nRowsMissing_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (priorOutput is None):
        processRet(priorOutput_priorOutput_tmp,
                   shape=(nGroups), pyvar=priorOutput)
    if not (groupCounts is None):
        processRet(groupCounts_groupCounts_tmp,
                   shape=(nGroups), pyvar=groupCounts)
    if not (means is None):
        processRet(means_means_tmp, shape=(nGroups, nVariables), pyvar=means)
    if not (cov is None):
        if method == 3 or method == 6:
            shape = (nVariables, nVariables)
        else:
            shape = (nGroups + 1, nVariables, nVariables)
        processRet(cov_cov_tmp, shape=shape, pyvar=cov)
    if not (coef is None):
        processRet(coef_coef_tmp, shape=(nGroups, nVariables + 1), pyvar=coef)
    if not (classMembership is None):
        processRet(classMembership_classMembership_tmp,
                   shape=(nRows), pyvar=classMembership)
    if not (classTable is None):
        processRet(classTable_classTable_tmp, shape=(
            nGroups, nGroups), pyvar=classTable)
    if not (prob is None):
        processRet(prob_prob_tmp, shape=(nRows, nGroups), pyvar=prob)
    if not (mahalanobis is None):
        processRet(mahalanobis_mahalanobis_tmp, shape=(
            nGroups, nGroups), pyvar=mahalanobis)
    if not (stats is None):
        processRet(stats_stats_tmp, shape=(4 + 2 * (nGroups + 1)), pyvar=stats)
    if not (nRowsMissing is None):
        processRet(nRowsMissing_nRowsMissing_tmp, shape=1, pyvar=nRowsMissing)
    return
