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
from pyimsl.stat.statStructs import Imsls_d_nb_classifier
from pyimsl.util.CnlState import CnlState
from pyimsl.util.VersionFacade import VersionFacade
from numpy import array, empty
from ctypes import *

# Print levels
NONE = 0
FINAL = 1
TRACE_GEN = 2
TRACE_ALL = 3
DATA_WARNINGS = 4

# Types of distribution
GAUSSIAN = 0
LOG_NORMAL = 1
GAMMA = 2
POISSON = 3
USER = 5

IMSLS_CONTINUOUS = 10950
IMSLS_NOMINAL = 50701
IMSLS_PRINT_LEVEL = 20530
IMSLS_IGNORE_MISSING_VALUE_PATTERNS = 50517
IMSLS_DISCRETE_SMOOTHING_PARM = 50500
IMSLS_CONTINUOUS_SMOOTHING_PARM = 50501
IMSLS_ZERO_CORRECTION = 50502
IMSLS_SELECTED_PDF = 50503
IMSLS_GAUSSIAN_PDF = 50506
IMSLS_LOG_NORMAL_PDF = 50508
IMSLS_GAMMA_PDF = 50507
IMSLS_POISSON_PDF = 50509
IMSLS_USER_PDF = 50504
IMSLS_USER_PDF_WITH_PARMS = 50505
IMSLS_STATISTICS = 14780
IMSLS_PREDICTED_CLASS = 40612
IMSLS_PREDICTED_CLASS_PROB = 40618
IMSLS_CLASS_ERROR = 40614
IMSLS_COUNT_TABLE = 50514
IMSLS_NB_CLASSIFIER = 50518
imslstat = loadimsl(STAT)


