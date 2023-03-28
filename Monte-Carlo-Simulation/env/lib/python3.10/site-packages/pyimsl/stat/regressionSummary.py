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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, byref, c_double, c_int
from .statStructs import Imsls_d_regression

IMSLS_INDEX_REGRESSION = 20941
IMSLS_COEF_T_TESTS = 10710
IMSLS_COEF_COL_DIM = 15600
IMSLS_COEF_VIF = 10730
IMSLS_COEF_COVARIANCES = 10690
IMSLS_COEF_COV_COL_DIM = 11060
IMSLS_ANOVA_TABLE = 10080
IMSLS_SQSS = 40519
imslstat = loadimsl(STAT)


def regressionSummary(regressionInfo, indexRegression=None, coefTTests=None, coefColDim=None, coefVif=None, coefCovariances=None, coefCovColDim=None, anovaTable=None, sqss=None):
    """ Produces summary statistics for a regression model given the information from the fit.
    """
    imslstat.imsls_d_regression_summary.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_regression_summary('
    evalstring += 'regressionInfo'
    if not (indexRegression is None):
        evalstring += ','
        evalstring += repr(IMSLS_INDEX_REGRESSION)
        evalstring += ','
        evalstring += 'c_int(indexRegression)'
    if not (coefTTests is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_T_TESTS)
        checkForList(coefTTests, 'coefTTests')
        evalstring += ','
        coefTTests_coefTTests_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefTTests_coefTTests_tmp)'
    if not (coefColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(coefColDim)'
    if not (coefVif is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_VIF)
        checkForList(coefVif, 'coefVif')
        evalstring += ','
        coefVif_coefVif_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefVif_coefVif_tmp)'
    if not (coefCovariances is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_COVARIANCES)
        checkForList(coefCovariances, 'coefCovariances')
        evalstring += ','
        coefCovariances_coefCovariances_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(coefCovariances_coefCovariances_tmp)'
    if not (coefCovColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEF_COV_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(coefCovColDim)'
    if not (anovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_TABLE)
        checkForList(anovaTable, 'anovaTable')
        evalstring += ','
        anovaTable_anovaTable_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(anovaTable_anovaTable_tmp)'
    if not (sqss is None):
        evalstring += ','
        evalstring += repr(IMSLS_SQSS)
        checkForList(sqss, 'sqss')
        evalstring += ','
        sqss_sqss_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(sqss_sqss_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    npar = regressionInfo[0].n_parameters
    if not (coefTTests is None):
        processRet(coefTTests_coefTTests_tmp,
                   shape=(npar, 4), pyvar=coefTTests)
    if not (coefVif is None):
        processRet(coefVif_coefVif_tmp, shape=(npar), pyvar=coefVif)
    if not (coefCovariances is None):
        processRet(coefCovariances_coefCovariances_tmp,
                   shape=(npar, npar), pyvar=coefCovariances)
    if not (anovaTable is None):
        processRet(anovaTable_anovaTable_tmp, shape=(15), pyvar=anovaTable)
    if not (sqss is None):
        processRet(sqss_sqss_tmp, shape=(npar, 4), pyvar=sqss)
    return
