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
from numpy import dtype, int, shape
from ctypes import POINTER, c_int, c_void_p

imslstat = loadimsl(STAT)


def randomTableTwoway(nrtot, nctot):
    """ Generates a pseudorandom two-way table.
    """
    imslstat.imsls_random_table_twoway.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_random_table_twoway('
    evalstring += 'c_int(nrow)'
    evalstring += ','
    evalstring += 'c_int(ncol)'
    evalstring += ','
    nrtot = toNumpyArray(nrtot, 'nrtot', shape=shape,
                         dtype='int', expectedShape=(0))
    evalstring += 'nrtot.ctypes.data_as(c_void_p)'
    nrow = shape[0]
    evalstring += ','
    nctot = toNumpyArray(nctot, 'nctot', shape=shape,
                         dtype='int', expectedShape=(0))
    evalstring += 'nctot.ctypes.data_as(c_void_p)'
    ncol = shape[0]
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nrow, ncol), result=True)
