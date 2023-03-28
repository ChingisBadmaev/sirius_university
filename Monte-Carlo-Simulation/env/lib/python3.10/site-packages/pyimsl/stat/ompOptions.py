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

IMSLS_SET_FUNCTIONS_THREAD_SAFE = 50741
IMSLS_GET_FUNCTIONS_THREAD_SAFE = 50742
imslstat = loadimsl(STAT)


def ompOptions(setFunctionsThreadSafe=None, getFunctionsThreadSafe=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_omp_options.restype = None
    shape = []
    evalstring = 'imslstat.imsls_omp_options('
    if not (setFunctionsThreadSafe is None):
        evalstring += repr(IMSLS_SET_FUNCTIONS_THREAD_SAFE)
        evalstring += ','
        evalstring += 'c_int(setFunctionsThreadSafe)'
    if not (getFunctionsThreadSafe is None):
        if not (setFunctionsThreadSafe is None):
            evalstring += ','
        evalstring += repr(IMSLS_GET_FUNCTIONS_THREAD_SAFE)
        checkForList(getFunctionsThreadSafe, 'getFunctionsThreadSafe')
        evalstring += ','
        getFunctionsThreadSafe_psetting_tmp = c_int()
        evalstring += 'byref(getFunctionsThreadSafe_psetting_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (getFunctionsThreadSafe is None):
        processRet(getFunctionsThreadSafe_psetting_tmp,
                   shape=(1), pyvar=getFunctionsThreadSafe)
    return
