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
from .statStructs import Imsls_d_kohonenSOM

IMSLS_RECTANGULAR = 16083
IMSLS_HEXAGONAL = 16084
IMSLS_VON_NEUMANN = 16085
IMSLS_MOORE = 16086
IMSLS_WRAP_AROUND = 16087
IMSLS_RANDOM_SEED = 50600
IMSLS_ITERATIONS = 20681
IMSLS_INITIAL_WEIGHTS = 16088
IMSLS_RECONSTRUCTION_ERROR = 16090
IMSLS_FCN_W_DATA = 40020
IMSLS_LCN_W_DATA = 16089
imslstat = loadimsl(STAT)


def kohonenSOMTrainer(fcn, lcn, nrow, ncol, data, rectangular=None, hexagonal=None, vonNeumann=None, moore=None, wrapAround=None, randomSeed=None, iterations=None, initialWeights=None, reconstructionError=None, fcnWData=None, lcnWData=None):
    """ Trains a Kohonen network.
    """
    # imslstat.imsls_d_kohonenSOM_trainer.restype = struct
    imslstat.imsls_d_kohonenSOM_trainer.restype = POINTER(Imsls_d_kohonenSOM)
    shape = []
    evalstring = 'imslstat.imsls_d_kohonenSOM_trainer('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_int, c_int, c_int, c_int, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    checkForCallable(lcn, 'lcn')
    TMP_LCN = CFUNCTYPE(c_double, c_int, c_int, c_int, c_int)
    tmp_lcn = TMP_LCN(lcn)
    evalstring += 'tmp_lcn'
    evalstring += ','
    evalstring += 'c_int(dim)'
    evalstring += ','
    evalstring += 'c_int(nrow)'
    evalstring += ','
    evalstring += 'c_int(ncol)'
    evalstring += ','
    evalstring += 'c_int(nobs)'
    evalstring += ','
    data = toNumpyArray(data, 'data', shape=shape,
                        dtype='double', expectedShape=(0, 0))
    evalstring += 'data.ctypes.data_as(c_void_p)'
    nobs = shape[0]
    dim = shape[1]
    checkForBoolean(rectangular, 'rectangular')
    if (rectangular):
        evalstring += ','
        evalstring += repr(IMSLS_RECTANGULAR)
    checkForBoolean(hexagonal, 'hexagonal')
    if (hexagonal):
        evalstring += ','
        evalstring += repr(IMSLS_HEXAGONAL)
    checkForBoolean(vonNeumann, 'vonNeumann')
    if (vonNeumann):
        evalstring += ','
        evalstring += repr(IMSLS_VON_NEUMANN)
    checkForBoolean(moore, 'moore')
    if (moore):
        evalstring += ','
        evalstring += repr(IMSLS_MOORE)
    checkForBoolean(wrapAround, 'wrapAround')
    if (wrapAround):
        evalstring += ','
        evalstring += repr(IMSLS_WRAP_AROUND)
    if not (randomSeed is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANDOM_SEED)
        evalstring += ','
        evalstring += 'c_int(randomSeed)'
    if not (iterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(iterations)'
    if not (initialWeights is None):
        evalstring += ','
        evalstring += repr(IMSLS_INITIAL_WEIGHTS)
        evalstring += ','
        initialWeights = toNumpyArray(initialWeights, 'initialWeights',
                                      shape=shape, dtype='double', expectedShape=(dim * nrow * ncol))
        evalstring += 'initialWeights.ctypes.data_as(c_void_p)'
    if not (reconstructionError is None):
        evalstring += ','
        evalstring += repr(IMSLS_RECONSTRUCTION_ERROR)
        checkForList(reconstructionError, 'reconstructionError')
        evalstring += ','
        reconstructionError_error_tmp = c_double()
        evalstring += 'byref(reconstructionError_error_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (reconstructionError is None):
        processRet(reconstructionError_error_tmp,
                   shape=(1), pyvar=reconstructionError)
    return result
