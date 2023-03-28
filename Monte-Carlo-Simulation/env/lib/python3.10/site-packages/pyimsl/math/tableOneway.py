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
from pyimsl.util.imslUtils import MATH, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_DATA_BOUNDS = 10330
IMSL_KNOWN_BOUNDS = 10331
IMSL_CUTPOINTS = 10058
IMSL_CLASS_MARKS = 10332
imslmath = loadimsl(MATH)


def tableOneway(x, nIntervals, dataBounds=None, knownBounds=None, cutpoints=None, classMarks=None):
    """ Tallies observations into a one-way frequency table.
    """
    imslmath.imsl_d_table_oneway.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_table_oneway('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(nIntervals)'
    if not (dataBounds is None):
        evalstring += ','
        evalstring += repr(IMSL_DATA_BOUNDS)
        checkForDict(dataBounds, 'dataBounds', ['minimum', 'maximum'])
        evalstring += ','
        dataBounds_minimum_tmp = c_double()
        evalstring += 'byref(dataBounds_minimum_tmp)'
        evalstring += ','
        dataBounds_maximum_tmp = c_double()
        evalstring += 'byref(dataBounds_maximum_tmp)'
    if not (knownBounds is None):
        evalstring += ','
        evalstring += repr(IMSL_KNOWN_BOUNDS)
        checkForDict(knownBounds, 'knownBounds', ['lowerBound', 'upperBound'])
        evalstring += ','
        knownBounds_lowerBound_tmp = knownBounds['lowerBound']
        evalstring += 'c_double(knownBounds_lowerBound_tmp)'
        evalstring += ','
        knownBounds_upperBound_tmp = knownBounds['upperBound']
        evalstring += 'c_double(knownBounds_upperBound_tmp)'
    if not (cutpoints is None):
        evalstring += ','
        evalstring += repr(IMSL_CUTPOINTS)
        evalstring += ','
        cutpoints = toNumpyArray(
            cutpoints, 'cutpoints', shape=shape, dtype='double', expectedShape=(nIntervals - 1))
        evalstring += 'cutpoints.ctypes.data_as(c_void_p)'
    if not (classMarks is None):
        evalstring += ','
        evalstring += repr(IMSL_CLASS_MARKS)
        evalstring += ','
        classMarks = toNumpyArray(
            classMarks, 'classMarks', shape=shape, dtype='double', expectedShape=(nIntervals))
        evalstring += 'classMarks.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (dataBounds is None):
        processRet(dataBounds_minimum_tmp, shape=(
            1), key='minimum', pyvar=dataBounds)
        processRet(dataBounds_maximum_tmp, shape=(
            1), key='maximum', pyvar=dataBounds)
    return processRet(result, shape=(nIntervals), result=True)
