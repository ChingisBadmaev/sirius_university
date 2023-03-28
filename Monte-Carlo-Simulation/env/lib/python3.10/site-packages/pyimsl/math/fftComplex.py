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
from pyimsl.util.imslUtils import MATH, checkForBoolean, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, ndarray
from ctypes import POINTER, c_int, c_void_p, c_double
from .mathStructs import d_complex
from .mathStructs import d_complex

IMSL_BACKWARD = 10008
IMSL_PARAMS = 10009
imslmath = loadimsl(MATH)


def fftComplex(p, backward=None, params=None):
    """ Computes the complex discrete Fourier transform of a complex sequence.
    """
    imslmath.imsl_z_fft_complex.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_fft_complex('
    evalstring += 'c_int(n)'
    evalstring += ','
    p = toNumpyArray(p, 'p', shape=shape, dtype='d_complex', expectedShape=(0))
    evalstring += 'p'
    n = shape[0]
    checkForBoolean(backward, 'backward')
    if (backward):
        evalstring += ','
        evalstring += repr(IMSL_BACKWARD)
    if not (params is None):
        evalstring += ','
        evalstring += repr(IMSL_PARAMS)
        evalstring += ','
        if (not(isinstance(params, POINTER(c_double)))):
            params = toNumpyArray(
                params, 'params', shape=shape, dtype='double', expectedShape=(2 * n + 15))
            evalstring += 'params.ctypes.data_as(c_void_p)'
        else:
            evalstring += 'params'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(n), result=True)
