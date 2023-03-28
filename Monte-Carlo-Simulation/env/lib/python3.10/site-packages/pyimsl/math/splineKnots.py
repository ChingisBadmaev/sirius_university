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
from pyimsl.util.imslUtils import MATH, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSL_ORDER = 10036
IMSL_OPT = 10037
IMSL_OPT_ITMAX = 10148
imslmath = loadimsl(MATH)


def splineKnots(xdata, order=None, opt=None, optItmax=None):
    """ Computes the knots for a spline interpolant
    """
    imslmath.imsl_d_spline_knots.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_spline_knots('
    evalstring += 'c_int(ndata)'
    evalstring += ','
    xdata = toNumpyArray(xdata, 'xdata', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'xdata.ctypes.data_as(c_void_p)'
    ndata = shape[0]
    if not (order is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER)
        evalstring += ','
        evalstring += 'c_int(order)'
    else:
        order = 4
    checkForBoolean(opt, 'opt')
    if (opt):
        evalstring += ','
        evalstring += repr(IMSL_OPT)
    if not (optItmax is None):
        evalstring += ','
        evalstring += repr(IMSL_OPT_ITMAX)
        evalstring += ','
        evalstring += 'c_int(optItmax)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(ndata + order), result=True)
