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
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_EIGENVALUES = 11300
IMSLS_A_MATRIX = 10180
IMSLS_A_COL_DIM = 10170
imslstat = loadimsl(STAT)


def randomOrthogonalMatrix(n, eigenvalues=None, aMatrix=None, aColDim=None):
    """ Generates a pseudorandom orthogonal matrix or a correlation matrix.
    """
    imslstat.imsls_d_random_orthogonal_matrix.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_orthogonal_matrix('
    evalstring += 'c_int(n)'
    if not (eigenvalues is None):
        evalstring += ','
        evalstring += repr(IMSLS_EIGENVALUES)
        evalstring += ','
        eigenvalues = toNumpyArray(
            eigenvalues, 'eigenvalues', shape=shape, dtype='double', expectedShape=(n))
        evalstring += 'eigenvalues.ctypes.data_as(c_void_p)'
    if not (aMatrix is None):
        evalstring += ','
        evalstring += repr(IMSLS_A_MATRIX)
        evalstring += ','
        aMatrix = toNumpyArray(
            aMatrix, 'aMatrix', shape=shape, dtype='double', expectedShape=(n, n))
        evalstring += 'aMatrix.ctypes.data_as(c_void_p)'
    if not (aColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_A_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(aColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(n, n), result=True)
