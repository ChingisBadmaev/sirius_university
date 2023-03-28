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
from .statStructs import Imsls_d_apriori_itemsets
from .statStructs import Imsls_d_association_rules

imslstat = loadimsl(STAT)


def writeAssociationRules(assocRules):
    """ Prints association rules.
    """
    imslstat.imsls_d_write_association_rules.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_write_association_rules('
    # assocRules = toNumpyArray(assocRules, 'assocRules', shape=shape, dtype='struct', expectedShape=(1))
    # evalstring +='assocRules.ctypes.data_as(c_void_p)'
    evalstring += 'assocRules'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
