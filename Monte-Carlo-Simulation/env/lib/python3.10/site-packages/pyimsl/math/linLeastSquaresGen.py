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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, int, ndarray, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_BASIS = 10170
IMSL_RESIDUAL = 10172
IMSL_FACTOR = 10004
IMSL_Q = 10177
IMSL_PIVOT = 10171
IMSL_FACTOR_ONLY = 10006
IMSL_SOLVE_ONLY = 10007
IMSL_FACTOR_USER = 10151
imslmath = loadimsl(MATH)


def linLeastSquaresGen(a, b, basis=None, residual=None, factor=None, q=None, pivot=None, factorOnly=None, solveOnly=None):
    """ Solves a linear least-squares problem Ax = b. Using optional arguments, the QR factorization of A, AP = QR, and the solve step based on this factorization can be computed.
    """
    imslmath.imsl_d_lin_least_squares_gen.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_lin_least_squares_gen('
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    # with soveOnly argument a is ignored
    checkForBoolean(factorOnly, 'factorOnly')
    checkForBoolean(solveOnly, 'solveOnly')
    if solveOnly:
        evalstring += 'c_void_p()'
    else:
        a = toNumpyArray(a, 'a', shape=shape, dtype='double',
                         expectedShape=(0, 0))
        evalstring += 'a.ctypes.data_as(c_void_p)'
        m = shape[0]
        n = shape[1]
    evalstring += ','
    if factorOnly:
        evalstring += 'c_void_p()'
    else:
        if not solveOnly:
            # In this case check that b is of length m.
            b = toNumpyArray(b, 'b', shape=shape,
                             dtype='double', expectedShape=(m))
            evalstring += 'b.ctypes.data_as(c_void_p)'
        else:
            # In this case, set m based on length of b.
            b = toNumpyArray(b, 'b', shape=shape,
                             dtype='double', expectedShape=(0))
            evalstring += 'b.ctypes.data_as(c_void_p)'
            m = shape[0]
    if not (basis is None):
        evalstring += ','
        evalstring += repr(IMSL_BASIS)
        checkForDict(basis, 'basis', ['tol'])
        evalstring += ','
        basis_tol_tmp = basis['tol']
        evalstring += 'c_double(basis_tol_tmp)'
        evalstring += ','
        basis_kbasis_tmp = c_int()
        if 'kbasis' in basis:  # kbasis is input/output so not always defined on output
            basis_kbasis_tmp = c_int(basis['kbasis'])
        evalstring += 'byref(basis_kbasis_tmp)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSL_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_pRes_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_pRes_tmp)'
    if not (factor is None):
        if solveOnly:  # must use IMSL_FACTOR_USER as is input (and output?)
            evalstring += ','
            evalstring += repr(IMSL_FACTOR_USER)
            checkForDict(factor, 'factor', ['pQraux', 'pQr'])
            evalstring += ','
            factor_pQraux_tmp = factor['pQraux']
            factor_pQraux_tmp = toNumpyArray(
                factor_pQraux_tmp, 'pQraux', shape=shape, dtype='double', expectedShape=(0))
            evalstring += 'factor_pQraux_tmp.ctypes.data_as(c_void_p)'
            evalstring += ','
            factor_pQr_tmp = factor['pQr']
            factor_pQr_tmp = toNumpyArray(
                factor_pQr_tmp, 'pQr', shape=shape, dtype='double', expectedShape=(0, 0))
            m = shape[0]
            n = shape[1]
            evalstring += 'factor_pQr_tmp.ctypes.data_as(c_void_p)'
        else:
            # is a normal output var
            evalstring += ','
            evalstring += repr(IMSL_FACTOR)
            checkForDict(factor, 'factor', [])
            evalstring += ','
            factor_pQraux_tmp = POINTER(c_double)(c_double())
            factor_pQr_tmp = POINTER(c_double)(c_double())
            evalstring += 'byref(factor_pQraux_tmp)'
            evalstring += ','
            evalstring += 'byref(factor_pQr_tmp)'
    if not (q is None):
        evalstring += ','
        evalstring += repr(IMSL_Q)
        checkForList(q, 'q')
        evalstring += ','
        q_pQ_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(q_pQ_tmp)'
    if not (pivot is None):
        evalstring += ','
        evalstring += repr(IMSL_PIVOT)
        evalstring += ','
        pivot_pvt_tmp = toNumpyArray(
            pivot, 'pivot', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'pivot_pvt_tmp.ctypes.data_as(c_void_p)'
    if (factorOnly):
        evalstring += ','
        evalstring += repr(IMSL_FACTOR_ONLY)
    if (solveOnly):
        evalstring += ','
        evalstring += repr(IMSL_SOLVE_ONLY)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (basis is None):
        processRet(basis_kbasis_tmp, shape=(1), key='kbasis', pyvar=basis)
    if not (residual is None):
        processRet(residual_pRes_tmp, shape=(m), pyvar=residual)
    if not (factor is None):
        processRet(factor_pQraux_tmp, shape=(n), key='pQraux', pyvar=factor)
        processRet(factor_pQr_tmp, shape=(m, n), key='pQr', pyvar=factor)
    if not (q is None):
        processRet(q_pQ_tmp, shape=(m, m), pyvar=q)
    if not (pivot is None):
        processRet(pivot_pvt_tmp, inout=True, shape=(n), pyvar=pivot)
    return processRet(result, shape=(n), result=True)