def naiveBayesTrainer(nClasses, classification, continuous=None, nominal=None, printLevel=None,
                      ignoreMissingValuePatterns=None, discreteSmoothingParm=None, continuousSmoothingParm=None,
                      zeroCorrection=None, selectedPdf=None, gaussianPdf=None, logNormalPdf=None, gammaPdf=None,
                      poissonPdf=None, userPdf=None, statistics=None, predictedClass=None, predictedClassProb=None,
                      classError=None, countTable=None, nbClassifier=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_naive_bayes_trainer.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_d_naive_bayes_trainer('
    evalstring += 'c_int(nPatterns)'
    evalstring += ','
    evalstring += 'c_int(nClasses)'
    evalstring += ','
    classification = toNumpyArray(
        classification, 'classification', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'classification.ctypes.data_as(c_void_p)'
    nPatterns = shape[0]
    if not (continuous is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONTINUOUS)
        evalstring += ','
        evalstring += 'c_int(continuous_nContinuous_tmp)'
        evalstring += ','
        continuous_continuous_tmp = toNumpyArray(
            continuous, 'continuous', shape=shape, dtype='double', expectedShape=(nPatterns, 0))
        evalstring += 'continuous_continuous_tmp.ctypes.data_as(c_void_p)'
        continuous_nContinuous_tmp = shape[1]
    if not (nominal is None):
        evalstring += ','
        evalstring += repr(IMSLS_NOMINAL)
        checkForDict(nominal, 'nominal', ['nCategories', 'nominal'])
        evalstring += ','
        evalstring += 'c_int(nominal_nNominal_tmp)'
        evalstring += ','
        nominal_nCategories_tmp = nominal['nCategories']
        nominal_nCategories_tmp = toNumpyArray(
            nominal_nCategories_tmp, 'nCategories', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'nominal_nCategories_tmp.ctypes.data_as(c_void_p)'
        nominal_nNominal_tmp = shape[0]
        evalstring += ','
        nominal_nominal_tmp = nominal['nominal']
        nominal_nominal_tmp = toNumpyArray(
            nominal_nominal_tmp, 'nominal', shape=shape, dtype='int', expectedShape=(nPatterns, nominal_nNominal_tmp))
        evalstring += 'nominal_nominal_tmp.ctypes.data_as(c_void_p)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    checkForBoolean(ignoreMissingValuePatterns, 'ignoreMissingValuePatterns')
    if (ignoreMissingValuePatterns):
        evalstring += ','
        evalstring += repr(IMSLS_IGNORE_MISSING_VALUE_PATTERNS)
    if not (discreteSmoothingParm is None):
        evalstring += ','
        evalstring += repr(IMSLS_DISCRETE_SMOOTHING_PARM)
        evalstring += ','
        evalstring += 'c_double(discreteSmoothingParm)'
    if not (continuousSmoothingParm is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONTINUOUS_SMOOTHING_PARM)
        evalstring += ','
        evalstring += 'c_double(continuousSmoothingParm)'
    if not (zeroCorrection is None):
        evalstring += ','
        evalstring += repr(IMSLS_ZERO_CORRECTION)
        evalstring += ','
        evalstring += 'c_double(zeroCorrection)'
    if not (selectedPdf is None):
        evalstring += ','
        evalstring += repr(IMSLS_SELECTED_PDF)
        evalstring += ','
        selectedPdf = toNumpyArray(selectedPdf, 'selectedPdf', shape=shape,
                                   dtype='int', expectedShape=(continuous_nContinuous_tmp))
        evalstring += 'selectedPdf.ctypes.data_as(c_void_p)'
    if not (gaussianPdf is None):
        evalstring += ','
        evalstring += repr(IMSLS_GAUSSIAN_PDF)
        checkForDict(gaussianPdf, 'gaussianPdf', ['means', 'stdev'])
        evalstring += ','
        gaussianPdf_means_tmp = gaussianPdf['means']
        gaussianPdf_means_tmp = toNumpyArray(
            gaussianPdf_means_tmp, 'means', shape=shape, dtype='double', expectedShape=(0, nClasses))
        evalstring += 'gaussianPdf_means_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        gaussianPdf_stdev_tmp = gaussianPdf['stdev']
        gaussianPdf_stdev_tmp = toNumpyArray(
            gaussianPdf_stdev_tmp, 'stdev', shape=shape, dtype='double', expectedShape=(0, nClasses))
        evalstring += 'gaussianPdf_stdev_tmp.ctypes.data_as(c_void_p)'
    if not (logNormalPdf is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOG_NORMAL_PDF)
        checkForDict(logNormalPdf, 'logNormalPdf', ['logmean', 'logstdev'])
        evalstring += ','
        logNormalPdf_logmean_tmp = logNormalPdf['logmean']
        logNormalPdf_logmean_tmp = toNumpyArray(
            logNormalPdf_logmean_tmp, 'logmean', shape=shape, dtype='double', expectedShape=(0, nClasses))
        evalstring += 'logNormalPdf_logmean_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        logNormalPdf_logstdev_tmp = logNormalPdf['logstdev']
        logNormalPdf_logstdev_tmp = toNumpyArray(
            logNormalPdf_logstdev_tmp, 'logstdev', shape=shape, dtype='double', expectedShape=(0, nClasses))
        evalstring += 'logNormalPdf_logstdev_tmp.ctypes.data_as(c_void_p)'
    if not (gammaPdf is None):
        evalstring += ','
        evalstring += repr(IMSLS_GAMMA_PDF)
        checkForDict(gammaPdf, 'gammaPdf', ['a', 'b'])
        evalstring += ','
        gammaPdf_a_tmp = gammaPdf['a']
        gammaPdf_a_tmp = toNumpyArray(
            gammaPdf_a_tmp, 'a', shape=shape, dtype='double', expectedShape=(0, nClasses))
        evalstring += 'gammaPdf_a_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        gammaPdf_b_tmp = gammaPdf['b']
        gammaPdf_b_tmp = toNumpyArray(
            gammaPdf_b_tmp, 'b', shape=shape, dtype='double', expectedShape=(0, nClasses))
        evalstring += 'gammaPdf_b_tmp.ctypes.data_as(c_void_p)'
    if not (poissonPdf is None):
        evalstring += ','
        evalstring += repr(IMSLS_POISSON_PDF)
        evalstring += ','
        poissonPdf = toNumpyArray(
            poissonPdf, 'poissonPdf', shape=shape, dtype='double', expectedShape=(0, nClasses))
        evalstring += 'poissonPdf.ctypes.data_as(c_void_p)'
    if not (userPdf is None):
        evalstring += ','
        evalstring += repr(IMSLS_USER_PDF)
        evalstring += ','
        checkForCallable(pdf, 'pdf')
        TMP_USERPDF_PDF = CFUNCTYPE(c_double, POINTER(c_int), c_double)
        tmp_userPdf_pdf = TMP_USERPDF_PDF(pdf)
        evalstring += 'tmp_userPdf_pdf'
    if not (statistics is None):
        evalstring += ','
        evalstring += repr(IMSLS_STATISTICS)
        checkForDict(statistics, 'statistics', [])
        evalstring += ','
        statistics_means_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(statistics_means_tmp)'
        evalstring += ','
        statistics_stdev_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(statistics_stdev_tmp)'
    if not (predictedClass is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED_CLASS)
        checkForList(predictedClass, 'predictedClass')
        evalstring += ','
        predictedClass_predictedClass_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(predictedClass_predictedClass_tmp)'
    if not (predictedClassProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED_CLASS_PROB)
        checkForList(predictedClassProb, 'predictedClassProb')
        evalstring += ','
        predictedClassProb_predClassProb_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(predictedClassProb_predClassProb_tmp)'
    if not (classError is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_ERROR)
        checkForList(classError, 'classError')
        evalstring += ','
        classError_classError_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(classError_classError_tmp)'
    if not (countTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_COUNT_TABLE)
        checkForList(countTable, 'countTable')
        evalstring += ','
        countTable_countTable_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(countTable_countTable_tmp)'
    if not (nbClassifier is None):
        evalstring += ','
        evalstring += repr(IMSLS_NB_CLASSIFIER)
        checkForList(nbClassifier, 'nbClassifier')
        evalstring += ','
        nbClassifier_nbClassifier_tmp = POINTER(
            Imsls_d_nb_classifier)(Imsls_d_nb_classifier())
        evalstring += 'byref(nbClassifier_nbClassifier_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (statistics is None):
        processRet(statistics_means_tmp, shape=(
            continuous_nContinuous_tmp, nClasses), key='means', pyvar=statistics)
        processRet(statistics_stdev_tmp, shape=(
            continuous_nContinuous_tmp, nClasses), key='stdev', pyvar=statistics)
    if not (predictedClass is None):
        processRet(predictedClass_predictedClass_tmp,
                   shape=(nPatterns), pyvar=predictedClass)
    if not (predictedClassProb is None):
        processRet(predictedClassProb_predClassProb_tmp, shape=(
            nPatterns, nClasses), pyvar=predictedClassProb)
    if not (classError is None):
        processRet(classError_classError_tmp,
                   shape=(nPatterns), pyvar=classError)
    if not (countTable is None):
        m = nominal_nNominal_tmp - 1
        sumNCategories = 0
        for i in range(0, nominal_nCategories_tmp):
            sumNCategories += nominal_nCategories_tmp[i]
        ySize = nClasses + (nClasses * sumNCategories)
        processRet(countTable_countTable_tmp, shape=(
            m + 1, ySize), pyvar=countTable)
    if not (nbClassifier is None):
        nbClassifier[:] = []
        nbClassifierState = CnlState(nbClassifier_nbClassifier_tmp)
        nbClassifier.append(nbClassifierState)
    return processRet(result, shape=(nClasses + 1, 2), result=True)
