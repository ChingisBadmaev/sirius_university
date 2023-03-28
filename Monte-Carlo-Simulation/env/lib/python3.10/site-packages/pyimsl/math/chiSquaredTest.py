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
from numpy import double, dtype, shape, size, empty, ndarray
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_N_PARAMETERS_ESTIMATED = 10057
IMSL_CUTPOINTS = 10058
IMSL_CUTPOINTS_USER = 10059
IMSL_CUTPOINTS_EQUAL = 10280
IMSL_CHI_SQUARED = 10322
IMSL_DEGREES_OF_FREEDOM = 10066
IMSL_FREQUENCIES = 10054
IMSL_BOUNDS = 10056
IMSL_CELL_COUNTS = 10060
IMSL_CELL_EXPECTED = 10062
IMSL_CELL_CHI_SQUARED = 10064
IMSL_FCN_W_DATA = 13101
imslmath = loadimsl(MATH)
# cutpoints (Input or Output)
# Usage :
#     output - users must pass in an empty list


def chiSquaredTest(userProcCdf, nCategories, x, nParametersEstimated=None, cutpoints=None, cutpointsEqual=None, chiSquared=None, degreesOfFreedom=None, frequencies=None, bounds=None, cellCounts=None, cellExpected=None, cellChiSquared=None, fcnWData=None):
    """ Performs a chi-squared goodness-of-fit test.
    """
    imslmath.imsl_d_chi_squared_test.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_chi_squared_test('
    checkForCallable(userProcCdf, 'userProcCdf')
    TMP_USERPROCCDF = CFUNCTYPE(c_double, c_double)
    tmp_userProcCdf = TMP_USERPROCCDF(userProcCdf)
    evalstring += 'tmp_userProcCdf'
    evalstring += ','
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nCategories)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (nParametersEstimated is None):
        evalstring += ','
        evalstring += repr(IMSL_N_PARAMETERS_ESTIMATED)
        evalstring += ','
        evalstring += 'c_int(nParametersEstimated)'
    # cutpoints - use IMSL_CUTPOINT_USER for input and IMSL_CUTPOINT for output.
    # Typically, One can define an empty array of teh correct size and use the
    # the IMSL_CUTPOINTS_USER keyword but there seems to be a problem in doing so.
    if not (cutpoints is None):
        evalstring += ','
        if isinstance(cutpoints, ndarray):
            length = cutpoints.size
        else:
            length = len(cutpoints)
        if(length == 0):
            evalstring += repr(IMSL_CUTPOINTS)
            evalstring += ','
            cutpoints_pCutpoints_tmp = POINTER(c_double)(c_double())
            evalstring += 'byref(cutpoints_pCutpoints_tmp)'
        else:
            evalstring += repr(IMSL_CUTPOINTS_USER)
            checkForList(cutpoints, 'cutpoints', size=(nCategories - 1))
            evalstring += ','
            cutpoints_pCutpoints_tmp = toNumpyArray(
                cutpoints, 'cutpoints', shape=shape, dtype='double', expectedShape=(nCategories - 1))
            evalstring += 'cutpoints_pCutpoints_tmp.ctypes.data_as(c_void_p)'
    checkForBoolean(cutpointsEqual, 'cutpointsEqual')
    if (cutpointsEqual):
        evalstring += ','
        evalstring += repr(IMSL_CUTPOINTS_EQUAL)
    if not (chiSquared is None):
        evalstring += ','
        evalstring += repr(IMSL_CHI_SQUARED)
        checkForList(chiSquared, 'chiSquared')
        evalstring += ','
        chiSquared_chiSquared_tmp = c_double()
        evalstring += 'byref(chiSquared_chiSquared_tmp)'
    if not (degreesOfFreedom is None):
        evalstring += ','
        evalstring += repr(IMSL_DEGREES_OF_FREEDOM)
        checkForList(degreesOfFreedom, 'degreesOfFreedom')
        evalstring += ','
        degreesOfFreedom_df_tmp = c_double()
        evalstring += 'byref(degreesOfFreedom_df_tmp)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSL_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (bounds is None):
        evalstring += ','
        evalstring += repr(IMSL_BOUNDS)
        checkForDict(bounds, 'bounds', ['lowerBound', 'upperBound'])
        evalstring += ','
        bounds_lowerBound_tmp = bounds['lowerBound']
        evalstring += 'c_double(bounds_lowerBound_tmp)'
        evalstring += ','
        bounds_upperBound_tmp = bounds['upperBound']
        evalstring += 'c_double(bounds_upperBound_tmp)'
    if not (cellCounts is None):
        evalstring += ','
        evalstring += repr(IMSL_CELL_COUNTS)
        checkForList(cellCounts, 'cellCounts')
        evalstring += ','
        cellCounts_pCellCounts_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cellCounts_pCellCounts_tmp)'
    if not (cellExpected is None):
        evalstring += ','
        evalstring += repr(IMSL_CELL_EXPECTED)
        checkForList(cellExpected, 'cellExpected')
        evalstring += ','
        cellExpected_pCellExpected_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cellExpected_pCellExpected_tmp)'
    if not (cellChiSquared is None):
        evalstring += ','
        evalstring += repr(IMSL_CELL_CHI_SQUARED)
        checkForList(cellChiSquared, 'cellChiSquared')
        evalstring += ','
        cellChiSquared_pCellChiSquared_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cellChiSquared_pCellChiSquared_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcn', 'data'])
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData['fcn']
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_double, POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (cutpoints is None):
        processRet(cutpoints_pCutpoints_tmp, shape=(
            nCategories - 1), inout=True, pyvar=cutpoints)
    if not (chiSquared is None):
        processRet(chiSquared_chiSquared_tmp, shape=1, pyvar=chiSquared)
    if not (degreesOfFreedom is None):
        processRet(degreesOfFreedom_df_tmp, shape=1, pyvar=degreesOfFreedom)
    if not (cellCounts is None):
        processRet(cellCounts_pCellCounts_tmp,
                   shape=(nCategories), pyvar=cellCounts)
    if not (cellExpected is None):
        processRet(cellExpected_pCellExpected_tmp,
                   shape=(nCategories), pyvar=cellExpected)
    if not (cellChiSquared is None):
        processRet(cellChiSquared_pCellChiSquared_tmp,
                   shape=(nCategories), pyvar=cellChiSquared)
    return result
