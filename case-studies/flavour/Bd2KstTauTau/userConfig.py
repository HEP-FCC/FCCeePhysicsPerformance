import os
repo = os.getenv('PWD')
#repo can be changed, but by default writes locally
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output/'
loc.DATA = loc.ROOT+'data'
loc.PLOTS = loc.OUT+'plots22'
loc.TABLES = loc.OUT+'tables'
loc.JSON = loc.OUT+'json'
loc.FLAT = "/eos/experiment/fcc/ee/tmp/flatntuples/Z_Zbb_Flavor"
