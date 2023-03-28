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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, c_double, c_int

imslmath = loadimsl(MATH)


def randomBeta(nRandom, pin, qin):
    """ Generates pseudorandom numbers from a beta distribution.
    """
    imslmath.imsl_d_random_beta.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_random_beta('
    evalstring += 'c_int(nRandom)'
    evalstring += ','
    evalstring += 'c_double(pin)'
    evalstring += ','
    evalstring += 'c_double(qin)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(nRandom), result=True)
