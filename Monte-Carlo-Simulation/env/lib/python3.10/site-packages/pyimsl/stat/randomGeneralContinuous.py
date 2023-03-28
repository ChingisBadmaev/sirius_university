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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_TABLE_COL_DIM = 40005
imslstat = loadimsl(STAT)


def randomGeneralContinuous(nRandom, table, tableColDim=None):
    """ Generates pseudorandom numbers from a general continuous distribution.
    """
    imslstat.imsls_d_random_general_continuous.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_general_continuous('
    evalstring += 'c_int(nRandom)'
    evalstring += ','
    evalstring += 'c_int(ndata)'
    evalstring += ','
    table = toNumpyArray(table, 'table', shape=shape,
                         dtype='double', expectedShape=(0, 5))
    evalstring += 'table.ctypes.data_as(c_void_p)'
    ndata = shape[0]
    if not (tableColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_TABLE_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(tableColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nRandom), result=True)
