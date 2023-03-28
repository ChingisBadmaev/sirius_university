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
from pyimsl.util.imslUtils import MATH, complexConvert, d_complex, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, c_double, c_int
from .mathStructs import d_complex
from .mathStructs import d_complex

imslmath = loadimsl(MATH)


def besselYx(xnu, z, n):
    """ Evaluates a sequence of Bessel functions of the second kind with real order and complex arguments.
    """
    imslmath.imsl_z_bessel_Yx.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_bessel_Yx('
    evalstring += 'c_double(xnu)'
    evalstring += ','
    evalstring += 'z'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ',0)'
    z = complexConvert(z, toDComplex=True)
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(n), result=True)
