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
IMSLS_LOC_RANDOM = 40106
IMSLS_LOC_FIXED = 40105
IMSLS_RCBD = 40103
IMSLS_CRD = 40104
IMSLS_WHOLE_FIXED = 40107
IMSLS_WHOLE_RANDOM = 40108
IMSLS_SPLIT_FIXED = 40109
IMSLS_SPLIT_RANDOM = 40110
IMSLS_N_MISSING = 13440
IMSLS_CV = 40134
IMSLS_GRAND_MEAN = 40112
IMSLS_WHOLE_PLOT_MEANS = 40113
IMSLS_SPLIT_PLOT_MEANS = 40115
IMSLS_TREATMENT_MEANS = 40117
IMSLS_STD_ERRORS = 40120
IMSLS_N_BLOCKS = 40122
IMSLS_BLOCK_SS = 40124
IMSLS_WHOLE_PLOT_SS = 40126
IMSLS_SPLIT_PLOT_SS = 40128
IMSLS_WHOLEXSPLIT_PLOT_SS = 40138
IMSLS_WHOLE_PLOT_ERROR_SS = 40130
IMSLS_SPLIT_PLOT_ERROR_SS = 40132
IMSLS_TOTAL_SS = 40136
IMSLS_ANOVA_ROW_LABELS = 40200
imslstat = loadimsl(STAT)


