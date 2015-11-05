#Grant Riley October 27 2015

## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.source = cms.Source("PoolSource",
                duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                skipEvents = cms.untracked.uint32(0),
                fileNames = cms.untracked.vstring(
                        'file:/uscms_data/d3/jheidema/13TeVRecodata/CMSSW_7_4_15_patch1/src/127559F7-E86B-E511-8631-02163E014497.root'
                        )
                )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.GlobalTag.globaltag = cms.string('74X_dataRun2_Prompt_v4')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = cms.string('74X_dataRun2_Prompt_v4')

#Needed for the below MC Matching to find processes
process.load("PhysicsTools.PatAlgos.patSequences_cff")
#remove MC Matching for Real data
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, names=['All'],outputModules=[])
# switch on PAT trigger info
from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process )
#try to trigger skim?
process.triggerSelection = cms.EDFilter( "TriggerResultsFilter",
                triggerConditions = cms.vstring(
                        'HLT_Dimuon0_Upsilon_Muon_v*',
                        'HLT_Dimuon0_Jpsi_Muon_v*' ),
                hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
                l1tResults = cms.InputTag( "gtDigis" ),
                l1tIgnoreMask = cms.bool( False ),
                l1techIgnorePrescales = cms.bool( False ),
                daqPartitions = cms.uint32( 1 ),
                throw = cms.bool( True )
                )
process.TrigSkim = cms.Path(process.triggerSelection)
#make J/Psi cands from muons
##Add Muon candidates
#from PhysicsTools.PatAlgos.tools.muonTools import *
process.goodMuons = cms.EDFilter("PATMuonSelector",
                src = cms.InputTag("patMuons"),
#                cut = cms.string(''),
                cut = cms.string("track.isNonnull && track.hitPattern.pixelLayersWithMeasurement > 0 ")
                )
process.makeGoodMuons = cms.Path(process.goodMuons)
#process.UpsCand = cms.EDProducer("CandViewShallowCloneCombiner",
#                decay = cms.string('goodMuons@+ goodMuons@-'),
#                cut = cms.string('mass>=9.1 && mass<=9.75'),
#                )
#process.makeUpsCand = cms.Path(process.UpsCand)
#process.DiMuCand = cms.EDProducer("CandViewShallowCloneCombiner",
#                decay = cms.string('goodMuons@+ goodMuons@-'),
#                cut = cms.string('mass<9.1'),
#                )
#process.makeDiMuCand = cms.Path(process.DiMuCand)
process.FourMuCand= cms.EDProducer("CandViewShallowCloneCombiner",
                decay = cms.string('UpsCand DiMuCand'),
                cut = cms.string(''),
                )
process.makeFourMuCand = cms.Path(process.FourMuCand)
## let it run
process.pat = cms.Path(
                process.patDefaultSequence
                )

#produce output

process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('MuOnia_Run2015D_5Oct2015-v1_HLT_MuonJpsi_Oct2015Skim.root'),
## save only events passing the full path
                SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring("TrigSkim") ),
                ## save PAT output; you need a '*' to unpack the list of commands
#                outputCommands = cms.untracked.vstring('drop *', 'keep *reco*', 'keep *pat*', 'keep *hlt*')

#Need to add in removal of non necessary data
                )
process.outpath = cms.EndPath(process.out)
# Schedule
process.schedule = cms.Schedule(process.TrigSkim,process.pat,process.makeGoodMuons,process.makeFourMuCand,process.outpath)

