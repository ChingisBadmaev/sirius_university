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
from ctypes import c_double
from numpy import empty, double
from pyimsl.util.CnlState import CnlState
from pyimsl.util.CnlCtypesWrapper import CnlCtypesWrapper
from pyimsl.util.Translator import Translator


class DeaPGState (CnlState):
    """ This class is used to encapsulate the state variable used
            by deaPetzoldGearMgr and deaPetzoldGear, and
            functions that are defined in the manager and
            used in deaPetzoldGear.  This is to avoid accidental
            garbage collection.
    """

    def __init__(self, state):
        CnlState.__init__(self, state)
        self.__jacobianFcn__ = None
        self.__normFcn__ = None
        self.__userJacFactorSolveFcn__ = None

    def reset(self):
        self.setState(None)
        if (not(self.__jacobianFcn__ is None)):
            self.__jacobianFcn__ = None
        if (not(self.__normFcn__ is None)):
            self.__normFcn__ = None
        if (not(self.__userJacFactorSolveFcn__ is None)):
            self.__userJacFactorSolveFcn__ = None

    def _setJacobianFcn(self, fcn):
        self.__jacobianFcn__ = fcn

        def _setNormFcn(self, fcn):
            self.__normFcn__ = fcn

    def _setUserJacFactorSolveFcn(self, fcn):
        self.__userJacFactorSolveFcn__ = fcn
