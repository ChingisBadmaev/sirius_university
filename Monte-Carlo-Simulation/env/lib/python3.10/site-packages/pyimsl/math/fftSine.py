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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSL_PARAMS = 10009
imslmath = loadimsl(MATH)


def fftSine(p, params=None):
    """ Computes the discrete Fourier sine transformation of an odd sequence.
    """
    imslmath.imsl_d_fft_sine.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_fft_sine('
    evalstring += 'c_int(n)'
    evalstring += ','
    p = toNumpyArray(p, 'p', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'p.ctypes.data_as(c_void_p)'
    n = shape[0]
    if not (params is None):
        evalstring += ','
        evalstring += repr(IMSL_PARAMS)
        evalstring += ','
        params = toNumpyArray(params, 'params', shape=shape,
                              dtype='double', expectedShape=(2 * n + 15))
        evalstring += 'params.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(n), result=True)
