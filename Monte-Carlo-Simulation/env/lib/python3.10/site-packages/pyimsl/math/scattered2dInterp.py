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

IMSL_SUR_COL_DIM = 10147
imslmath = loadimsl(MATH)


def scattered2dInterp(xydata, fdata, xOut, yOut):
    # Note that the CNL IMSL_COL_DIM keyword is not supported, because
    # it only applies when IMSL_RETURN_USER is used.
    """ Computes a smooth bivariate interpolant to scattered data that is locally a quintic polynomial in two variables.
    """
    imslmath.imsl_d_scattered_2d_interp.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_scattered_2d_interp('
    evalstring += 'c_int(ndata)'
    evalstring += ','
    xydata = toNumpyArray(xydata, 'xydata', shape=shape,
                          dtype='double', expectedShape=(0, 2))
    evalstring += 'xydata.ctypes.data_as(c_void_p)'
    ndata = shape[0]
    evalstring += ','
    fdata = toNumpyArray(fdata, 'fdata', shape=shape,
                         dtype='double', expectedShape=(ndata))
    evalstring += 'fdata.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(nxOut)'
    evalstring += ','
    evalstring += 'c_int(nyOut)'
    evalstring += ','
    xOut = toNumpyArray(xOut, 'xOut', shape=shape,
                        dtype='double', expectedShape=(0))
    evalstring += 'xOut.ctypes.data_as(c_void_p)'
    nxOut = shape[0]
    evalstring += ','
    yOut = toNumpyArray(yOut, 'yOut', shape=shape,
                        dtype='double', expectedShape=(0))
    evalstring += 'yOut.ctypes.data_as(c_void_p)'
    nyOut = shape[0]
    surColDim = nyOut
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(nxOut, surColDim), result=True)
