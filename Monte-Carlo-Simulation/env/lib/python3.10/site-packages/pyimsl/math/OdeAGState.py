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
from pyimsl.util.CnlState import CnlState
from pyimsl.util.CnlCtypesWrapper import CnlCtypesWrapper
from pyimsl.util.Translator import Translator


class OdeAGState (CnlState):
    """ This class is used to encapsulate the state variable used
        by odeAdamsGearMgr and odeAdamsGear, along with the
        variables that are modified during odeRungeKutta exection
        (nstep, nfcn, and nfcnj).
    """

    def __init__(self, state):
        CnlState.__init__(self, state)
        self.__nstep__ = None
        self.__nfcnj__ = None
        self.__nfcn__ = None
        self.__jacobianFcn__ = None

    def reset(self):
        self.setState(None)
        if (not(self.__nstep__ is None)):
            self.__nstep__.setCtValue(None)
        if (not(self.__nfcn__ is None)):
            self.__nfcn__.setCtValue(None)
        if (not(self.__nfcnj__ is None)):
            self.__nfcnj__.setCtValue(None)
        if (not(self.__jacobianFcn__ is None)):
            self.__jacobianFcn__ = None

    def _setNstep(self, nstep):
        self.__nstep__ = CnlCtypesWrapper(nstep)

    def getNstep(self):
        if (self.state is None) or (self.__nstep__ is None):
            errStr = Translator.getString("varnotavailable")
            raise ValueError(errStr)
        return self.__nstep__

    def _setNfcn(self, nfcn):
        self.__nfcn__ = CnlCtypesWrapper(nfcn)

    def getNfcn(self):
        if (self.state is None) or (self.__nfcn__ is None):
            errStr = Translator.getString("varnotavailable")
            raise ValueError(errStr)
        return self.__nfcn__

    def _setNfcnj(self, nfcnj):
        self.__nfcnj__ = CnlCtypesWrapper(nfcnj)

    def getNfcnj(self):
        if (self.state is None) or (self.__nfcnj__ is None):
            errStr = Translator.getString("varnotavailable")
            raise ValueError(errStr)
        return self.__nfcnj__

    def _setJacobianFcn(self, fcn):
        self.__jacobianFcn__ = fcn

    nstep = property(getNstep, doc='Number of steps')
    nfcn = property(getNfcn, doc='Number of function evaluations')
    nfcnj = property(getNfcnj, doc='Current trial step size')
