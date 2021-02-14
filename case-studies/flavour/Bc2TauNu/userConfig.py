import os
#repo = os.getenv('PWD')
repo = "/afs/cern.ch/work/d/dhill/Bc2TauNu"
#repo can be changed, but by default writes locally
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output/'
loc.DATA = loc.ROOT+'data'
loc.CSV = loc.DATA+'/csv'
loc.ROOTFILES = loc.DATA+'/ROOT'
loc.PLOTS = loc.OUT+'plots'
loc.TABLES = loc.OUT+'tables'
loc.JSON = loc.OUT+'json'

#Input file location
loc.IN = "/eos/experiment/fcc/ee/tmp/flatntuples"

#Decay mode
mode = "Z_Zbb_Bc2TauNu_v02"
