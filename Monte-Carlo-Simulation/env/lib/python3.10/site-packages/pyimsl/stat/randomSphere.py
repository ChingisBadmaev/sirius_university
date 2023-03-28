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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, c_double, c_int

imslstat = loadimsl(STAT)


def randomSphere(nRandom, k):
    """ Generates pseudorandom points on a unit circle or K-dimensional sphere
    """
    imslstat.imsls_d_random_sphere.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_sphere('
    evalstring += 'c_int(nRandom)'
    evalstring += ','
    evalstring += 'c_int(k)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nRandom, k), result=True)
