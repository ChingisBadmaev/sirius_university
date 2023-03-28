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
from pyimsl.util.VersionFacade import VersionFacade
from numpy import array, empty
from ctypes import *

# Print levels
NONE = 0
FINAL = 1
TRACE_GEN = 2
TRACE_ALL = 3
DATA_WARNINGS = 4

IMSLS_NOMINAL = 50701
IMSLS_CONTINUOUS = 10950
IMSLS_PRINT_LEVEL = 20530
IMSLS_USER_PDF = 50504
IMSLS_USER_PDF_WITH_PARMS = 50505
IMSLS_PREDICTED_CLASS_PROB = 40618
imslstat = loadimsl(STAT)


def naiveBayesClassification(nbClassifier, nPatterns, nominal=None, continuous=None, printLevel=None,
                             userPdf=None, predictedClassProb=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_naive_bayes_classification.restype = POINTER(c_int)
    shape = []
    nbClassifierState = nbClassifier[0].state
    evalstring = 'imslstat.imsls_d_naive_bayes_classification('
    evalstring += 'nbClassifierState'
    evalstring += ','
    evalstring += 'c_int(nPatterns)'
    if not (nominal is None):
        evalstring += ','
        evalstring += repr(IMSLS_NOMINAL)
        evalstring += ','
        n_nominal = nbClassifierState[0].n_nominal
        nominal = toNumpyArray(nominal, 'nominal', shape=shape,
                               dtype='int', expectedShape=(nPatterns, n_nominal))
        evalstring += 'nominal.ctypes.data_as(c_void_p)'
    if not (continuous is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONTINUOUS)
        evalstring += ','
        n_continuous = nbClassifierState[0].n_continuous
        continuous = toNumpyArray(continuous, 'continuous', shape=shape,
                                  dtype='double', expectedShape=(nPatterns, n_continuous))
        evalstring += 'continuous.ctypes.data_as(c_void_p)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (userPdf is None):
        evalstring += ','
        evalstring += repr(IMSLS_USER_PDF)
        evalstring += ','
        checkForCallable(pdf, 'pdf')
        TMP_USERPDF_PDF = CFUNCTYPE(c_double, POINTER(c_int), c_double)
        tmp_userPdf_pdf = TMP_USERPDF_PDF(pdf)
        evalstring += 'tmp_userPdf_pdf'
    if not (predictedClassProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED_CLASS_PROB)
        checkForList(predictedClassProb, 'predictedClassProb')
        evalstring += ','
        predictedClassProb_predClassProb_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(predictedClassProb_predClassProb_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (predictedClassProb is None):
        nClasses = nbClassifierState[0].n_classes
        processRet(predictedClassProb_predClassProb_tmp, shape=(
            nPatterns, nClasses), pyvar=predictedClassProb)
    return processRet(result, shape=(nPatterns), result=True)
