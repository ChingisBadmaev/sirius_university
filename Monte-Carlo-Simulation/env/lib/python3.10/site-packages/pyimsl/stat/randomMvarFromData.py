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
from numpy import double, dtype, ndim, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
imslstat = loadimsl(STAT)


def randomMvarFromData(nRandom, x, nn, xColDim=None):
    """ Generates pseudorandom numbers from a multivariate distribution determined from a given sample.
    """
    imslstat.imsls_d_random_mvar_from_data.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_mvar_from_data('
    evalstring += 'c_int(nRandom)'
    evalstring += ','
    evalstring += 'c_int(ndim)'
    evalstring += ','
    evalstring += 'c_int(nsamp)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nsamp = shape[0]
    ndim = shape[1]
    evalstring += ','
    evalstring += 'c_int(nn)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nRandom, ndim), result=True)
