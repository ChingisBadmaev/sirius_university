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
from numpy import double, dtype, int, shape, split
from ctypes import POINTER, byref, c_char_p, c_double, c_int, c_void_p

IMSLS_LOCATIONS = 40102
IMSLS_N_MISSING = 13440
IMSLS_CV = 40134
IMSLS_GRAND_MEAN = 40112
IMSLS_STRIP_PLOT_A_MEANS = 40209
IMSLS_STRIP_PLOT_B_MEANS = 40211
IMSLS_SPLIT_PLOT_MEANS = 40115
IMSLS_STRIP_PLOT_AB_MEANS = 40213
IMSLS_STRIP_PLOT_A_SPLIT_PLOT_MEANS = 40219
IMSLS_STRIP_PLOT_B_SPLIT_PLOT_MEANS = 40221
IMSLS_TREATMENT_MEANS = 40117
IMSLS_STD_ERRORS = 40120
IMSLS_N_BLOCKS = 40122
IMSLS_LOCATION_ANOVA_TABLE = 40142
IMSLS_ANOVA_ROW_LABELS = 40200
imslstat = loadimsl(STAT)


def stripSplitPlot(nLocations, nStripA, nStripB, nSplit, block, stripA, stripB, split, y, locations=None, nMissing=None, cv=None, grandMean=None, stripPlotAMeans=None, stripPlotBMeans=None, splitPlotMeans=None, stripPlotAbMeans=None, stripPlotASplitPlotMeans=None, stripPlotBSplitPlotMeans=None, treatmentMeans=None, stdErrors=None, nBlocks=None, locationAnovaTable=None, anovaRowLabels=None):
    """ Analyzes data from strip-split-plot experiments.
    """
    imslstat.imsls_d_strip_split_plot.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_strip_split_plot('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nLocations)'
    evalstring += ','
    evalstring += 'c_int(nStripA)'
    evalstring += ','
    evalstring += 'c_int(nStripB)'
    evalstring += ','
    evalstring += 'c_int(nSplit)'
    evalstring += ','
    block = toNumpyArray(block, 'block', shape=shape,
                         dtype='int', expectedShape=(0))
    evalstring += 'block.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    stripA = toNumpyArray(stripA, 'stripA', shape=shape,
                          dtype='int', expectedShape=(n))
    evalstring += 'stripA.ctypes.data_as(c_void_p)'
    evalstring += ','
    stripB = toNumpyArray(stripB, 'stripB', shape=shape,
                          dtype='int', expectedShape=(n))
    evalstring += 'stripB.ctypes.data_as(c_void_p)'
    evalstring += ','
    split = toNumpyArray(split, 'split', shape=shape,
                         dtype='int', expectedShape=(n))
    evalstring += 'split.ctypes.data_as(c_void_p)'
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
        cv_cv_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cv_cv_tmp)'
    if not (grandMean is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRAND_MEAN)
        checkForList(grandMean, 'grandMean')
        evalstring += ','
        grandMean_grandMean_tmp = c_double()
        evalstring += 'byref(grandMean_grandMean_tmp)'
    if not (stripPlotAMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRIP_PLOT_A_MEANS)
        checkForList(stripPlotAMeans, 'stripPlotAMeans')
        evalstring += ','
        stripPlotAMeans_stripPlotAMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stripPlotAMeans_stripPlotAMeans_tmp)'
    if not (stripPlotBMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRIP_PLOT_B_MEANS)
        checkForList(stripPlotBMeans, 'stripPlotBMeans')
        evalstring += ','
        stripPlotBMeans_stripPlotBMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stripPlotBMeans_stripPlotBMeans_tmp)'
    if not (splitPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_SPLIT_PLOT_MEANS)
        checkForList(splitPlotMeans, 'splitPlotMeans')
        evalstring += ','
        splitPlotMeans_splitPlotMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(splitPlotMeans_splitPlotMeans_tmp)'
    if not (stripPlotAbMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRIP_PLOT_AB_MEANS)
        checkForList(stripPlotAbMeans, 'stripPlotAbMeans')
        evalstring += ','
        stripPlotAbMeans_stripPlotAbMeans_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(stripPlotAbMeans_stripPlotAbMeans_tmp)'
    if not (stripPlotASplitPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRIP_PLOT_A_SPLIT_PLOT_MEANS)
        checkForList(stripPlotASplitPlotMeans, 'stripPlotASplitPlotMeans')
        evalstring += ','
        stripPlotASplitPlotMeans_stripPlotASplitPlotMeans_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(stripPlotASplitPlotMeans_stripPlotASplitPlotMeans_tmp)'
    if not (stripPlotBSplitPlotMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_STRIP_PLOT_B_SPLIT_PLOT_MEANS)
        checkForList(stripPlotBSplitPlotMeans, 'stripPlotBSplitPlotMeans')
        evalstring += ','
        stripPlotBSplitPlotMeans_stripPlotBSplitPlotMeans_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(stripPlotBSplitPlotMeans_stripPlotBSplitPlotMeans_tmp)'
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
    if not (stripPlotAMeans is None):
        processRet(stripPlotAMeans_stripPlotAMeans_tmp,
                   shape=(nStripA), pyvar=stripPlotAMeans)
    if not (stripPlotBMeans is None):
        processRet(stripPlotBMeans_stripPlotBMeans_tmp,
                   shape=(nStripB), pyvar=stripPlotBMeans)
    if not (splitPlotMeans is None):
        processRet(splitPlotMeans_splitPlotMeans_tmp,
                   shape=(nSplit), pyvar=splitPlotMeans)
    if not (stripPlotAbMeans is None):
        processRet(stripPlotAbMeans_stripPlotAbMeans_tmp,
                   shape=(nStripA, nStripB), pyvar=stripPlotAbMeans)
    if not (stripPlotASplitPlotMeans is None):
        processRet(stripPlotASplitPlotMeans_stripPlotASplitPlotMeans_tmp, shape=(
            nStripA, nSplit), pyvar=stripPlotASplitPlotMeans)
    if not (stripPlotBSplitPlotMeans is None):
        processRet(stripPlotBSplitPlotMeans_stripPlotBSplitPlotMeans_tmp, shape=(
            nStripB, nSplit), pyvar=stripPlotBSplitPlotMeans)
    if not (treatmentMeans is None):
        processRet(treatmentMeans_treatmentMeans_tmp, shape=(
            nStripA, nStripB, nSplit), pyvar=treatmentMeans)
    if not (stdErrors is None):
        processRet(stdErrors_stdErr_tmp, shape=(20), pyvar=stdErrors)
    if not (nBlocks is None):
        processRet(nBlocks_nBlocks_tmp, shape=(nLocations), pyvar=nBlocks)
    if not (locationAnovaTable is None):
        processRet(locationAnovaTable_locationAnovaTable_tmp,
                   shape=(nLocations, 22, 6), pyvar=locationAnovaTable)
    if not (anovaRowLabels is None):
        nAnova = 22
        processRet(anovaRowLabels_anovaRowLabels_tmp,
                   shape=(nAnova), pyvar=anovaRowLabels)
    return processRet(result, shape=(22, 6), result=True)
