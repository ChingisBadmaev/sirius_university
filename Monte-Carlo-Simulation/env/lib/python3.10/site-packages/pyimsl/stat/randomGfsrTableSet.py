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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import dtype, int, shape
from ctypes import c_void_p

imslstat = loadimsl(STAT)


def randomGfsrTableSet(table):
    imslstat.imsls_random_GFSR_table_set.restype = None
    shape = []
    evalstring = 'imslstat.imsls_random_GFSR_table_set('
    table = toNumpyArray(table, 'table', shape=shape,
                         dtype='int', expectedShape=(1565))
    evalstring += 'table.ctypes.data_as(c_void_p)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
