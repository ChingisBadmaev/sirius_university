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
from .adNormalityTest import adNormalityTest
from .aggrApriori import aggrApriori
from .ancovar import ancovar
from .anovaBalanced import anovaBalanced
from .anovaFactorial import anovaFactorial
from .anovaNested import anovaNested
from .anovaOneway import anovaOneway
from .apriori import apriori
from .arma import arma
from .armaForecast import armaForecast
from .autoArima import autoArima
from .autoParm import autoParm
from .autoUniAr import autoUniAr
from .autocorrelation import autocorrelation
from .bayesianSeasonalAdj import bayesianSeasonalAdj
from .beta import beta
from .betaCdf import betaCdf
from .betaIncomplete import betaIncomplete
from .betaInverseCdf import betaInverseCdf
from .binomialCdf import binomialCdf
from .binomialCoefficient import binomialCoefficient
from .binomialPdf import binomialPdf
from .bivariateNormalCdf import bivariateNormalCdf
from .boxCoxTransform import boxCoxTransform
from .canonicalCorrelation import canonicalCorrelation
from .categoricalGlm import categoricalGlm
from .chiSquaredCdf import chiSquaredCdf
from .chiSquaredInverseCdf import chiSquaredInverseCdf
from .chiSquaredNormalityTest import chiSquaredNormalityTest
from .chiSquaredTest import chiSquaredTest
from .clusterHierarchical import clusterHierarchical
from .clusterKMeans import clusterKMeans
from .clusterNumber import clusterNumber
from .cochranQTest import cochranQTest
from .complementaryChiSquaredCdf import complementaryChiSquaredCdf
from .complementaryFCdf import complementaryFCdf
from .complementaryNonCentralFCdf import complementaryNonCentralFCdf
from .complementaryTCdf import complementaryTCdf
from .contingencyTable import contingencyTable
from .continuousTableSetup import continuousTableSetup
from .covariances import covariances
from .coxStuartTrendsTest import coxStuartTrendsTest
from .crdFactorial import crdFactorial
from .crosscorrelation import crosscorrelation
from .ctime import ctime
from .cvmNormalityTest import cvmNormalityTest
from .dataSets import dataSets
from .decisionTree import decisionTree
from .decisionTreeFree import decisionTreeFree
from .decisionTreePredict import decisionTreePredict
from .decisionTreePrint import decisionTreePrint
from .difference import difference
from .discreteTableSetup import discreteTableSetup
from .discreteUniformCdf import discreteUniformCdf
from .discreteUniformInverseCdf import discreteUniformInverseCdf
from .discreteUniformPdf import discreteUniformPdf
from .discriminantAnalysis import discriminantAnalysis
from .dissimilarities import dissimilarities
from .empiricalQuantiles import empiricalQuantiles
from .errorCode import errorCode
from .errorMessage import errorMessage
from .errorOptions import errorOptions
from .errorType import errorType
from .estimateMissing import estimateMissing
from .exactEnumeration import exactEnumeration
from .exactNetwork import exactNetwork
from .exponentialCdf import exponentialCdf
from .exponentialInverseCdf import exponentialInverseCdf
from .exponentialPdf import exponentialPdf
from .fCdf import fCdf
from .fInverseCdf import fInverseCdf
from .factorAnalysis import factorAnalysis
from .falseDiscoveryRates import falseDiscoveryRates
from .faureNextPoint import faureNextPoint
from .faureSequenceFree import faureSequenceFree
from .faureSequenceInit import faureSequenceInit
from .fclose import fclose
from .fopen import fopen
from .free import free
from .freeAprioriItemsets import freeAprioriItemsets
from .freeAssociationRules import freeAssociationRules
from .friedmansTest import friedmansTest
from .gaChromosome import gaChromosome
from .gaCloneChromosome import gaCloneChromosome
from .gaCloneIndividual import gaCloneIndividual
from .gaClonePopulation import gaClonePopulation
from .gaCopyChromosome import gaCopyChromosome
from .gaCopyIndividual import gaCopyIndividual
from .gaCopyPopulation import gaCopyPopulation
from .gaDecode import gaDecode
from .gaEncode import gaEncode
from .gaFreeIndividual import gaFreeIndividual
from .gaFreePopulation import gaFreePopulation
from .gaGrowPopulation import gaGrowPopulation
from .gaIndividual import gaIndividual
from .gaMergePopulation import gaMergePopulation
from .gaMutate import gaMutate
from .gaPopulation import gaPopulation
from .gaRandomPopulation import gaRandomPopulation
from .gamma import gamma
from .gammaCdf import gammaCdf
from .gammaIncomplete import gammaIncomplete
from .gammaInverseCdf import gammaInverseCdf
from .garch import garch
from .geneticAlgorithm import geneticAlgorithm
from .geometricCdf import geometricCdf
from .geometricInverseCdf import geometricInverseCdf
from .geometricPdf import geometricPdf
from .homogeneity import homogeneity
from .hwTimeSeries import hwTimeSeries
from .hypergeometricCdf import hypergeometricCdf
from .hypergeometricPdf import hypergeometricPdf
from .hypothesisPartial import hypothesisPartial
from .hypothesisScph import hypothesisScph
from .hypothesisTest import hypothesisTest
from .iMachine import iMachine
from .imputeMissing import imputeMissing
from .initialize import initialize
from .initializeErrorHandler import initializeErrorHandler
from .kTrendsTest import kTrendsTest
from .kalman import kalman
from .kaplanMeierEstimates import kaplanMeierEstimates
from .kohonenSOMForecast import kohonenSOMForecast
from .kohonenSOMTrainer import kohonenSOMTrainer
from .kolmogorovOne import kolmogorovOne
from .kolmogorovTwo import kolmogorovTwo
from .kruskalWallisTest import kruskalWallisTest
from .lackOfFit import lackOfFit
from .latinSquare import latinSquare
from .lattice import lattice
from .lifeTables import lifeTables
from .lillieforsNormalityTest import lillieforsNormalityTest
from .lnormRegression import lnormRegression
from .logBeta import logBeta
from .logGamma import logGamma
from .logisticRegPredict import logisticRegPredict
from .logisticRegression import logisticRegression
from .lognormalCdf import lognormalCdf
from .lognormalInverseCdf import lognormalInverseCdf
from .lognormalPdf import lognormalPdf
from .machine import machine
from .matMulRect import matMulRect
from .maxArma import maxArma
from .maxLikelihoodEstimates import maxLikelihoodEstimates
from .mlffClassificationTrainer import mlffClassificationTrainer
from .mlffInitializeWeights import mlffInitializeWeights
from .mlffNetwork import mlffNetwork
from .mlffNetworkForecast import mlffNetworkForecast
from .mlffNetworkFree import mlffNetworkFree
from .mlffNetworkInit import mlffNetworkInit
from .mlffNetworkRead import mlffNetworkRead
from .mlffNetworkTrainer import mlffNetworkTrainer
from .mlffNetworkWrite import mlffNetworkWrite
from .mlffPatternClassification import mlffPatternClassification
from .multiCrosscorrelation import multiCrosscorrelation
from .multipleComparisons import multipleComparisons
from .multivarNormalityTest import multivarNormalityTest
from .multivariateNormalCdf import multivariateNormalCdf
from .naiveBayesClassification import naiveBayesClassification
from .naiveBayesTrainer import naiveBayesTrainer
from .nbClassifierFree import nbClassifierFree
from .nbClassifierRead import nbClassifierRead
from .nbClassifierWrite import nbClassifierWrite
from .noetherCyclicalTrend import noetherCyclicalTrend
from .nonCentralBetaCdf import nonCentralBetaCdf
from .nonCentralBetaInverseCdf import nonCentralBetaInverseCdf
from .nonCentralBetaPdf import nonCentralBetaPdf
from .nonCentralChiSq import nonCentralChiSq
from .nonCentralChiSqInv import nonCentralChiSqInv
from .nonCentralChiSqPdf import nonCentralChiSqPdf
from .nonCentralFCdf import nonCentralFCdf
from .nonCentralFInverseCdf import nonCentralFInverseCdf
from .nonCentralFPdf import nonCentralFPdf
from .nonCentralTCdf import nonCentralTCdf
from .nonCentralTInvCdf import nonCentralTInvCdf
from .nonCentralTPdf import nonCentralTPdf
from .nonlinearOptimization import nonlinearOptimization
from .nonlinearRegression import nonlinearRegression
from .nonparamHazardRate import nonparamHazardRate
from .normalCdf import normalCdf
from .normalInverseCdf import normalInverseCdf
from .normalOneSample import normalOneSample
from .normalTwoSample import normalTwoSample
from .normalityTest import normalityTest
from .ompOptions import ompOptions
from .outputFile import outputFile
from .page import page
from .paretoCdf import paretoCdf
from .paretoPdf import paretoPdf
from .partialAutocorrelation import partialAutocorrelation
from .partialCovariances import partialCovariances
from .permuteMatrix import permuteMatrix
from .permuteVector import permuteVector
from .plsRegression import plsRegression
from .poissonCdf import poissonCdf
from .poissonPdf import poissonPdf
from .polyPrediction import polyPrediction
from .polyRegression import polyRegression
from .pooledCovariances import pooledCovariances
from .principalComponents import principalComponents
from .propHazardsGenLin import propHazardsGenLin
from .randomArma import randomArma
from .randomBeta import randomBeta
from .randomBinomial import randomBinomial
from .randomCauchy import randomCauchy
from .randomChiSquared import randomChiSquared
from .randomExponential import randomExponential
from .randomExponentialMix import randomExponentialMix
from .randomGamma import randomGamma
from .randomGeneralContinuous import randomGeneralContinuous
from .randomGeneralDiscrete import randomGeneralDiscrete
from .randomGeometric import randomGeometric
from .randomGfsrTableGet import randomGfsrTableGet
from .randomGfsrTableSet import randomGfsrTableSet
from .randomHypergeometric import randomHypergeometric
from .randomLogarithmic import randomLogarithmic
from .randomLognormal import randomLognormal
from .randomMt32Init import randomMt32Init
from .randomMt32TableGet import randomMt32TableGet
from .randomMt32TableSet import randomMt32TableSet
from .randomMt64Init import randomMt64Init
from .randomMt64TableGet import randomMt64TableGet
from .randomMt64TableSet import randomMt64TableSet
from .randomMultinomial import randomMultinomial
from .randomMvarFromData import randomMvarFromData
from .randomMvarGaussianCopula import randomMvarGaussianCopula
from .randomMvarTCopula import randomMvarTCopula
from .randomNegBinomial import randomNegBinomial
from .randomNormal import randomNormal
from .randomNormalMultivariate import randomNormalMultivariate
from .randomNpp import randomNpp
from .randomOption import randomOption
from .randomOptionGet import randomOptionGet
from .randomOrderNormal import randomOrderNormal
from .randomOrderUniform import randomOrderUniform
from .randomOrthogonalMatrix import randomOrthogonalMatrix
from .randomPermutation import randomPermutation
from .randomPoisson import randomPoisson
from .randomSample import randomSample
from .randomSampleIndices import randomSampleIndices
from .randomSeedGet import randomSeedGet
from .randomSeedSet import randomSeedSet
from .randomSphere import randomSphere
from .randomStable import randomStable
from .randomStudentT import randomStudentT
from .randomSubstreamSeedGet import randomSubstreamSeedGet
from .randomTableGet import randomTableGet
from .randomTableSet import randomTableSet
from .randomTableTwoway import randomTableTwoway
from .randomTriangular import randomTriangular
from .randomUniform import randomUniform
from .randomUniformDiscrete import randomUniformDiscrete
from .randomVonMises import randomVonMises
from .randomWeibull import randomWeibull
from .randomnessTest import randomnessTest
from .ranks import ranks
from .rcbdFactorial import rcbdFactorial
from .regression import regression
from .regressionArima import regressionArima
from .regressionPrediction import regressionPrediction
from .regressionSelection import regressionSelection
from .regressionStepwise import regressionStepwise
from .regressionSummary import regressionSummary
from .regressorsForGlm import regressorsForGlm
from .robustCovariances import robustCovariances
from .scaleFilter import scaleFilter
from .seasonalFit import seasonalFit
from .setUserFcnReturnFlag import setUserFcnReturnFlag
from .shapiroWilkNormalityTest import shapiroWilkNormalityTest
from .signTest import signTest
from .simpleStatistics import simpleStatistics
from .sortData import sortData
from .splitPlot import splitPlot
from .splitSplitPlot import splitSplitPlot
from .stripPlot import stripPlot
from .stripSplitPlot import stripSplitPlot
from .supportVectorClassification import supportVectorClassification
from .supportVectorTrainer import supportVectorTrainer
from .survivalEstimates import survivalEstimates
from .survivalGlm import survivalGlm
from .svmClassifierFree import svmClassifierFree
from .tCdf import tCdf
from .tInverseCdf import tInverseCdf
from .tableOneway import tableOneway
from .tableTwoway import tableTwoway
from .tieStatistics import tieStatistics
from .timeSeriesClassFilter import timeSeriesClassFilter
from .timeSeriesFilter import timeSeriesFilter
from .tsOutlierForecast import tsOutlierForecast
from .tsOutlierIdentification import tsOutlierIdentification
from .unsupervisedNominalFilter import unsupervisedNominalFilter
from .unsupervisedOrdinalFilter import unsupervisedOrdinalFilter
from .vectorAutoregression import vectorAutoregression
from .version import version
from .wilcoxonRankSum import wilcoxonRankSum
from .wilcoxonSignRank import wilcoxonSignRank
from .writeAprioriItemsets import writeAprioriItemsets
from .writeAssociationRules import writeAssociationRules
from .writeMatrix import writeMatrix
from .writeOptions import writeOptions
from .yates import yates