def splitPlot(nLocations, nWhole, nSplit, rep, whole, split, y, locations=None, locRandom=None, locFixed=None, rcbd=None, crd=None, wholeFixed=None, wholeRandom=None, splitFixed=None, splitRandom=None, nMissing=None, cv=None, grandMean=None, wholePlotMeans=None, splitPlotMeans=None, treatmentMeans=None, stdErrors=None, nBlocks=None, blockSs=None, wholePlotSs=None, splitPlotSs=None, wholexsplitPlotSs=None, wholePlotErrorSs=None, splitPlotErrorSs=None, totalSs=None, anovaRowLabels=None):
    """ Analyzes a wide variety of split-plot experiments with fixed, mixed or random factors.
    """
    imslstat.imsls_d_split_plot.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_split_plot('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nLocations)'
    evalstring += ','
    evalstring += 'c_int(nWhole)'
    evalstring += ','
    evalstring += 'c_int(nSplit)'
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
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(n))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    if not (locations is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOCATIONS)
        evalstring += ','
        locations = toNumpyArray(
            locations, 'locations', shape=shape, dtype='int', expectedShape=(n))
        evalstring += 'locations.ctypes.data_as(c_void_p)'
    checkForBoolean(locRandom, 'locRandom')
    if (locRandom):
        evalstring += ','
        evalstring += repr(IMSLS_LOC_RANDOM)
    checkForBoolean(locFixed, 'locFixed')
    if (locFixed):
        evalstring += ','
        evalstring += repr(IMSLS_LOC_FIXED)
    checkForBoolean(rcbd, 'rcbd')
    if (rcbd):
        evalstring += ','
        evalstring += repr(IMSLS_RCBD)
    checkForBoolean(crd, 'crd')
    if (crd):
        evalstring += ','
        evalstring += repr(IMSLS_CRD)
    checkForBoolean(wholeFixed, 'wholeFixed')
    if (wholeFixed):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLE_FIXED)
    checkForBoolean(wholeRandom, 'wholeRandom')
    if (wholeRandom):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLE_RANDOM)
    checkForBoolean(splitFixed, 'splitFixed')
    if (splitFixed):
        evalstring += ','
        evalstring += repr(IMSLS_SPLIT_FIXED)
    checkForBoolean(splitRandom, 'splitRandom')
    if (splitRandom):
        evalstring += ','
        evalstring += repr(IMSLS_SPLIT_RANDOM)
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
    if not (blockSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_BLOCK_SS)
        checkForList(blockSs, 'blockSs')
        evalstring += ','
        blockSs_blockSs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(blockSs_blockSs_tmp)'
    if not (wholePlotSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLE_PLOT_SS)
        checkForList(wholePlotSs, 'wholePlotSs')
        evalstring += ','
        wholePlotSs_wholePlotSs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(wholePlotSs_wholePlotSs_tmp)'
    if not (splitPlotSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_SPLIT_PLOT_SS)
        checkForList(splitPlotSs, 'splitPlotSs')
        evalstring += ','
        splitPlotSs_splitPlotSs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(splitPlotSs_splitPlotSs_tmp)'
    if not (wholexsplitPlotSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLEXSPLIT_PLOT_SS)
        checkForList(wholexsplitPlotSs, 'wholexsplitPlotSs')
        evalstring += ','
        wholexsplitPlotSs_wholexsplitPlotSs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(wholexsplitPlotSs_wholexsplitPlotSs_tmp)'
    if not (wholePlotErrorSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_WHOLE_PLOT_ERROR_SS)
        checkForList(wholePlotErrorSs, 'wholePlotErrorSs')
        evalstring += ','
        wholePlotErrorSs_wholePlotErrorSs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(wholePlotErrorSs_wholePlotErrorSs_tmp)'
    if not (splitPlotErrorSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_SPLIT_PLOT_ERROR_SS)
        checkForList(splitPlotErrorSs, 'splitPlotErrorSs')
        evalstring += ','
        splitPlotErrorSs_splitPlotErrorSs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(splitPlotErrorSs_splitPlotErrorSs_tmp)'
    if not (totalSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOTAL_SS)
        checkForList(totalSs, 'totalSs')
        evalstring += ','
        totalSs_totalSs_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(totalSs_totalSs_tmp)'
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
        processRet(cv_cv_tmp, shape=(2), pyvar=cv)
    if not (grandMean is None):
        processRet(grandMean_grandMean_tmp, shape=1, pyvar=grandMean)
    if not (wholePlotMeans is None):
        processRet(wholePlotMeans_wholePlotMeans_tmp,
                   shape=(nWhole), pyvar=wholePlotMeans)
    if not (splitPlotMeans is None):
        processRet(splitPlotMeans_splitPlotMeans_tmp,
                   shape=(nSplit), pyvar=splitPlotMeans)
    if not (treatmentMeans is None):
        processRet(treatmentMeans_treatmentMeans_tmp,
                   shape=(nWhole, nSplit), pyvar=treatmentMeans)
    if not (stdErrors is None):
        processRet(stdErrors_stdErr_tmp, shape=(10), pyvar=stdErrors)
    if not (nBlocks is None):
        processRet(nBlocks_nBlocks_tmp, shape=(nLocations), pyvar=nBlocks)
    if not (blockSs is None):
        processRet(blockSs_blockSs_tmp, shape=(nLocations, 2), pyvar=blockSs)
    if not (wholePlotSs is None):
        processRet(wholePlotSs_wholePlotSs_tmp, shape=(
            nLocations, 2), pyvar=wholePlotSs)
    if not (splitPlotSs is None):
        processRet(splitPlotSs_splitPlotSs_tmp, shape=(
            nLocations, 2), pyvar=splitPlotSs)
    if not (wholexsplitPlotSs is None):
        processRet(wholexsplitPlotSs_wholexsplitPlotSs_tmp,
                   shape=(nLocations, 2), pyvar=wholexsplitPlotSs)
    if not (wholePlotErrorSs is None):
        processRet(wholePlotErrorSs_wholePlotErrorSs_tmp,
                   shape=(nLocations, 2), pyvar=wholePlotErrorSs)
    if not (splitPlotErrorSs is None):
        processRet(splitPlotErrorSs_splitPlotErrorSs_tmp,
                   shape=(nLocations, 2), pyvar=splitPlotErrorSs)
    if not (totalSs is None):
        processRet(totalSs_totalSs_tmp, shape=(nLocations, 2), pyvar=totalSs)
    if not (anovaRowLabels is None):
        nAnova = 11
        processRet(anovaRowLabels_anovaRowLabels_tmp,
                   shape=(nAnova), pyvar=anovaRowLabels)
    return processRet(result, shape=(11, 6), result=True)
