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
from numpy import double, dtype, int, shape, split
from ctypes import POINTER, byref, c_char_p, c_double, c_int, c_void_p

IMSLS_LOCATIONS = 40102
IMSLS_RCBD = 40103
IMSLS_CRD = 40104
IMSLS_N_MISSING = 13440
IMSLS_CV = 40134
IMSLS_GRAND_MEAN = 40112
IMSLS_WHOLE_PLOT_MEANS = 40113
IMSLS_SPLIT_PLOT_MEANS = 40115
IMSLS_SUB_PLOT_MEANS = 40140
IMSLS_WHOLE_SPLIT_PLOT_MEANS = 40146
IMSLS_WHOLE_SUB_PLOT_MEANS = 40148
IMSLS_SPLIT_SUB_PLOT_MEANS = 40150
IMSLS_TREATMENT_MEANS = 40117
IMSLS_STD_ERRORS = 40120
IMSLS_N_BLOCKS = 40122
IMSLS_LOCATION_ANOVA_TABLE = 40142
IMSLS_ANOVA_ROW_LABELS = 40200
imslstat = loadimsl(STAT)


def splitSplitPlot(nLocations, nWhole, nSplit, nSub, rep, whole, split, sub, y, locations=None, rcbd=None, crd=None, nMissing=None, cv=None, grandMean=None, wholePlotMeans=None, splitPlotMeans=None, subPlotMeans=None, wholeSplitPlotMeans=None, wholeSubPlotMeans=None, splitSubPlotMeans=None, treatmentMeans=None, stdErrors=None, nBlocks=None, locationAnovaTable=None, anovaRowLabels=None):
    """ Analyzes data from split-split-plot experiments.
    """
    imslstat.imsls_d_split_split_plot.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_split_split_plot('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nLocations)'
    evalstring += ','
    evalstring += 'c_int(nWhole)'
    evalstring += ','
    evalstring += 'c_int(nSplit)'
    evalstring += ','
    evalstring += 'c_int(nSub)'
    evalstring += ','
    rep = toNumpyArray(rep, 'rep', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'rep.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    whole = toNumpyArray(whole, 'whole', shape=shape,
                         dtype='int', expectedShape=(n))
    evalstring += 'whole.ctypes.data_as(c_void_p)'
    evalstring += ','
    split = toNumpyArray(split, 'split', shape=shape,
                         dtype='int', expectedShape=(n))
    evalstring += 'split.ctypes.data_as(c_void_p)'
    evalstring += ','
    sub = toNumpyArray(sub, 'sub', shape=shape, dtype='int', expectedShape=(n))
    evalstring += 'sub.ctypes.data_as(c_void_p)'
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
    checkForBoolean(rcbd, 'rcbd')
    if (rcbd):
        evalstring += ','
        evalstring += repr(IMSLS_RCBD)
    checkForBoolean(crd, 'crd')
    if (crd):
        evalstring += ','
        evalstring += repr(IMSLS_CRD)
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
        cv_cv_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cv_cv_tmp)'
    if not (grandMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRAND_MEAN)
        checkForList(grandMean, 'grandMean')
        evalstring += ','
        grandMean_grandMean_tmp = c_double()
        evalstring += 'byref(grandMean_grandMean_tmp)'
    if not (wholePlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLE_PLOT_MEANS)
        checkForList(wholePlotMeans, 'wholePlotMeans')
        evalstring += ','
        wholePlotMeans_wholePlotMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(wholePlotMeans_wholePlotMeans_tmp)'
    if not (splitPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_SPLIT_PLOT_MEANS)
        checkForList(splitPlotMeans, 'splitPlotMeans')
        evalstring += ','
        splitPlotMeans_splitPlotMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(splitPlotMeans_splitPlotMeans_tmp)'
    if not (subPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUB_PLOT_MEANS)
        checkForList(subPlotMeans, 'subPlotMeans')
        evalstring += ','
        subPlotMeans_subPlotMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(subPlotMeans_subPlotMeans_tmp)'
    if not (wholeSplitPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLE_SPLIT_PLOT_MEANS)
        checkForList(wholeSplitPlotMeans, 'wholeSplitPlotMeans')
        evalstring += ','
        wholeSplitPlotMeans_wholeSplitPlotMeans_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(wholeSplitPlotMeans_wholeSplitPlotMeans_tmp)'
    if not (wholeSubPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLE_SUB_PLOT_MEANS)
        checkForList(wholeSubPlotMeans, 'wholeSubPlotMeans')
        evalstring += ','
        wholeSubPlotMeans_wholeSubPlotMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(wholeSubPlotMeans_wholeSubPlotMeans_tmp)'
    if not (splitSubPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_SPLIT_SUB_PLOT_MEANS)
        checkForList(splitSubPlotMeans, 'splitSubPlotMeans')
        evalstring += ','
        splitSubPlotMeans_splitSubPlotMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(splitSubPlotMeans_splitSubPlotMeans_tmp)'
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
    if not (nBlocks is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_BLOCKS)
        checkForList(nBlocks, 'nBlocks')
        evalstring += ','
        nBlocks_nBlocks_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(nBlocks_nBlocks_tmp)'
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
        processRet(cv_cv_tmp, shape=(3), pyvar=cv)
    if not (grandMean is None):
        processRet(grandMean_grandMean_tmp, shape=1, pyvar=grandMean)
    if not (wholePlotMeans is None):
        processRet(wholePlotMeans_wholePlotMeans_tmp,
                   shape=(nWhole), pyvar=wholePlotMeans)
    if not (splitPlotMeans is None):
        processRet(splitPlotMeans_splitPlotMeans_tmp,
                   shape=(nSplit), pyvar=splitPlotMeans)
    if not (subPlotMeans is None):
        processRet(subPlotMeans_subPlotMeans_tmp,
                   shape=(nSub), pyvar=subPlotMeans)
    if not (wholeSplitPlotMeans is None):
        processRet(wholeSplitPlotMeans_wholeSplitPlotMeans_tmp,
                   shape=(nWhole, nSplit), pyvar=wholeSplitPlotMeans)
    if not (wholeSubPlotMeans is None):
        processRet(wholeSubPlotMeans_wholeSubPlotMeans_tmp,
                   shape=(nWhole, nSub), pyvar=wholeSubPlotMeans)
    if not (splitSubPlotMeans is None):
        processRet(splitSubPlotMeans_splitSubPlotMeans_tmp,
                   shape=(nSplit, nSub), pyvar=splitSubPlotMeans)
    if not (treatmentMeans is None):
        processRet(treatmentMeans_treatmentMeans_tmp, shape=(
            nWhole, nSplit, nSub), pyvar=treatmentMeans)
    if not (stdErrors is None):
        processRet(stdErrors_stdErr_tmp, shape=(8), pyvar=stdErrors)
    if not (nBlocks is None):
        processRet(nBlocks_nBlocks_tmp, shape=(nLocations), pyvar=nBlocks)
    if not (locationAnovaTable is None):
        processRet(locationAnovaTable_locationAnovaTable_tmp,
                   shape=(nLocations, 20, 6), pyvar=locationAnovaTable)
    if not (anovaRowLabels is None):
        nAnova = 20
        processRet(anovaRowLabels_anovaRowLabels_tmp,
                   shape=(nAnova), pyvar=anovaRowLabels)
    return processRet(result, shape=(20, 6), result=True)
