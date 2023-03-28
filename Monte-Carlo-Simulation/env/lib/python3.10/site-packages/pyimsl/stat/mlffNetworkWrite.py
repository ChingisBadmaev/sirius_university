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
from .statStructs import Imsls_d_NN_Network
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_PRINT = 13900
IMSLS_FILE = 40621
imslstat = loadimsl(STAT)


def mlffNetworkWrite(network, filename, t_print=None, file=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_mlff_network_write.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_network_write('
    evalstring += 'network'
    evalstring += ','
    if not (file is None):
        evalstring += 'None'
    else:
        checkForStr(filename, 'filename')
        evalstring += 'toByte(filename)'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    if not (file is None):
        evalstring += ','
        evalstring += repr(IMSLS_FILE)
        evalstring += ','
        evalstring += 'c_void_p(file)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
