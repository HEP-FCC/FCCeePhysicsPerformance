import os
repo = os.getenv('PWD')
print ('========================',repo)
repo="/afs/cern.ch/work/h/helsens/FCC/soft/FCCAnalyses/test/"
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output/'
loc.DATA = loc.ROOT+'data'
loc.PLOTS = loc.OUT+'plots'
loc.TABLES = loc.OUT+'tables'
loc.JSON = loc.OUT+'json'
loc.FLAT = "/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Flavor"