CONST = 1
NO_CONST = 2
NO_ESTIMATION = 0
MOMENTS = 1
DURBIN_LEVINSON = 2
INNOVATIONS = 3
PRELIMINARY_ARMA = 4
LSE = 5
MLE = 6
NO_SE_CCF = 0
BARTLETT_SE_CCF = 1
XY_NO_CORR_SE_CCF = 2
X_NOISES_SE_CCF = 3
FORWARD_PERMUTATION = 1
BACKWARD_PERMUTATION = 2
PERMUTE_ROWS = 3
PERMUTE_COLUMNS = 4
ALL = 1
LEAVE_OUT_LAST = 2
SUM_TO_ZERO = 3
NOTE = 1
ALERT = 2
WARNING = 3
FATAL = 4
TERMINAL = 5
WARNING_IMMEDIATE = 6
FATAL_IMMEDIATE = 7
SET_PAGE_WIDTH = -1
GET_PAGE_WIDTH = 1
SET_PAGE_LENGTH = -2
GET_PAGE_LENGTH = 2
SET_DEFAULTS = 0
SET_CENTERING = -1
GET_CENTERING = 1
SET_ROW_WRAP = -2
GET_ROW_WRAP = 2
SET_PAGING = -3
GET_PAGING = 3
SET_NAN_CHAR = -4
GET_NAN_CHAR = 4
SET_TITLE_PAGE = -5
GET_TITLE_PAGE = 5
SET_FORMAT = -6
GET_FORMAT = 6
ALG = 1
ALG_LEFT_LOG = 2
ALG_RIGHT_LOG = 3
ALG_LOG = 4
INF_BOUND = 5
BOUND_INF = 6
INF_INF = 7
COS = 8
SIN = 9
LINEAR = 0
LOGISTIC = 1
TANH = 2
SQUASH = 3
