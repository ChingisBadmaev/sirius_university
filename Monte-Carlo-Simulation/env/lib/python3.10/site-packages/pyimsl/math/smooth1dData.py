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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSL_ITMAX = 10016
IMSL_DISTANCE = 12001
IMSL_STOPPING_CRITERION = 12002
imslmath = loadimsl(MATH)


def smooth1dData(xdata, fdata, itmax=None, distance=None, stoppingCriterion=None):
    """ Smooth one-dimensional data by error detection.
    """
    imslmath.imsl_d_smooth_1d_data.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_smooth_1d_data('
    evalstring += 'c_int(ndata)'
    evalstring += ','
    xdata = toNumpyArray(xdata, 'xdata', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'xdata.ctypes.data_as(c_void_p)'
    ndata = shape[0]
    evalstring += ','
    fdata = toNumpyArray(fdata, 'fdata', shape=shape,
                         dtype='double', expectedShape=(ndata))
    evalstring += 'fdata.ctypes.data_as(c_void_p)'
    if not (itmax is None):
        evalstring += ','
        evalstring += repr(IMSL_ITMAX)
        evalstring += ','
        evalstring += 'c_int(itmax)'
    if not (distance is None):
        evalstring += ','
        evalstring += repr(IMSL_DISTANCE)
        evalstring += ','
        evalstring += 'c_double(distance)'
    if not (stoppingCriterion is None):
        evalstring += ','
        evalstring += repr(IMSL_STOPPING_CRITERION)
        evalstring += ','
        evalstring += 'c_double(stoppingCriterion)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(ndata), result=True)
