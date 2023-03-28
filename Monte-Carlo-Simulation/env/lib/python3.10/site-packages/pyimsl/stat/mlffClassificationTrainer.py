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
from .statStructs import Imsls_d_NN_Network
from pyimsl.util.VersionFacade import VersionFacade

# Weight initialization methods
EQUAL = 1
RANDOM = 2
PRINCIPAL_COMPONENTS = 3
DISCRIMINANT = 4

IMSLS_STAGE_I = 40609
IMSLS_NO_STAGE_II = 40610
IMSLS_MAX_STEP = 13070
IMSLS_MAX_ITN = 12980
IMSLS_MAX_FCN = 12940
IMSLS_REL_FCN_TOL = 14170
IMSLS_GRAD_TOL = 12070
IMSLS_TOLERANCE = 15040
IMSLS_PRINT = 13900
IMSLS_WEIGHT_INITIALIZATION_METHOD = 40616
IMSLS_LOGISTIC_TABLE = 40620
IMSLS_PREDICTED_CLASS = 40612
IMSLS_GRADIENT = 12050
IMSLS_PREDICTED_CLASS_PROB = 40618
IMSLS_CLASS_ERROR = 40614
imslstat = loadimsl(STAT)


def mlffClassificationTrainer(network, classification, nominal, continuous, stageI=None,
                              noStageII=None, maxStep=None, maxItn=None, maxFcn=None, relFcnTol=None, gradTol=None,
                              tolerance=None, t_print=None, weightInitializationMethod=None, logisticTable=None,
                              predictedClass=None, gradient=None, predictedClassProb=None, classError=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_mlff_classification_trainer.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_classification_trainer('
    evalstring += 'network'
    evalstring += ','
    evalstring += 'c_int(nPatterns)'
    evalstring += ','
    evalstring += 'c_int(nNominal)'
    evalstring += ','
    evalstring += 'c_int(nContinuous)'
    evalstring += ','
    classification = toNumpyArray(
        classification, 'classification', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'classification.ctypes.data_as(c_void_p)'
    nPatterns = shape[0]
    evalstring += ','
    # ++Custom code
    if not (nominal is None):
        nominal = toNumpyArray(
            nominal, 'nominal', shape=shape, dtype='int', expectedShape=(nPatterns, 0))
        evalstring += 'nominal.ctypes.data_as(c_void_p)'
        nNominal = shape[1]
    else:  # pass null if not supplied
        evalstring += 'None'
        nNominal = 0
    evalstring += ','
    if not (continuous is None):
        continuous = toNumpyArray(
            continuous, 'continuous', shape=shape, dtype='double', expectedShape=(nPatterns, 0))
        evalstring += 'continuous.ctypes.data_as(c_void_p)'
        nContinuous = shape[1]
    else:  # pass null if not supplied
        evalstring += 'None'
        nContinuous = 0
    layerNum = network[0].n_layers - 1
    nLinks = network[0].n_links
    nNodes = network[0].n_nodes
    nInputs = network[0].layers[0].nodes
    nOutputs = network[0].layers[layerNum].n_nodes
    # --Custom code
    if not (stageI is None):
        evalstring += ','
        evalstring += repr(IMSLS_STAGE_I)
        checkForDict(stageI, 'stageI', ['nEpochs', 'epochSize'])
        evalstring += ','
        stageI_nEpochs_tmp = stageI['nEpochs']
        evalstring += 'c_int(stageI_nEpochs_tmp)'
        evalstring += ','
        stageI_epochSize_tmp = stageI['epochSize']
        evalstring += 'c_int(stageI_epochSize_tmp)'
    checkForBoolean(noStageII, 'noStageII')
    if (noStageII):
        evalstring += ','
        evalstring += repr(IMSLS_NO_STAGE_II)
    if not (maxStep is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_STEP)
        evalstring += ','
        evalstring += 'c_double(maxStep)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    if not (relFcnTol is None):
        evalstring += ','
        evalstring += repr(IMSLS_REL_FCN_TOL)
        evalstring += ','
        evalstring += 'c_double(relFcnTol)'
    if not (gradTol is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRAD_TOL)
        evalstring += ','
        evalstring += 'c_double(gradTol)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    if not (weightInitializationMethod is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHT_INITIALIZATION_METHOD)
        evalstring += ','
        evalstring += 'c_int(weightInitializationMethod)'
    checkForBoolean(logisticTable, 'logisticTable')
    if (logisticTable):
        evalstring += ','
        evalstring += repr(IMSLS_LOGISTIC_TABLE)
    if not (predictedClass is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED_CLASS)
        checkForList(predictedClass, 'predictedClass')
        evalstring += ','
        predictedClass_predictedClass_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(predictedClass_predictedClass_tmp)'
    if not (gradient is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRADIENT)
        checkForList(gradient, 'gradient')
        evalstring += ','
        gradient_gradients_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(gradient_gradients_tmp)'
    if not (predictedClassProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED_CLASS_PROB)
        checkForList(predictedClassProb, 'predictedClassProb')
        evalstring += ','
        predictedClassProb_predictedClassProb_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(predictedClassProb_predictedClassProb_tmp)'
    if not (classError is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_ERROR)
        checkForList(classError, 'classError')
        evalstring += ','
        classError_classError_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(classError_classError_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (gradient is None):
        processRet(gradient_gradients_tmp, shape=(
            nLinks + nNodes - nInputs), pyvar=gradient)
    if not (predictedClass is None):
        processRet(predictedClass_predictedClass_tmp,
                   shape=(nPatterns), pyvar=predictedClass)
    if not (predictedClassProb is None):
        processRet(predictedClassProb_predictedClassProb_tmp, shape=(
            nPatterns, nOutputs), pyvar=predictedClassProb)
    if not (classError is None):
        processRet(classError_classError_tmp,
                   shape=(nPatterns), pyvar=classError)
    return processRet(result, shape=(6), result=True)
