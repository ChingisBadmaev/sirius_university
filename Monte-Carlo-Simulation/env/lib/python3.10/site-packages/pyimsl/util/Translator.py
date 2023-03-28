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


class Translator (object):
    """ This class is responsible for loading and translating message strings.
        The implementation details are handled by the __impl class, to
        provide singleton behavior.

        Basic usage:
            str = Translator.getString ("foo")
        TODO: Figure out what to do with the CNL message file.
    """
    class __impl:
        def __init__(self):
            # There is probably a more efficient way to do this...
            # Basically, we want to force the search for localized
            # files to start in a subdirectory of "pyimsl".
            # The "imsl" directory should be located somewhere under
            # sys.path.
            # If for some reason we can't locate the "pyimsl" directory,
            # use "." as the default.
            self.imslDir = "."
            import sys
            import os
            import gettext
            import locale
            # ++Windows HACK: Windows requires the LANG environment
            # variable.
            if (os.name == "nt"):
                lang = os.getenv("LANG")
                if (lang is None):
                    default_lang, default_enc = locale.getdefaultlocale()
                    if (default_lang):
                        lang = default_lang
                    else:
                        os.environ["LANG"] = lang
            # --Windows HACK
#            locale.setlocale (locale.LC_ALL, '')
            for dir in sys.path:
                testDir = dir + os.sep + "pyimsl"
                localeDir = testDir + os.sep + "locale"
                if os.path.exists(localeDir):
                    self.imslDir = testDir
                    break
            self.localeDir = self.imslDir + os.sep + "locale"
#            print "Obtaining localized strings from: ", self.localeDir
            if (not(os.path.exists(self.localeDir))):
                #                print "localeDir does NOT exist"
                self.gtTranslator = None
                return
            # NOTE: translation() calls find() to locate the .mo files
            # The files should be in localedir/language/LC_MESSAGES/domain.mo
            # where "domain" is the first argument to translation() or find()
#            self.gtTranslator = gettext.translation ("pnl", self.localeDir,languages=['en'])
            loc = locale.getlocale()
            if (loc[0] is None):       # No current locale
                #                print "Current locale is not set"
                dl = locale.getdefaultlocale()
                if (dl[0] is None):
                    #                    print "No default locale is set.  Defaulting to en_US."
                    lang = "en_US"
                else:
                    lang = dl[0]
            else:
                lang = loc[0]
#            print "Obtaining messages for language: ", lang
            if (lang == 'en_US'):
                languages = ['en_US']
            else:
                languages = [lang, 'en_US']
#            self.gtTranslator = gettext.translation ("pnl", self.localeDir, languages=['en_US'])
#            translationFile = gettext.find ("pnl", self.localeDir, languages=['en_US'])
            translationFile = gettext.find(
                "pnl", self.localeDir, languages=languages)
#            print "translationFile: ", translationFile
            self.gtTranslator = gettext.translation(
                "pnl", self.localeDir, languages=languages, fallback=['en_US'])
            loc = translationFile.rfind(os.sep)
            self.translationDir = translationFile[0:loc]

#            print "test translation: ", self.gtTranslator.lgettext("test")
#            print "test2 translation: ", self.gtTranslator.ugettext ("test2")

        def getString(self, key):
            if (self.gtTranslator is None):
                return key
            else:
                text = self.gtTranslator.lgettext(key)
                if (isinstance(text, bytes)):
                    text = bytes.decode(text)
                return text

        def getTranslationDir(self):
            if (self.gtTranslator is None):
                return None
            else:
                return self.translationDir

    __translatorImpl = None

    def __init__(self):
        if (Translator.__translatorImpl is None):
            Translator.__translatorImpl = Translator.__impl()

    def getString(key):
        if (Translator.__translatorImpl is None):
            Translator.__translatorImpl = Translator.__impl()
        return Translator.__translatorImpl.getString(key)

    def getTranslationDir():
        if (Translator.__translatorImpl is None):
            Translator.__translatorImpl = Translator.__impl()
        return Translator.__translatorImpl.getTranslationDir()

    getString = staticmethod(getString)
    getTranslationDir = staticmethod(getTranslationDir)
