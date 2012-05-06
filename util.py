import settings
import os
def save_file_with_md5path(filename,content,md5):
    base_path = __create_md5path(md5,settings.UPLOAD_PATH)
    with open(os.path.join(base_path,filename),'w+') as f:
        f.write(content)
        f.close()

def __create_md5path(md5,base_dir):
    dir1 = md5[0:2]
    dir2 = md5[2:4]
    dir3 = md5[4:6]
    __chk_and_create_dir(base_dir,dir1)
    __chk_and_create_dir(base_dir,dir1,dir2)
    __chk_and_create_dir(base_dir,dir1,dir2,dir3)
    __chk_and_create_dir(base_dir,dir1,dir2,dir3,md5)
    return os.path.join(base_dir,dir1,dir2,dir3,md5)

def __chk_and_create_dir(a,*args):
    p = os.path.join(a,*args)
    if os.path.exists(p) and os.path.isdir(p):
        pass
    else:
        os.mkdir(p)
        
def load_content_from_md5(fn,md5,base_dir):
    dir1 = md5[0:2]
    dir2 = md5[2:4]
    dir3 = md5[4:6]
    fpath = os.path.join(base_dir,dir1,dir2,dir3,md5,fn)
    with open(fpath,'r') as f:
        return f.read()