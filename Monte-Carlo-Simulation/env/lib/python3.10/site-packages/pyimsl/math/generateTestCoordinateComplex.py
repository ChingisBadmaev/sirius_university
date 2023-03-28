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
from pyimsl.util.imslUtils import Imsl_c_sparse_elem, MATH, checkForBoolean, d_complex, fatalErrorCheck, loadimsl
from numpy import complex, int, matrix, shape
from ctypes import POINTER, byref, c_int, pointer


IMSL_D_MATRIX = 11093
IMSL_SYMMETRIC_STORAGE = 11094
imslmath = loadimsl(MATH)


def generateTestCoordinateComplex(n, c, matrix=None, symmetricStorage=None):
    """ Generates test matrices of class D(n, c) and E(n, c). Returns in either coordinate or band storage format, where possible.
    """
    imslmath.imsl_z_generate_test_coordinate.restype = POINTER(
        Imsl_c_sparse_elem)
    shape = []
    evalstring = 'imslmath.imsl_z_generate_test_coordinate('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(c)'
    evalstring += ','
    nz_tmp = c_int()
    evalstring += 'byref(nz_tmp)'
    checkForBoolean(matrix, 'matrix')
    if (matrix):
        evalstring += ','
        evalstring += repr(IMSL_D_MATRIX)
    checkForBoolean(symmetricStorage, 'symmetricStorage')
    if (symmetricStorage):
        evalstring += ','
        evalstring += repr(IMSL_SYMMETRIC_STORAGE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)

    # result is a pointer to Imsl_c_sparse_elem.
    # Imsl_c_sparse struct is made up of row,col, and value
    # but the value is of type d_complex (imsl struct), we need
    # to convert it back to python complex.
    # We can make use of the list to hold both int for rows/cols and complex
    # values.
    res = []
    for i in range(0, nz_tmp.value):
        temp = result[i].val
        res.append([result[i].row, result[i].col, (complex(temp.re, temp.im))])
    return res
