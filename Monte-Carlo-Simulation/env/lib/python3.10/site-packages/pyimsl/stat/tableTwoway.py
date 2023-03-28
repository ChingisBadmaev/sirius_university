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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict, processRet
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_DATA_BOUNDS = 11120
IMSLS_KNOWN_BOUNDS = 12620
IMSLS_CUTPOINTS = 11090
IMSLS_CLASS_MARKS = 10630
imslstat = loadimsl(STAT)


def tableTwoway(x, y, nx, ny, dataBounds=None, knownBounds=None, cutpoints=None, classMarks=None):
    """ Tallies observations into two-way frequency table.
    """
    imslstat.imsls_d_table_twoway.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_table_twoway('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=(nObservations))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(nx)'
    evalstring += ','
    evalstring += 'c_int(ny)'
    if not (dataBounds is None):
        evalstring += ','
        evalstring += repr(IMSLS_DATA_BOUNDS)
        checkForDict(dataBounds, 'dataBounds', [])
        evalstring += ','
        dataBounds_xmin_tmp = c_double()
        evalstring += 'byref(dataBounds_xmin_tmp)'
        evalstring += ','
        dataBounds_xmax_tmp = c_double()
        evalstring += 'byref(dataBounds_xmax_tmp)'
        evalstring += ','
        dataBounds_ymin_tmp = c_double()
        evalstring += 'byref(dataBounds_ymin_tmp)'
        evalstring += ','
        dataBounds_ymax_tmp = c_double()
        evalstring += 'byref(dataBounds_ymax_tmp)'
    if not (knownBounds is None):
        evalstring += ','
        evalstring += repr(IMSLS_KNOWN_BOUNDS)
        checkForDict(knownBounds, 'knownBounds', ['xlo', 'xhi', 'ylo', 'yhi'])
        evalstring += ','
        knownBounds_xlo_tmp = knownBounds['xlo']
        evalstring += 'c_double(knownBounds_xlo_tmp)'
        evalstring += ','
        knownBounds_xhi_tmp = knownBounds['xhi']
        evalstring += 'c_double(knownBounds_xhi_tmp)'
        evalstring += ','
        knownBounds_ylo_tmp = knownBounds['ylo']
        evalstring += 'c_double(knownBounds_ylo_tmp)'
        evalstring += ','
        knownBounds_yhi_tmp = knownBounds['yhi']
        evalstring += 'c_double(knownBounds_yhi_tmp)'
    if not (cutpoints is None):
        evalstring += ','
        evalstring += repr(IMSLS_CUTPOINTS)
        checkForDict(cutpoints, 'cutpoints', ['cx', 'cy'])
        evalstring += ','
        cutpoints_cx_tmp = cutpoints['cx']
        cutpoints_cx_tmp = toNumpyArray(
            cutpoints_cx_tmp, 'cx', shape=shape, dtype='double', expectedShape=(nx - 1))
        evalstring += 'cutpoints_cx_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cutpoints_cy_tmp = cutpoints['cy']
        cutpoints_cy_tmp = toNumpyArray(
            cutpoints_cy_tmp, 'cy', shape=shape, dtype='double', expectedShape=(ny - 1))
        evalstring += 'cutpoints_cy_tmp.ctypes.data_as(c_void_p)'
    if not (classMarks is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_MARKS)
        checkForDict(classMarks, 'classMarks', ['cx', 'cy'])
        evalstring += ','
        classMarks_cx_tmp = classMarks['cx']
        classMarks_cx_tmp = toNumpyArray(
            classMarks_cx_tmp, 'cx', shape=shape, dtype='double')
        evalstring += 'classMarks_cx_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        classMarks_cy_tmp = classMarks['cy']
        classMarks_cy_tmp = toNumpyArray(
            classMarks_cy_tmp, 'cy', shape=shape, dtype='double')
        evalstring += 'classMarks_cy_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (dataBounds is None):
        processRet(dataBounds_xmin_tmp, shape=(
            1), key='xmin', pyvar=dataBounds)
        processRet(dataBounds_xmax_tmp, shape=(
            1), key='xmax', pyvar=dataBounds)
        processRet(dataBounds_ymin_tmp, shape=(
            1), key='ymin', pyvar=dataBounds)
        processRet(dataBounds_ymax_tmp, shape=(
            1), key='ymax', pyvar=dataBounds)
    return processRet(result, shape=(nx, ny), result=True)
