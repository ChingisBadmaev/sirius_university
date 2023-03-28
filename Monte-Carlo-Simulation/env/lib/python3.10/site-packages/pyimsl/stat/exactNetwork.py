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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, checkForDict, processRet
from numpy import double, dtype, shape, size
from ctypes import byref, c_double, c_int, c_void_p

IMSLS_PROB_TABLE = 20610
IMSLS_P_VALUE = 20620
IMSLS_APPROXIMATION_PARAMETERS = 20650
IMSLS_NO_APPROXIMATION = 20660
IMSLS_WORKSPACE = 20640
imslstat = loadimsl(STAT)


def exactNetwork(table, probTable=None, pValue=None, approximationParameters=None, noApproximation=None, workspace=None):
    """ Computes Fisher exact probabilities and a hybrid approximation of the Fisher exact method for a two-way contingency table using the network algorithm.
    """
    imslstat.imsls_d_exact_network.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_exact_network('
    evalstring += 'c_int(nRows)'
    evalstring += ','
    evalstring += 'c_int(nColumns)'
    evalstring += ','
    table = toNumpyArray(table, 'table', shape=shape,
                         dtype='double', expectedShape=(0, 0))
    evalstring += 'table.ctypes.data_as(c_void_p)'
    nRows = shape[0]
    nColumns = shape[1]
    if not (probTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_PROB_TABLE)
        checkForList(probTable, 'probTable')
        evalstring += ','
        probTable_prt_tmp = c_double()
        evalstring += 'byref(probTable_prt_tmp)'
    if not (pValue is None):
        evalstring += ','
        evalstring += repr(IMSLS_P_VALUE)
        checkForList(pValue, 'pValue')
        evalstring += ','
        pValue_pValue_tmp = c_double()
        evalstring += 'byref(pValue_pValue_tmp)'
    if not (approximationParameters is None):
        evalstring += ','
        evalstring += repr(IMSLS_APPROXIMATION_PARAMETERS)
        checkForDict(approximationParameters, 'approximationParameters', [
                     'expect', 'percent', 'expectedMinimum'])
        evalstring += ','
        approximationParameters_expect_tmp = approximationParameters['expect']
        evalstring += 'c_double(approximationParameters_expect_tmp)'
        evalstring += ','
        approximationParameters_percent_tmp = approximationParameters['percent']
        evalstring += 'c_double(approximationParameters_percent_tmp)'
        evalstring += ','
        approximationParameters_expectedMinimum_tmp = approximationParameters['expectedMinimum']
        evalstring += 'c_double(approximationParameters_expectedMinimum_tmp)'
    checkForBoolean(noApproximation, 'noApproximation')
    if (noApproximation):
        evalstring += ','
        evalstring += repr(IMSLS_NO_APPROXIMATION)
    if not (workspace is None):
        evalstring += ','
        evalstring += repr(IMSLS_WORKSPACE)
        checkForDict(workspace, 'workspace', [
                     'factor1', 'factor2', 'maxAttempts'])
        evalstring += ','
        workspace_factor1_tmp = workspace['factor1']
        evalstring += 'c_int(workspace_factor1_tmp)'
        evalstring += ','
        workspace_factor2_tmp = workspace['factor2']
        evalstring += 'c_int(workspace_factor2_tmp)'
        evalstring += ','
        workspace_maxAttempts_tmp = workspace['maxAttempts']
        evalstring += 'c_int(workspace_maxAttempts_tmp)'
        evalstring += ','
        workspace_nAttempts_tmp = c_int()
        evalstring += 'byref(workspace_nAttempts_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (probTable is None):
        processRet(probTable_prt_tmp, shape=(1), pyvar=probTable)
    if not (pValue is None):
        processRet(pValue_pValue_tmp, shape=(1), pyvar=pValue)
    if not (workspace is None):
        processRet(workspace_nAttempts_tmp, shape=(
            1), key='nAttempts', pyvar=workspace)
    return result
