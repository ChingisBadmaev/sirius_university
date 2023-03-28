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
import copy

from pyimsl.math.version import LIBRARY_VERSION, version
from pyimsl.util.Translator import Translator


class VersionFacade (object):
    """ This class represents a version number, including
        major, minor, and sub numbers.  It also includes
        utilities for getting the current CNL version number
        and parsing version strings.
        Much of the work of the class is done in the __impl
        class, so we can have something that behaves like
        a singleton when necessary.

        Usage:
        from pyimsl.util.VersionFacade import VersionFacade
        v = VersionFacade()    # Default constructor, version 0,0,0
        v2 = VersionFacade.getCnlVersion()  # Get the current CNL version
        print "Version: ", v2.majorVersion, v2.minorVersion, v2.subVersion
        print v2.versionString
    """

    def __init__(self, getCurrentCnlVersion=False, versionString=None):
        """ Constructor.
            If getCurrentCnlVersion is True, populate the
            object with the current CNL version.
            Otherwise, if versionString is supplied, parse it
            as if it were a CNL version string
            and use the parsed values to populate the object.
            Otherwise, set the version to (0,0,0).
        """
        if getCurrentCnlVersion:
            cnl_version = VersionFacade.getCnlVersion()
            self.majorVersion = cnl_version.majorVersion
            self.minorVersion = cnl_version.minorVersion
            self.subVersion = cnl_version.subVersion
            self.versionString = cnl_version.versionString
        elif versionString is not None:
            self._fromString(versionString)
        else:
            self.setVersion(0, 0, 0)

    def _fromString(self, versionString):
        self.versionString = versionString
        # Assume the last component of the input string is the version
        versionString = versionString.split()[-1]

        versionString = versionString.split('.')
        versionString = [int(ver) for ver in versionString]
        versionString += ([0] * (3 - len(versionString)))
        self.majorVersion = versionString[0]
        self.minorVersion = versionString[1]
        self.subVersion = versionString[2]

    def setVersion(self, majorVersion=0, minorVersion=0, subVersion=0):
        """ Set the version number.
        """
        self.majorVersion = int(majorVersion)
        self.minorVersion = int(minorVersion)
        self.subVersion = int(subVersion)
        self.versionString = '{}.{}.{}'.format(self.majorVersion,
                                               self.minorVersion,
                                               self.subVersion)

    __cnlVersion = None

    @staticmethod
    def getCnlVersion():
        """ Virtual constructor that returns
            the current CNL version in a new object.
        """
        if VersionFacade.__cnlVersion is None:
            cnl = version(LIBRARY_VERSION)
            VersionFacade.__cnlVersion = VersionFacade(versionString=cnl)
        return copy.copy(VersionFacade.__cnlVersion)

    @staticmethod
    def checkVersion(majorVersionNum=6,
                     minorVersionNum=0,
                     subVersionNum=0):
        """ Check to see if the current version of math/stat
            is greater than or equal to the version number passed in.
            If the current version is less than the requested
            version, this routine will throw an exception.
            Note that the math routine (imsl_version) is being
            called to obtain the version number.
        """
        cnlVersion = VersionFacade.getCnlVersion()
        version = (int(majorVersionNum),
                   int(minorVersionNum),
                   int(subVersionNum))

        if cnlVersion._version_tuple < version:
            errstr = Translator.getString("cnlver1")
            errstr2 = Translator.getString("cnlver2")
            msg = '{errstr}{major}.{minor}.{sub}{errstr2}{version}'
            msg = msg.format(errstr=errstr,
                             errstr2=errstr2,
                             major=majorVersionNum,
                             minor=minorVersionNum,
                             sub=subVersionNum,
                             version=cnlVersion.versionString)
            raise RuntimeError(msg)

    @property
    def _version_tuple(self):
        return (self.majorVersion, self.minorVersion, self.subVersion)

    def __repr__(self):
        return 'VersionFacade({})'.format(self.versionString)

    def __eq__(self, rhs):
        return self._version_tuple == rhs._version_tuple

    def __lt__(self, rhs):
        return self._version_tuple < rhs._version_tuple

    def __le__(self, rhs):
        return self._version_tuple <= rhs._version_tuple
