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

IMSLS_LOGISTIC_TABLE = 40620
IMSLS_PREDICTED_CLASS = 40612
imslstat = loadimsl(STAT)


def mlffPatternClassification(network, nominal, continuous, logisticTable=None, predictedClass=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_mlff_pattern_classification.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_pattern_classification('
    evalstring += 'network'
    evalstring += ','
    evalstring += 'c_int(nPatterns)'
    evalstring += ','
    evalstring += 'c_int(nNominal)'
    evalstring += ','
    evalstring += 'c_int(nContinuous)'
    evalstring += ','
    if not (nominal is None):
        nominal = toNumpyArray(
            nominal, 'nominal', shape=shape, dtype='int', expectedShape=(0, 0))
        evalstring += 'nominal.ctypes.data_as(c_void_p)'
        nPatterns = shape[0]
        nNominal = shape[1]
    else:  # pass null if not supplied
        evalstring += 'None'
        nNominal = 0
    evalstring += ','
    if not (continuous is None):
        continuous = toNumpyArray(
            continuous, 'continuous', shape=shape, dtype='double', expectedShape=(0, 0))
        evalstring += 'continuous.ctypes.data_as(c_void_p)'
        nPatterns = shape[0]
        nContinuous = shape[1]
    else:  # pass null if not supplied
        evalstring += 'None'
        nContinuous = 0
    layerNum = network[0].n_layers - 1
    nLinks = network[0].n_links
    nNodes = network[0].n_nodes
    nInputs = network[0].layers[0].nodes
    nOutputs = network[0].layers[layerNum].n_nodes
    checkForBoolean(logisticTable, 'logisticTable')
    if (logisticTable):
        evalstring += ','
        evalstring += repr(IMSLS_LOGISTIC_TABLE)
    if not (predictedClass is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED_CLASS)
        checkForList(predictedClass, 'predictedClass')
        evalstring += ','
        predictedClass_predClass_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(predictedClass_predClass_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (predictedClass is None):
        processRet(predictedClass_predClass_tmp,
                   shape=(nPatterns), pyvar=predictedClass)
    if nOutputs == 1:  # binary classification so return nClasses=2
        nOutputs = 2
    return processRet(result, shape=(nPatterns, nOutputs), result=True)
