#__________________________________________________________
def dir_exist(mydir):
    import os.path
    if os.path.exists(mydir): return True
    else: return False


#__________________________________________________________
def create_dir(mydir):
    if not dir_exist(mydir):
        import os
        os.system('mkdir -p {}'.format(mydir))
