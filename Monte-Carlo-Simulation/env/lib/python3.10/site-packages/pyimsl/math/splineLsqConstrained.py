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
from pyimsl.util.imslUtils import MATH, checkForList, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_int, c_void_p
from .mathStructs import Imsl_d_spline
from .mathStructs import d_constraint_struct

IMSL_NHARD = 11080
IMSL_WEIGHTS = 10141
IMSL_ORDER = 10036
IMSL_KNOTS = 10035
imslmath = loadimsl(MATH)


def splineLsqConstrained(xdata, fdata, splineSpaceDim, numConPts, constraints, nhard=None, weights=None, order=None, knots=None):
    """ Computes a least-squares constrained spline approximation.
    """
    imslmath.imsl_d_spline_lsq_constrained.restype = POINTER(Imsl_d_spline)
    shape = []
    evalstring = 'imslmath.imsl_d_spline_lsq_constrained('
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
    evalstring += ','
    evalstring += 'c_int(splineSpaceDim)'
    evalstring += ','
    evalstring += 'c_int(numConPts)'
    evalstring += ','
    evalstring += 'constraints'
    if not (nhard is None):
        evalstring += ','
        evalstring += repr(IMSL_NHARD)
        checkForList(nhard, 'nhard')
        evalstring += ','
        nhard_nhard_tmp = c_int()
        evalstring += 'byref(nhard_nhard_tmp)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(ndata))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (order is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER)
        evalstring += ','
        evalstring += 'c_int(order)'
    else:
        order = 4
    if not (knots is None):
        evalstring += ','
        evalstring += repr(IMSL_KNOTS)
        evalstring += ','
        knots = toNumpyArray(knots, 'knots', shape=shape,
                             dtype='double', expectedShape=(splineSpaceDim + order))
        evalstring += 'knots.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (nhard is None):
        processRet(nhard_nhard_tmp, shape=1, pyvar=nhard)
    return result
