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
from .statStructs import Imsls_d_svm_model

IMSLS_SVM_KERNEL_PRECOMPUTED = 50966
IMSLS_PREDICTED_CLASS_PROB = 40618
IMSLS_SVR_PROBABILITY = 50976
IMSLS_CLASS_ERROR = 40614
IMSLS_DECISION_VALUES = 50974
imslstat = loadimsl(STAT)


def supportVectorClassification(svmClassifier, x, svmKernelPrecomputed=None, predictedClassProb=None, svrProbability=None, classError=None, decisionValues=None):
    """ Classifies unknown patterns using a previously trained Support Vector Machines (SVM) model computed by support_vector_trainer.
    """
    imslstat.imsls_d_support_vector_classification.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_support_vector_classification('
    # svmClassifier = toNumpyArray(svmClassifier, 'svmClassifier', shape=shape, dtype='struct', expectedShape=(1))
    # evalstring +='svmClassifier.ctypes.data_as(c_void_p)'
    evalstring += 'svmClassifier'
    evalstring += ','
    evalstring += 'c_int(nPatterns)'
    evalstring += ','
    # custom code: Need the valaue of nAttributes from within the input structure.
    nAttributes = svmClassifier[0].param[0].n_attributes
    x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                     expectedShape=(0, nAttributes))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nPatterns = shape[0]
    if not (svmKernelPrecomputed is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_KERNEL_PRECOMPUTED)
        evalstring += ','
        svmKernelPrecomputed = toNumpyArray(
            svmKernelPrecomputed, 'svmKernelPrecomputed', shape=shape, dtype='double', expectedShape=(nPatterns, nPatterns))
        evalstring += 'svmKernelPrecomputed.ctypes.data_as(c_void_p)'
    if not (predictedClassProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED_CLASS_PROB)
        checkForList(predictedClassProb, 'predictedClassProb')
        evalstring += ','
        predictedClassProb_predClassProb_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(predictedClassProb_predClassProb_tmp)'
    if not (svrProbability is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVR_PROBABILITY)
        checkForList(svrProbability, 'svrProbability')
        evalstring += ','
        svrProbability_svrProbability_tmp = c_double()
        evalstring += 'byref(svrProbability_svrProbability_tmp)'
    if not (classError is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_ERROR)
        checkForDict(classError, 'classError', [
                     'classErrors', 'classification'])
        evalstring += ','
        classError_classification_tmp = classError['classification']
        classError_classification_tmp = toNumpyArray(
            classError_classification_tmp, 'classification', shape=shape, dtype='double', expectedShape=(nPatterns))
        evalstring += 'classError_classification_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        classError_classErrors_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(classError_classErrors_tmp)'
    if not (decisionValues is None):
        evalstring += ','
        evalstring += repr(IMSLS_DECISION_VALUES)
        checkForDict(decisionValues, 'decisionValues', ['i'])
        evalstring += ','
        decisionValues_i_tmp = decisionValues['i']
        evalstring += 'c_int(decisionValues_i_tmp)'
        evalstring += ','
        decisionValues_decValues_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(decisionValues_decValues_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    # custom code: Need the valaue of nClasses from within the input structure.
    nClasses = svmClassifier[0].nr_class
    if not (predictedClassProb is None):
        processRet(predictedClassProb_predClassProb_tmp, shape=(
            nPatterns, nClasses), pyvar=predictedClassProb)
    if not (svrProbability is None):
        processRet(svrProbability_svrProbability_tmp,
                   shape=(1), pyvar=svrProbability)
    if not (classError is None):
        processRet(classError_classErrors_tmp, shape=(
            (nClasses + 1), 2), key='classErrors', pyvar=classError)
    if not (decisionValues is None):
        # custom code: The length of decisionValues is determined by the value of type of classification model, which
        # is available from svmClassifier[0].param[0].svm_type.  The check below required access to the
        # CNL source code to determine the correct logic.
        length = nClasses * (nClasses - 1) / 2
        ONE_CLASS = 2
        EPSILON_SVR = 3
        NU_SVR = 4
        if ((svmClassifier[0].param[0].svm_type == ONE_CLASS)
            or (svmClassifier[0].param[0].svm_type == EPSILON_SVR)
                or (svmClassifier[0].param[0].svm_type == NU_SVR)):
            length = 1
        processRet(decisionValues_decValues_tmp, shape=length,
                   key='decValues', pyvar=decisionValues)
    return processRet(result, shape=(nPatterns), result=True)
