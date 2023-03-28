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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_Q_STATISTIC = 20600
imslstat = loadimsl(STAT)


def cochranQTest(x, xColDim=None, qStatistic=None):
    """ Performs a Cochran Q test for related observations.
    """
    imslstat.imsls_d_cochran_q_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_cochran_q_test('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nVariables = shape[1]
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (qStatistic is None):
        evalstring += ','
        evalstring += repr(IMSLS_Q_STATISTIC)
        checkForList(qStatistic, 'qStatistic')
        evalstring += ','
        qStatistic_q_tmp = c_double()
        evalstring += 'byref(qStatistic_q_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (qStatistic is None):
        processRet(qStatistic_q_tmp, shape=1, pyvar=qStatistic)
    return result
