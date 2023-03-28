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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, rank, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_XGUESS = 10100
IMSL_JACOBIAN = 10118
IMSL_XSCALE = 10106
IMSL_FSCALE = 10107
IMSL_GRAD_TOL = 10108
IMSL_STEP_TOL = 10109
IMSL_REL_FCN_TOL = 10110
IMSL_ABS_FCN_TOL = 10290
IMSL_MAX_STEP = 10111
IMSL_INIT_TRUST_REGION = 10104
IMSL_GOOD_DIGIT = 10112
IMSL_MAX_ITN = 10113
IMSL_MAX_FCN = 10103
IMSL_MAX_JACOBIAN = 10291
IMSL_INTERN_SCALE = 10292
IMSL_TOLERANCE = 10053
IMSL_FVEC = 10293
IMSL_FJAC = 10295
IMSL_FJAC_COL_DIM = 10297
IMSL_RANK = 10049
IMSL_JTJ_INVERSE = 10298
IMSL_JTJ_INV_COL_DIM = 10300
IMSL_FCN_W_DATA = 13101
IMSL_JACOBIAN_W_DATA = 13104
imslmath = loadimsl(MATH)


def nonlinLeastSquares(fcn, m, n, xguess=None, jacobian=None, xscale=None, fscale=None, gradTol=None, stepTol=None, relFcnTol=None, absFcnTol=None, maxStep=None, initTrustRegion=None, goodDigit=None, maxItn=None, maxFcn=None, maxJacobian=None, internScale=None, tolerance=None, fvec=None, fjac=None, fjacColDim=None, rank=None, jtjInverse=None, jtjInvColDim=None):
    """ Solve a nonlinear least-squares problem using a modified Levenberg-Marquardt algorithm.
    """
    imslmath.imsl_d_nonlin_least_squares.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_nonlin_least_squares('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_void_p, c_int, c_int,
                        POINTER(c_double), POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        xguess = toNumpyArray(xguess, 'xguess', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'xguess.ctypes.data_as(c_void_p)'
    if not (jacobian is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBIAN)
        evalstring += ','
        checkForCallable(jacobian, 'jacobian')
        TMP_JACOBIAN_JACOBIAN = CFUNCTYPE(
            c_void_p, c_int, c_int, POINTER(c_double), POINTER(c_double), c_int)
        tmp_jacobian_jacobian = TMP_JACOBIAN_JACOBIAN(jacobian)
        evalstring += 'tmp_jacobian_jacobian'
    if not (xscale is None):
        evalstring += ','
        evalstring += repr(IMSL_XSCALE)
        evalstring += ','
        xscale = toNumpyArray(xscale, 'xscale', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'xscale.ctypes.data_as(c_void_p)'
    if not (fscale is None):
        evalstring += ','
        evalstring += repr(IMSL_FSCALE)
        evalstring += ','
        fscale = toNumpyArray(fscale, 'fscale', shape=shape,
                              dtype='double', expectedShape=(m))
        evalstring += 'fscale.ctypes.data_as(c_void_p)'
    if not (gradTol is None):
        evalstring += ','
        evalstring += repr(IMSL_GRAD_TOL)
        evalstring += ','
        evalstring += 'c_double(gradTol)'
    if not (stepTol is None):
        evalstring += ','
        evalstring += repr(IMSL_STEP_TOL)
        evalstring += ','
        evalstring += 'c_double(stepTol)'
    if not (relFcnTol is None):
        evalstring += ','
        evalstring += repr(IMSL_REL_FCN_TOL)
        evalstring += ','
        evalstring += 'c_double(relFcnTol)'
    if not (absFcnTol is None):
        evalstring += ','
        evalstring += repr(IMSL_ABS_FCN_TOL)
        evalstring += ','
        evalstring += 'c_double(absFcnTol)'
    if not (maxStep is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_STEP)
        evalstring += ','
        evalstring += 'c_double(maxStep)'
    if not (initTrustRegion is None):
        evalstring += ','
        evalstring += repr(IMSL_INIT_TRUST_REGION)
        evalstring += ','
        evalstring += 'c_double(initTrustRegion)'
    if not (goodDigit is None):
        evalstring += ','
        evalstring += repr(IMSL_GOOD_DIGIT)
        evalstring += ','
        evalstring += 'c_int(goodDigit)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    if not (maxJacobian is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_JACOBIAN)
        evalstring += ','
        evalstring += 'c_int(maxJacobian)'
    checkForBoolean(internScale, 'internScale')
    if (internScale):
        evalstring += ','
        evalstring += repr(IMSL_INTERN_SCALE)
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (fvec is None):
        evalstring += ','
        evalstring += repr(IMSL_FVEC)
        checkForList(fvec, 'fvec')
        evalstring += ','
        fvec_fvec_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(fvec_fvec_tmp)'
    if not (fjac is None):
        evalstring += ','
        evalstring += repr(IMSL_FJAC)
        checkForList(fjac, 'fjac')
        evalstring += ','
        fjac_fjac_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(fjac_fjac_tmp)'
    if not (fjacColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_FJAC_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(fjacColDim)'
    if not (rank is None):
        evalstring += ','
        evalstring += repr(IMSL_RANK)
        checkForList(rank, 'rank')
        evalstring += ','
        rank_rank_tmp = c_int()
        evalstring += 'byref(rank_rank_tmp)'
    if not (jtjInverse is None):
        evalstring += ','
        evalstring += repr(IMSL_JTJ_INVERSE)
        checkForList(jtjInverse, 'jtjInverse')
        evalstring += ','
        jtjInverse_jtjInverse_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(jtjInverse_jtjInverse_tmp)'
    if not (jtjInvColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_JTJ_INV_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(jtjInvColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (fvec is None):
        processRet(fvec_fvec_tmp, shape=(m), pyvar=fvec)
    if not (fjac is None):
        processRet(fjac_fjac_tmp, shape=(m, n), pyvar=fjac)
    if not (rank is None):
        processRet(rank_rank_tmp, shape=1, pyvar=rank)
    if not (jtjInverse is None):
        processRet(jtjInverse_jtjInverse_tmp, shape=(n, n), pyvar=jtjInverse)
    return processRet(result, shape=(n), result=True)
