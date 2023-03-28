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
from pyimsl.util.imslUtils import MATH, checkForList, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, byref, c_double, c_int
from .mathStructs import Imsl_faure

IMSL_RETURN_SKIP = 12102
imslmath = loadimsl(MATH)


def faureNextPoint(state, returnSkip=None):
    """ Computes a shuffled Faure sequence.
    """
    imslmath.imsl_d_faure_next_point.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_faure_next_point('
    evalstring += 'state'
    if not (returnSkip is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_SKIP)
        checkForList(returnSkip, 'returnSkip')
        evalstring += ','
        returnSkip_skip_tmp = c_int()
        evalstring += 'byref(returnSkip_skip_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (returnSkip is None):
        processRet(returnSkip_skip_tmp, shape=1, pyvar=returnSkip)
    return processRet(result, shape=(state[0].dim), result=True)
