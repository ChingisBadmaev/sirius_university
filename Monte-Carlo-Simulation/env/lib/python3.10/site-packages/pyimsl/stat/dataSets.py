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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, byref, c_double, c_int

IMSLS_X_COL_DIM = 15470
IMSLS_N_OBSERVATIONS = 15640
IMSLS_N_VARIABLES = 15650
IMSLS_PRINT_NONE = 13950
IMSLS_PRINT_BRIEF = 13920
IMSLS_PRINT_ALL = 13910
imslstat = loadimsl(STAT)


def dataSets(dataSetChoice, xColDim=None, nObservations=None, nVariables=None, printNone=None, printBrief=None, printAll=None):
    """ Retrieves a commonly analyzed data set.
    """
    imslstat.imsls_d_data_sets.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_data_sets('
    evalstring += 'c_int(dataSetChoice)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    # always include these keywords as we need the values for processRet:
    if not (nObservations is None):
        checkForList(nObservations, 'nObservations')
    if not (nVariables is None):
        checkForList(nVariables, 'nVariables')
    evalstring += ','
    evalstring += repr(IMSLS_N_OBSERVATIONS)
    evalstring += ','
    nObservations_nObservations_tmp = c_int()
    evalstring += 'byref(nObservations_nObservations_tmp)'
    evalstring += ','
    evalstring += repr(IMSLS_N_VARIABLES)
    evalstring += ','
    nVariables_nVariables_tmp = c_int()
    evalstring += 'byref(nVariables_nVariables_tmp)'
    checkForBoolean(printNone, 'printNone')
    if (printNone):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_NONE)
    checkForBoolean(printBrief, 'printBrief')
    if (printBrief):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_BRIEF)
    checkForBoolean(printAll, 'printAll')
    if (printAll):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_ALL)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nObservations is None):
        processRet(nObservations_nObservations_tmp,
                   shape=1, pyvar=nObservations)
    if not (nVariables is None):
        processRet(nVariables_nVariables_tmp, shape=1, pyvar=nVariables)
    return processRet(result, shape=(nObservations_nObservations_tmp.value, nVariables_nVariables_tmp.value), result=True)
