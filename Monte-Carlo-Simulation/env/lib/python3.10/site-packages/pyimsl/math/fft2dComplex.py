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
from numpy import dtype, shape
from ctypes import POINTER, c_int

IMSL_P_COL_DIM = 10180
IMSL_BACKWARD = 10008
IMSL_Q_COL_DIM = 10179
imslmath = loadimsl(MATH)


def fft2dComplex(p, pColDim=None, backward=None, qColDim=None):
    """ Computes the complex discrete two-dimensional Fourier transform of a complex two-dimensional array.
    """
    imslmath.imsl_z_fft_2d_complex.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_fft_2d_complex('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(m)'
    evalstring += ','
    p = toNumpyArray(p, 'p', shape=shape, dtype='d_complex',
                     expectedShape=((0, 0)))
    evalstring += 'p'
    n = shape[0]
    m = shape[1]
    if not (pColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_P_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(pColDim)'
    checkForBoolean(backward, 'backward')
    if (backward):
        evalstring += ','
        evalstring += repr(IMSL_BACKWARD)
    if not (qColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_Q_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(qColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(n, m), result=True)
