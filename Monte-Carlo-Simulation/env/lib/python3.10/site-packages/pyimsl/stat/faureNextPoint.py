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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, byref, c_double
from .statStructs import Imsls_faure

IMSLS_RETURN_SKIP = 40018
imslstat = loadimsl(STAT)


def faureNextPoint(state, returnSkip=None):
    """ Computes a shuffled Faure sequence.
    """
    imslstat.imsls_d_faure_next_point.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_faure_next_point('
    evalstring += 'state'
    if not (returnSkip is None):
        evalstring += ','
        evalstring += repr(IMSLS_RETURN_SKIP)
        checkForList(returnSkip, 'returnSkip')
        evalstring += ','
        returnSkip_skip_tmp = c_double()
        evalstring += 'byref(returnSkip_skip_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (returnSkip is None):
        processRet(returnSkip_skip_tmp, shape=1, pyvar=returnSkip)
    return processRet(result, shape=(3), result=True)
