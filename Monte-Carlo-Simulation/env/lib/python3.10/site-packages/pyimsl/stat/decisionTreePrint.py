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

IMSLS_RESP_NAME = 50925
IMSLS_VAR_NAMES = 50922
IMSLS_CLASS_NAMES = 50923
IMSLS_CATEG_NAMES = 50924
IMSLS_PRINT_MAX = 50932
imslstat = loadimsl(STAT)


def decisionTreePrint(tree, respName=None, varNames=None, classNames=None, categNames=None, printMax=None):
    """ Prints a decision tree.
    """
    imslstat.imsls_d_decision_tree_print.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_decision_tree_print('
    # tree = toNumpyArray(tree, 'tree', shape=shape, dtype='struct', expectedShape=(1))
    # evalstring +='tree.ctypes.data_as(c_void_p)'
    evalstring += 'tree'
    if not (respName is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESP_NAME)
        evalstring += ','
        rName = (c_char_p * len(respName))()
        for i in range(0, len(respName)):
            rName[i] = toByte(respName[i])
        evalstring += 'rName'
    if not (varNames is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_NAMES)
        evalstring += ','
        vNames = (c_char_p * len(varNames))()
        for i in range(0, len(varNames)):
            vNames[i] = toByte(varNames[i])
        evalstring += 'vNames'
    if not (classNames is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLASS_NAMES)
        evalstring += ','
        clNames = (c_char_p * len(classNames))()
        for i in range(0, len(classNames)):
            clNames[i] = toByte(classNames[i])
        evalstring += 'clNames'
    if not (categNames is None):
        evalstring += ','
        evalstring += repr(IMSLS_CATEG_NAMES)
        evalstring += ','
        catNames = (c_char_p * len(categNames))()
        for i in range(0, len(categNames)):
            catNames[i] = toByte(categNames[i])
        evalstring += 'catNames'
    checkForBoolean(printMax, 'printMax')
    if (printMax):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_MAX)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
