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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl
from pyimsl.util.VersionFacade import VersionFacade
from numpy import shape
from ctypes import POINTER, c_int
from pyimsl.util.VersionFacade import VersionFacade
ver = VersionFacade.getCnlVersion()
if ver.majorVersion == 6:
    from .statStructs6 import Imsls_d_NN_Network
else:
    from .statStructs import Imsls_d_NN_Network
imslstat = loadimsl(STAT)


def mlffNetworkInit(nInputs, nOutputs):
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_mlff_network_init.restype = POINTER(Imsls_d_NN_Network)
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_network_init('
    evalstring += 'c_int(nInputs)'
    evalstring += ','
    evalstring += 'c_int(nOutputs)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
