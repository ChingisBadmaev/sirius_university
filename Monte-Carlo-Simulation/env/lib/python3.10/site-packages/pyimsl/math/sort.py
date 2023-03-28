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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import absolute, double, dtype, shape, sort
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_ABSOLUTE = 10326
IMSL_PERMUTATION = 10327
imslmath = loadimsl(MATH)


def sort(x, absolute=None, permutation=None):
    """ Sorts a vector by algebraic value. Optionally, a vector can be sorted by absolute value, and a sort permutation can be returned.
    """
    imslmath.imsl_d_sort.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_sort('
    evalstring += 'c_int(n)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    n = shape[0]
    checkForBoolean(absolute, 'absolute')
    if (absolute):
        evalstring += ','
        evalstring += repr(IMSL_ABSOLUTE)
    if not (permutation is None):
        evalstring += ','
        evalstring += repr(IMSL_PERMUTATION)
        checkForList(permutation, 'permutation')
        evalstring += ','
        permutation_perm_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(permutation_perm_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (permutation is None):
        processRet(permutation_perm_tmp, shape=(n), pyvar=permutation)
    return processRet(result, shape=(n), result=True)
