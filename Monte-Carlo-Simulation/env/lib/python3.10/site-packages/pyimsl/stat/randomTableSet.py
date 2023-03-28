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
from numpy import double, dtype, shape
from ctypes import c_void_p

imslstat = loadimsl(STAT)


def randomTableSet(table):
    """ Sets the current table used in the shuffled generator.
    """
    imslstat.imsls_d_random_table_set.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_random_table_set('
    table = toNumpyArray(table, 'table', shape=shape,
                         dtype='double', expectedShape=(0))
    if (table[0] is None):
        evalstring += 'None'
    else:
        evalstring += 'table.ctypes.data_as(c_void_p)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
