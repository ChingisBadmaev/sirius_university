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
from ctypes import POINTER, byref, c_char_p, c_double, c_int, c_void_p

IMSLS_LOCATIONS = 40102
IMSLS_N_MISSING = 13440
IMSLS_CV = 40134
IMSLS_GRAND_MEAN = 40112
IMSLS_TREATMENT_MEANS = 40117
IMSLS_STD_ERRORS = 40120
IMSLS_LOCATION_ANOVA_TABLE = 40142
IMSLS_ANOVA_ROW_LABELS = 40200
imslstat = loadimsl(STAT)


def latinSquare(nLocations, nTreatments, row, col, treatment, y, locations=None, nMissing=None, cv=None, grandMean=None, treatmentMeans=None, stdErrors=None, locationAnovaTable=None, anovaRowLabels=None):
    """ Analyzes data from latin-square experiments.
    """
    imslstat.imsls_d_latin_square.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_latin_square('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nLocations)'
    evalstring += ','
    evalstring += 'c_int(nTreatments)'
    evalstring += ','
    row = toNumpyArray(row, 'row', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'row.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    col = toNumpyArray(col, 'col', shape=shape, dtype='int', expectedShape=(n))
    evalstring += 'col.ctypes.data_as(c_void_p)'
    evalstring += ','
    treatment = toNumpyArray(treatment, 'treatment',
                             shape=shape, dtype='int', expectedShape=(n))
    evalstring += 'treatment.ctypes.data_as(c_void_p)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(n))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (locations is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOCATIONS)
        evalstring += ','
        locations = toNumpyArray(
            locations, 'locations', shape=shape, dtype='int', expectedShape=(n))
        evalstring += 'locations.ctypes.data_as(c_void_p)'
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
    if not (stdErrors is None):
        evalstring += ','
        evalstring += repr(IMSLS_STD_ERRORS)
        checkForList(stdErrors, 'stdErrors')
        evalstring += ','
        stdErrors_stdErr_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stdErrors_stdErr_tmp)'
    if not (locationAnovaTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOCATION_ANOVA_TABLE)
        checkForList(locationAnovaTable, 'locationAnovaTable')
        evalstring += ','
        locationAnovaTable_locationAnovaTable_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(locationAnovaTable_locationAnovaTable_tmp)'
    if not (anovaRowLabels is None):
        evalstring += ','
        evalstring += repr(IMSLS_ANOVA_ROW_LABELS)
        checkForList(anovaRowLabels, 'anovaRowLabels')
        evalstring += ','
        anovaRowLabels_anovaRowLabels_tmp = POINTER(c_char_p)(c_char_p())
        evalstring += 'byref(anovaRowLabels_anovaRowLabels_tmp)'
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
                   shape=(nTreatments), pyvar=treatmentMeans)
    if not (stdErrors is None):
        processRet(stdErrors_stdErr_tmp, shape=(2), pyvar=stdErrors)
    if not (locationAnovaTable is None):
        processRet(locationAnovaTable_locationAnovaTable_tmp,
                   shape=(nLocations, 7, 6), pyvar=locationAnovaTable)
    if not (anovaRowLabels is None):
        nAnova = 7
        processRet(anovaRowLabels_anovaRowLabels_tmp,
                   shape=(nAnova), pyvar=anovaRowLabels)
    return processRet(result, shape=(7, 6), result=True)
