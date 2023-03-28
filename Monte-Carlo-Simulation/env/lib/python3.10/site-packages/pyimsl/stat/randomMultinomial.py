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
from numpy import dtype, float32, shape
from ctypes import POINTER, c_int, c_void_p

imslstat = loadimsl(STAT)


def randomMultinomial(nRandom, n, p):
    """ Generates pseudorandom numbers from a multinomial distribution.
    """
    imslstat.imsls_random_multinomial.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_random_multinomial('
    evalstring += 'c_int(nRandom)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(k)'
    evalstring += ','
    p = toNumpyArray(p, 'p', shape=shape, dtype='float32', expectedShape=(0))
    evalstring += 'p.ctypes.data_as(c_void_p)'
    k = shape[0]
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nRandom, k), result=True)
