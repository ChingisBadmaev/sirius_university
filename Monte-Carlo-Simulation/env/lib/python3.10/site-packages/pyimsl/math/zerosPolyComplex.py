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
from numpy import dtype, shape
from ctypes import POINTER, c_int
from .mathStructs import d_complex
from .mathStructs import d_complex

imslmath = loadimsl(MATH)


def zerosPolyComplex(coef):
    """ Finds the zeros of a polynomial with complex coefficients using the Jenkins-Traub, three-stage algorithm.
    """
    imslmath.imsl_z_zeros_poly.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_zeros_poly('
    evalstring += 'c_int(ndeg)'
    evalstring += ','
    coef = toNumpyArray(coef, 'coef', shape=shape,
                        dtype='d_complex', expectedShape=(0))
    ndeg = shape[0] - 1
    evalstring += 'coef'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(ndeg), result=True)
