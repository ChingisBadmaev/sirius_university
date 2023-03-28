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


class pde1dMgState (CnlState):
    """ This class is used to encapsulate the state variable used
        by pde1dMgMgr and pde1dMg, along with the
        variables that are modified during odeRungeKutta exection
        (nstep, nfcn, nfcnj, nerror_test_failures,
        nconv_test_failures, and condition).
    """

    def __init__(self, state):
        CnlState.__init__(self, state)
        self.__t__ = None
        self.__u__ = None
        self.__initialConditionsFcn__ = None
        self.__userFactorSolveFacFcn__ = None
        self.__userFactorSolveFcn__ = None

    def reset(self):
        self.setState(None)
        if (not(self.__t__ is None)):
            self.__t__ = None
        if (not(self.__u__ is None)):
            self.__u__ = None

        if (not(self.__initialConditionsFcn__ is None)):
            self.__initialConditionsFcn__ = None

        if (not(self.__userFactorSolveFacFcn__ is None)):
            self.__userFactorSolveFacFcn__ = None
        if (not(self.__userFactorSolveFcn__ is None)):
            self.__userFactorSolveFcn__ = None

    def _setT(self, t):
        if (self.__t__ is None):
            self.__t__ = c_double(t)
        else:
            self.__t__.value = t

    def _getTObject(self):
        if (self.state is None) or (self.__t__ is None):
            errStr = Translator.getString("varnotavailable")
            raise ValueError(errStr)
        return self.__t__

    def getT(self):
        if (self.state is None) or (self.__t__ is None):
            errStr = Translator.getString("varnotavailable")
            raise ValueError(errStr)
        return self.__t__.value

    def _setU(self, u, nx, ny):
        if (self.__u__ is None):
            self.__u__ = empty((nx, ny), dtype=double)
        for i in range(0, nx):
            for j in range(0, ny):
                self.__u__[i, j] = u[i, j]

    def _getUObject(self):
        if (self.state is None) or (self.__u__ is None):
            errStr = Translator.getString("varnotavailable")
            raise ValueError(errStr)
        return self.__u__

    def getU(self, u, nx, ny):
        if (self.state is None) or (self.__u__ is None):
            errStr = Translator.getString("varnotavailable")
            raise ValueError(errStr)
        for i in range(0, nx):
            for j in range(0, ny):
                u[i, j] = self.__u__[i, j]

    t = property(getT, doc='Independent variable value')

    def _setInitialConditionsFcn(self, fcn):
        self.__initialConditionsFcn__ = fcn

    def _setUserFactorSolveFcn(self, facfcn, fcn):
        self.__userFactorSolveFacFcn__ = facfcn
        self.__userFactorSolveFcn__ = fcn
