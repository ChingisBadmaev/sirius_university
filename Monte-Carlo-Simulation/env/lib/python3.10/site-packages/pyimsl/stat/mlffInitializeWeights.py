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

# types of method
EQUAL = 1
RANDOM = 2
PRINCIPAL_COMPONENTS = 3
DISCRIMINANT = 4

IMSLS_METHOD = 13170
IMSLS_PRINT = 13900
IMSLS_CLASSIFICATION = 40611
imslstat = loadimsl(STAT)


def mlffInitializeWeights(network, nominal, continuous, method=None, t_print=None, classification=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_mlff_initialize_weights.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_initialize_weights('
    evalstring += 'network'
    evalstring += ','
    evalstring += 'c_int(nPatterns)'
    evalstring += ','
    evalstring += 'c_int(nNominal)'
    evalstring += ','
    evalstring += 'c_int(nContinuous)'
    evalstring += ','
    if (not (method is None)) and (method == DISCRIMINANT):
        evalstring += 'None'
        nNominal = 0
    else:
        nominal = toNumpyArray(
            nominal, 'nominal', shape=shape, dtype='int', expectedShape=(0, 0))
        evalstring += 'nominal.ctypes.data_as(c_void_p)'
        nNominal = shape[1]
    evalstring += ','
    continuous = toNumpyArray(continuous, 'continuous',
                              shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'continuous.ctypes.data_as(c_void_p)'
    nContinuous = shape[1]
    nPatterns = shape[0]
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    if not (classification is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASSIFICATION)
        evalstring += ','
        classification = toNumpyArray(
            classification, 'classification', shape=shape, dtype='int', expectedShape=(nPatterns))
        evalstring += 'classification.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    nLinks = network[0].n_links
    nNodes = network[0].n_nodes
    nInputs = network[0].n_inputs
    return processRet(result, shape=(nLinks + nNodes - nInputs), result=True)
