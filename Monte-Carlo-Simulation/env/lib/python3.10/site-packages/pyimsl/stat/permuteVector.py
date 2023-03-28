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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape
from ctypes import POINTER, c_double, c_int, c_void_p

FORWARD_PERMUTATION = 1
BACKWARD_PERMUTATION = 2

imslstat = loadimsl(STAT)


def permuteVector(x, permutation, permute):
    """ Rearranges the elements of a vector as specified by a permutation.
    """
    imslstat.imsls_d_permute_vector.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_permute_vector('
    evalstring += 'c_int(nElements)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nElements = shape[0]
    evalstring += ','
    permutation = toNumpyArray(
        permutation, 'permutation', shape=shape, dtype='int', expectedShape=(nElements))
    evalstring += 'permutation.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(permute)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nElements), result=True)
