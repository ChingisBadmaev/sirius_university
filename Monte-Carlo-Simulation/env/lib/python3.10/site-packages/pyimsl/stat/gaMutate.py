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

IMSLS_PRINT = 13900
IMSLS_SWAP_MUTATION = 50740
imslstat = loadimsl(STAT)


def gaMutate(p, individual, t_print=None, swapMutation=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ga_mutate.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_ga_mutate('
    evalstring += 'c_double(p)'
    evalstring += ','
    evalstring += 'individual'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    checkForBoolean(swapMutation, 'swapMutation')
    if (swapMutation):
        evalstring += ','
        evalstring += repr(IMSLS_SWAP_MUTATION)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
