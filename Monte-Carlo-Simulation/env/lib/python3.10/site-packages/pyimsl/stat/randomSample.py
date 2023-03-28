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
from pyimsl.util.imslUtils import STAT, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, ndarray, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_FIRST_CALL = 40007
IMSLS_ADDITIONAL_CALL = 40009
IMSLS_POPULATION_COL_DIM = 40006
imslstat = loadimsl(STAT)


def randomSample(population, nsamp, firstCall=None, additionalCall=None, populationColDim=None):
    """ Generates a simple pseudorandom sample from a finite population.
    """
    imslstat.imsls_d_random_sample.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_sample('
    evalstring += 'c_int(nrow)'
    evalstring += ','
    evalstring += 'c_int(nvar)'
    evalstring += ','
    population = toNumpyArray(population, 'population',
                              shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'population.ctypes.data_as(c_void_p)'
    nrow = shape[0]
    nvar = shape[1]
    evalstring += ','
    evalstring += 'c_int(nsamp)'
    if not (firstCall is None):
        evalstring += ','
        evalstring += repr(IMSLS_FIRST_CALL)
        checkForDict(firstCall, 'firstCall', [])
        evalstring += ','
        firstCall_index_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(firstCall_index_tmp)'
        evalstring += ','
        firstCall_npop_tmp = c_int()
        evalstring += 'byref(firstCall_npop_tmp)'
    if not (additionalCall is None):
        evalstring += ','
        evalstring += repr(IMSLS_ADDITIONAL_CALL)
        checkForDict(additionalCall, 'additionalCall',
                     ['index', 'npop', 'samp'])
        evalstring += ','
        additionalCall_index_tmp = additionalCall['index']
        if (not(isinstance(additionalCall_index_tmp, ndarray))):
            additionalCall_index_tmp = toNumpyArray(
                additionalCall_index_tmp, 'index', shape=shape, dtype='int', expectedShape=(nsamp))
            additionalCall['index'] = additionalCall_index_tmp
        evalstring += 'additionalCall_index_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        additionalCall_npop_tmp = additionalCall['npop']
        if (not(isinstance(additionalCall_npop_tmp, c_int))):
            additionalCall_npop_tmp = c_int(additionalCall_npop_tmp)
            additionalCall['npop'] = additionalCall_npop_tmp
        evalstring += 'byref(additionalCall_npop_tmp)'
        evalstring += ','
        additionalCall_samp_tmp = additionalCall['samp']
        if (not(isinstance(additionalCall_samp_tmp, ndarray))):
            additionalCall_samp_tmp = toNumpyArray(
                additionalCall_samp_tmp, 'samp', shape=shape, dtype='double', expectedShape=(nsamp, nvar))
            additionalCall['samp'] = additionalCall_samp_tmp
        evalstring += 'additionalCall_samp_tmp.ctypes.data_as(c_void_p)'
    if not (populationColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_POPULATION_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(populationColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (firstCall is None):
        processRet(firstCall_index_tmp, shape=(nsamp),
                   key='index', pyvar=firstCall, createArray=True)
        processRet(firstCall_npop_tmp, shape=(1), key='npop', pyvar=firstCall)
    if(additionalCall is None):
        return processRet(result, shape=(nsamp, nvar), result=True)
