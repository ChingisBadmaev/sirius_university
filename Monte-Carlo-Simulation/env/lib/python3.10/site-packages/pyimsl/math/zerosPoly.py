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
from pyimsl.util.imslUtils import MATH, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_int, c_void_p
from .mathStructs import d_complex

imslmath = loadimsl(MATH)


def zerosPoly(coef):
    """ Finds the zeros of a polynomial with real coefficients using the Jenkins-Traub, three-stage algorithm.
    """
    imslmath.imsl_d_zeros_poly.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_d_zeros_poly('
    evalstring += 'c_int(ndeg)'
    evalstring += ','
    coef = toNumpyArray(coef, 'coef', shape=shape,
                        dtype='double', expectedShape=(0))
    ndeg = len(coef) - 1
    evalstring += 'coef.ctypes.data_as(c_void_p)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(ndeg), result=True)
