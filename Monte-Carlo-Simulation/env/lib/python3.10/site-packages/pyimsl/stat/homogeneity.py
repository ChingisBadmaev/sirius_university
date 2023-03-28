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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_LEVENES_MEAN = 40155
IMSLS_LEVENES_MEDIAN = 40156
IMSLS_N_MISSING = 13440
IMSLS_CV = 40134
IMSLS_GRAND_MEAN = 40112
IMSLS_TREATMENT_MEANS = 40117
IMSLS_RESIDUALS = 25570
IMSLS_STUDENTIZED_RESIDUALS = 40157
IMSLS_STD_DEVS = 14840
IMSLS_BARTLETTS = 40160
IMSLS_LEVENES = 40161
imslstat = loadimsl(STAT)


def homogeneity(nTreatment, treatment, y, levenesMean=None, levenesMedian=None, nMissing=None, cv=None, grandMean=None, treatmentMeans=None, residuals=None, studentizedResiduals=None, stdDevs=None, bartletts=None, levenes=None):
    """ Conducts Bartlett's and Levene's tests of the homogeneity of variance assumption in analysis of variance.
    """
    imslstat.imsls_d_homogeneity.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_homogeneity('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nTreatment)'
    evalstring += ','
    treatment = toNumpyArray(treatment, 'treatment',
                             shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'treatment.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(n))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    checkForBoolean(levenesMean, 'levenesMean')
    if (levenesMean):
        evalstring += ','
        evalstring += repr(IMSLS_LEVENES_MEAN)
    checkForBoolean(levenesMedian, 'levenesMedian')
    if (levenesMedian):
        evalstring += ','
        evalstring += repr(IMSLS_LEVENES_MEDIAN)
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nMissing_tmp = c_int()
        evalstring += 'byref(nMissing_nMissing_tmp)'
    if not (cv is None):
        evalstring += ','
        evalstring += repr(IMSLS_CV)
        checkForList(cv, 'cv')
        evalstring += ','
        cv_cv_tmp = c_double()
        evalstring += 'byref(cv_cv_tmp)'
    if not (grandMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRAND_MEAN)
        checkForList(grandMean, 'grandMean')
        evalstring += ','
        grandMean_grandMean_tmp = c_double()
        evalstring += 'byref(grandMean_grandMean_tmp)'
    if not (treatmentMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_TREATMENT_MEANS)
        checkForList(treatmentMeans, 'treatmentMeans')
        evalstring += ','
        treatmentMeans_treatmentMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(treatmentMeans_treatmentMeans_tmp)'
    if not (residuals is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUALS)
        checkForList(residuals, 'residuals')
        evalstring += ','
        residuals_residuals_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residuals_residuals_tmp)'
    if not (studentizedResiduals is None):
        evalstring += ','
        evalstring += repr(IMSLS_STUDENTIZED_RESIDUALS)
        checkForList(studentizedResiduals, 'studentizedResiduals')
        evalstring += ','
        studentizedResiduals_studentizedResiduals_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(studentizedResiduals_studentizedResiduals_tmp)'
    if not (stdDevs is None):
        evalstring += ','
        evalstring += repr(IMSLS_STD_DEVS)
        checkForList(stdDevs, 'stdDevs')
        evalstring += ','
        stdDevs_stdDevs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stdDevs_stdDevs_tmp)'
    if not (bartletts is None):
        evalstring += ','
        evalstring += repr(IMSLS_BARTLETTS)
        checkForList(bartletts, 'bartletts')
        evalstring += ','
        bartletts_bartletts_tmp = c_double()
        evalstring += 'byref(bartletts_bartletts_tmp)'
    if not (levenes is None):
        evalstring += ','
        evalstring += repr(IMSLS_LEVENES)
        checkForList(levenes, 'levenes')
        evalstring += ','
        levenes_levenes_tmp = c_double()
        evalstring += 'byref(levenes_levenes_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nMissing is None):
        processRet(nMissing_nMissing_tmp, shape=1, pyvar=nMissing)
    if not (cv is None):
        processRet(cv_cv_tmp, shape=1, pyvar=cv)
    if not (grandMean is None):
        processRet(grandMean_grandMean_tmp, shape=1, pyvar=grandMean)
    if not (treatmentMeans is None):
        processRet(treatmentMeans_treatmentMeans_tmp,
                   shape=(nTreatment), pyvar=treatmentMeans)
    if not (residuals is None):
        processRet(residuals_residuals_tmp, shape=(n), pyvar=residuals)
    if not (studentizedResiduals is None):
        processRet(studentizedResiduals_studentizedResiduals_tmp,
                   shape=(n), pyvar=studentizedResiduals)
    if not (stdDevs is None):
        processRet(stdDevs_stdDevs_tmp, shape=(nTreatment), pyvar=stdDevs)
    if not (bartletts is None):
        processRet(bartletts_bartletts_tmp, shape=1, pyvar=bartletts)
    if not (levenes is None):
        processRet(levenes_levenes_tmp, shape=1, pyvar=levenes)
    return processRet(result, shape=(2), result=True)
