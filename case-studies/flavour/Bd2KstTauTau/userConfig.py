import os
repo = os.getenv('PWD')
#repo can be changed, but by default writes locally
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output/'
loc.DATA = loc.ROOT+'data'
loc.PLOTS = loc.OUT+'plots'
loc.TABLES = loc.OUT+'tables'
loc.JSON = loc.OUT+'json'
loc.FLAT = "/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Flavor"

#Input file location
loc.IN = "/eos/experiment/fcc/ee/tmp/testmatching/"

#Decay mode
mode = "Bd2KstTauTauTAUHADNU"
