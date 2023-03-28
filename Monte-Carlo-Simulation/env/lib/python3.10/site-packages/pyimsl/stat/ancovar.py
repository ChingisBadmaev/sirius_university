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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_N_MISSING = 13440
IMSLS_ADJ_ANOVA = 50613
IMSLS_PARALLEL_TESTS = 50615
IMSLS_XYMEAN = 50619
IMSLS_COEF = 20448
IMSLS_COEF_TABLES = 50627
IMSLS_REG_ANOVA = 50625
IMSLS_R_MATRIX = 50617
IMSLS_COV_MEANS = 50621
IMSLS_COV_COEF = 50623
imslstat = loadimsl(STAT)


def ancovar(ni, y, x, nMissing=None, adjAnova=None, parallelTests=None, xymean=None, coef=None, coefTables=None, regAnova=None, rMatrix=None, covMeans=None, covCoef=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ancovar.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_ancovar('
    evalstring += 'c_int(ngroup)'
    evalstring += ','
    evalstring += 'c_int(ncov)'
    evalstring += ','
    ni = toNumpyArray(ni, 'ni', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'ni.ctypes.data_as(c_void_p)'
    ngroup = shape[0]
    evalstring += ','
    ySize = 0
    for i in range(0, ngroup):
        ySize += ni[i]
    n = ySize
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(ySize))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(n, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    ncov = shape[1]
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nmiss_tmp = c_int()
        evalstring += 'byref(nMissing_nmiss_tmp)'
    if not (adjAnova is None):
        evalstring += ','
        evalstring += repr(IMSLS_ADJ_ANOVA)
        checkForList(adjAnova, 'adjAnova')
        evalstring += ','
        adjAnova_adjAov_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(adjAnova_adjAov_tmp)'
    if not (parallelTests is None):
        evalstring += ','
        evalstring += repr(IMSLS_PARALLEL_TESTS)
        checkForList(parallelTests, 'parallelTests')
        evalstring += ','
        parallelTests_testpl_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(parallelTests_testpl_tmp)'
    if not (xymean is None):
        evalstring += ','
        evalstring += repr(IMSLS_XYMEAN)
        checkForList(xymean, 'xymean')
        evalstring += ','
        xymean_xymean_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xymean_xymean_tmp)'
    if not (coef is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF)
        checkForList(coef, 'coef')
        evalstring += ','
        coef_coef_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coef_coef_tmp)'
    if not (coefTables is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_TABLES)
        checkForList(coefTables, 'coefTables')
        evalstring += ','
        coefTables_coefTables_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefTables_coefTables_tmp)'
    if not (regAnova is None):
        evalstring += ','
        evalstring += repr(IMSLS_REG_ANOVA)
        checkForList(regAnova, 'regAnova')
        evalstring += ','
        regAnova_aovTables_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(regAnova_aovTables_tmp)'
    if not (rMatrix is None):
        evalstring += ','
        evalstring += repr(IMSLS_R_MATRIX)
        checkForList(rMatrix, 'rMatrix')
        evalstring += ','
        rMatrix_r_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(rMatrix_r_tmp)'
    if not (covMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV_MEANS)
        checkForList(covMeans, 'covMeans')
        evalstring += ','
        covMeans_covm_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(covMeans_covm_tmp)'
    if not (covCoef is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV_COEF)
        checkForList(covCoef, 'covCoef')
        evalstring += ','
        covCoef_covb_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(covCoef_covb_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nMissing is None):
        processRet(nMissing_nmiss_tmp, shape=(1), pyvar=nMissing)
    if not (adjAnova is None):
        processRet(adjAnova_adjAov_tmp, shape=(8), pyvar=adjAnova)
    if not (parallelTests is None):
        processRet(parallelTests_testpl_tmp, shape=(10), pyvar=parallelTests)
    if not (xymean is None):
        processRet(xymean_xymean_tmp, shape=(
            ngroup + 1, ncov + 3), pyvar=xymean)
    if not (coef is None):
        processRet(coef_coef_tmp, shape=(ngroup + ncov, 4), pyvar=coef)
    if not (coefTables is None):
        processRet(coefTables_coefTables_tmp, shape=(
            ngroup, ncov + 1, 4), pyvar=coefTables)
    if not (regAnova is None):
        processRet(regAnova_aovTables_tmp, shape=(ngroup, 15), pyvar=regAnova)
    if not (rMatrix is None):
        processRet(rMatrix_r_tmp, shape=(
            ngroup + ncov, ngroup + ncov), pyvar=rMatrix)
    if not (covMeans is None):
        processRet(covMeans_covm_tmp, shape=(ngroup, ngroup), pyvar=covMeans)
    if not (covCoef is None):
        processRet(covCoef_covb_tmp, shape=(
            ngroup + ncov, ngroup + ncov), pyvar=covCoef)
    return processRet(result, shape=(15), result=True)
