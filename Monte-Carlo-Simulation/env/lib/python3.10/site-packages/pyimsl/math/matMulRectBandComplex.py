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
from pyimsl.util.imslUtils import MATH, checkForList, checkForDict, checkForStr, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray, toByte
from numpy import dtype, matrix, shape, size
from ctypes import POINTER, byref, c_int
from .mathStructs import d_complex
from .matMulResultSize import matMulCountMatrices, matMulResultSize

IMSL_A_MATRIX = 10181
IMSL_B_MATRIX = 10182
IMSL_X_VECTOR = 10183
IMSL_RETURN_MATRIX_CODIAGONALS = 11149
imslmath = loadimsl(MATH)


def matMulRectBandComplex(string, aMatrix=None, bMatrix=None, xVector=None, returnMatrixCodiagonals=None):
    """ Computes the transpose of a matrix, a matrix-vector product, or a matrix-matrix product for all matrices of complex type and stored in band form.
    """
    imslmath.imsl_z_mat_mul_rect_band.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_mat_mul_rect_band('
    checkForStr(string, 'string')
    evalstring += 'toByte(string)'
    aMatrix_nrowa_tmp = 1
    aMatrix_ncola_tmp = 1
    bMatrix_nrowb_tmp = 1
    bMatrix_ncolb_tmp = 1
    xVector_nx_tmp = 1
    yVector_ny_tmp = 1
    if not (aMatrix is None):
        evalstring += ','
        evalstring += repr(IMSL_A_MATRIX)
        checkForDict(aMatrix, 'aMatrix', [
                     'nrowa', 'ncola', 'nlca', 'nuca', 'a'])
        evalstring += ','
        aMatrix_nrowa_tmp = aMatrix['nrowa']
        evalstring += 'c_int(aMatrix_nrowa_tmp)'
        evalstring += ','
        aMatrix_ncola_tmp = aMatrix['ncola']
        evalstring += 'c_int(aMatrix_ncola_tmp)'
        evalstring += ','
        aMatrix_nlca_tmp = aMatrix['nlca']
        evalstring += 'c_int(aMatrix_nlca_tmp)'
        evalstring += ','
        aMatrix_nuca_tmp = aMatrix['nuca']
        evalstring += 'c_int(aMatrix_nuca_tmp)'
        evalstring += ','
        aMatrix_a_tmp = aMatrix['a']
        aMatrix_a_tmp = toNumpyArray(aMatrix_a_tmp, 'a', shape=shape, dtype='d_complex', expectedShape=(
            aMatrix_nlca_tmp + aMatrix_nuca_tmp + 1, aMatrix_ncola_tmp))
        evalstring += 'aMatrix_a_tmp'
    if not (bMatrix is None):
        evalstring += ','
        evalstring += repr(IMSL_B_MATRIX)
        checkForDict(bMatrix, 'bMatrix', [
                     'nrowb', 'ncolb', 'nlcb', 'nucb', 'b'])
        evalstring += ','
        bMatrix_nrowb_tmp = bMatrix['nrowb']
        evalstring += 'c_int(bMatrix_nrowb_tmp)'
        evalstring += ','
        bMatrix_ncolb_tmp = bMatrix['ncolb']
        evalstring += 'c_int(bMatrix_ncolb_tmp)'
        evalstring += ','
        bMatrix_nlcb_tmp = bMatrix['nlcb']
        evalstring += 'c_int(bMatrix_nlcb_tmp)'
        evalstring += ','
        bMatrix_nucb_tmp = bMatrix['nucb']
        evalstring += 'c_int(bMatrix_nucb_tmp)'
        evalstring += ','
        bMatrix_b_tmp = bMatrix['b']
        bMatrix_b_tmp = toNumpyArray(bMatrix_b_tmp, 'b', shape=shape, dtype='d_complex', expectedShape=(
            bMatrix_nlcb_tmp + bMatrix_nucb_tmp + 1, bMatrix_ncolb))
        evalstring += 'bMatrix_b_tmp'
    if not (xVector is None):
        evalstring += ','
        evalstring += repr(IMSL_X_VECTOR)
        evalstring += ','
        evalstring += 'c_int(xVector_nx_tmp)'
        evalstring += ','
        xVector_x_tmp = toNumpyArray(
            xVector, 'xVector', shape=shape, dtype='d_complex', expectedShape=(0))
        evalstring += 'xVector_x_tmp'
        xVector_nx_tmp = shape[0]

    returnMatrixCodiagonals_nlcResult_tmp = c_int()
    returnMatrixCodiagonals_nucResult_tmp = c_int()
    if (not(returnMatrixCodiagonals is None)):
        checkForList(returnMatrixCodiagonals, 'returnMatrixCodiagonals')
    matrixCount = matMulCountMatrices(string)
    if (matrixCount[0] > 1) or (matrixCount[1] > 1) or ((matrixCount[0] == 1) and (matrixCount[1] == 1)):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_MATRIX_CODIAGONALS)
        evalstring += ','
        returnMatrixCodiagonals_nlcResult_tmp = c_int()
        evalstring += 'byref(returnMatrixCodiagonals_nlcResult_tmp)'
        evalstring += ','
        returnMatrixCodiagonals_nucResult_tmp = c_int()
        evalstring += 'byref(returnMatrixCodiagonals_nucResult_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    #
    # If both A and B are specified, or either is specified twice,
    # the size of the returned
    # matrix is specified by the codiagonals.  Otherwise, it is based on the
    # size of X.
    #
    if (matrixCount[0] > 1) or (matrixCount[1] > 1) or ((matrixCount[0] == 1) and (matrixCount[1] == 1)):
        resultSize = [returnMatrixCodiagonals_nlcResult_tmp.value
                      + returnMatrixCodiagonals_nucResult_tmp.value + 1, aMatrix_ncola_tmp]
    else:
        resultSize = matMulResultSize(string, aMatrix_nrowa_tmp, aMatrix_ncola_tmp,
                                      bMatrix_nrowb_tmp, bMatrix_ncolb_tmp, xVector_nx_tmp, yVector_ny_tmp)
    if not (returnMatrixCodiagonals is None):
        # Because we are putting 2 seperate params into result can not use processRet here
        if isinstance(returnMatrixCodiagonals, list):
            returnMatrixCodiagonals[:] = []
            returnMatrixCodiagonals.append(
                returnMatrixCodiagonals_nlcResult_tmp.value)
            returnMatrixCodiagonals.append(
                returnMatrixCodiagonals_nucResult_tmp.value)
        else:
            returnMatrixCodiagonals.resize(2, refcheck=0)
            returnMatrixCodiagonals[0] = returnMatrixCodiagonals_nlcResult_tmp.value
            returnMatrixCodiagonals[0] = returnMatrixCodiagonals_nucResult_tmp.value
    return processRet(result, shape=(resultSize[0], resultSize[1]), result=True)
