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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *
from pyimsl.util.VersionFacade import VersionFacade

IMSL_NUM_ROOTS = 10018
IMSL_FCN_W_DATA = 13101
IMSL_NUM_ROOTS_FOUND = 15025
IMSL_N_EVALS = 10023
IMSL_BOUND = 10102
IMSL_MAX_EVALS = 10277
IMSL_XGUESS = 10100
IMSL_ERR_ABS = 10010
IMSL_ERR_X = 15024
IMSL_TOLERANCE_MULLER = 15022
IMSL_MIN_SEPARATION = 15023
IMSL_XSCALE = 10106
imslmath = loadimsl(MATH)


def zerosFunction(fcn, numRoots=None, fcnWData=None, numRootsFound=None, nEvals=None,
                  bound=None, maxEvals=None, xguess=None, errAbs=None, errX=None, toleranceMuller=None,
                  minSeparation=None, xscale=None):
    VersionFacade.checkVersion(7)
    imslmath.imsl_d_zeros_function.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_zeros_function('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    if not (numRoots is None):
        evalstring += ','
        evalstring += repr(IMSL_NUM_ROOTS)
        evalstring += ','
        evalstring += 'c_int(numRoots)'
        nroot = numRoots
    else:
        nroot = 1
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcnWData', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(
            c_double, c_double, POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    # Always pass in numRootsFound to determine the size of the result
    if not (numRootsFound is None):
        checkForList(numRootsFound, 'numRootsFound')
    evalstring += ','
    evalstring += repr(IMSL_NUM_ROOTS_FOUND)
    evalstring += ','
    numRootsFound_numRootsFound_tmp = c_int()
    evalstring += 'byref(numRootsFound_numRootsFound_tmp)'
    if not (nEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_N_EVALS)
        checkForList(nEvals, 'nEvals')
        evalstring += ','
        nEvals_nEvals_tmp = c_int()
        evalstring += 'byref(nEvals_nEvals_tmp)'
    if not (bound is None):
        evalstring += ','
        evalstring += repr(IMSL_BOUND)
        checkForDict(bound, 'bound', ['a', 'b'])
        evalstring += ','
        bound_a_tmp = bound['a']
        evalstring += 'c_double(bound_a_tmp)'
        evalstring += ','
        bound_b_tmp = bound['b']
        evalstring += 'c_double(bound_b_tmp)'
    if not (maxEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_EVALS)
        evalstring += ','
        evalstring += 'c_int(maxEvals)'
    if not (xguess is None):
        if not (numRoots is None):
            xguess = toNumpyArray(
                xguess, 'xguess', shape=shape, dtype='double', expectedShape=(nroot))
        else:
            # If xguess is specified, the number of roots is implied
            # by the number of elements in xguess.
            xguess = toNumpyArray(
                xguess, 'xguess', shape=shape, dtype='double', expectedShape=(0))
            nroot = len(xguess)
            evalstring += ','
            evalstring += repr(IMSL_NUM_ROOTS)
            evalstring += ','
            evalstring += 'c_int(nroot)'
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        evalstring += 'xguess.ctypes.data_as(c_void_p)'
    if not (errAbs is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_ABS)
        evalstring += ','
        evalstring += 'c_double(errAbs)'
    if not (errX is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_X)
        evalstring += ','
        evalstring += 'c_double(errX)'
    if not (toleranceMuller is None):
        evalstring += ','
        evalstring += repr(IMSL_TOLERANCE_MULLER)
        evalstring += ','
        evalstring += 'c_double(toleranceMuller)'
    if not (minSeparation is None):
        evalstring += ','
        evalstring += repr(IMSL_MIN_SEPARATION)
        evalstring += ','
        evalstring += 'c_double(minSeparation)'
    if not (xscale is None):
        evalstring += ','
        evalstring += repr(IMSL_XSCALE)
        evalstring += ','
        evalstring += 'c_double(xscale)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (numRootsFound is None):
        processRet(numRootsFound_numRootsFound_tmp,
                   shape=(1), pyvar=numRootsFound)
    if not (nEvals is None):
        processRet(nEvals_nEvals_tmp, shape=(1), pyvar=nEvals)
    return processRet(result, shape=numRootsFound_numRootsFound_tmp, result=True)
