#! /usr/bin/env python
#coding=utf-8

import os,sys,string,shutil
'''
import logging

LOG_FILENAME = '/media/DATA/t/git_gui_difftool.py.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
'''

#Here you can use bcompare(beyond compare),meld and so on
DIFFTOOL = "bcompare"

def find_git(fp):
    fl = fp.split("/")
    fl_len = len(fl)
    l = fl[:-1]
    #print fl
    for i in range(len(l)-1):
        dp = os.path.join(string.join(l[0:len(l)-i],"/"),".git")
        relfp = string.join(fl[(fl_len-i-1):],"/")
        #print dp,"---",relfp
        if os.path.exists(dp):
            return dp,relfp
    return "",""

def main(fp):
    #logging.debug("-------")
    fp = os.path.abspath(fp)
    #logging.debug(fp)
    git_dp,relfp = find_git(fp)
    #logging.debug("%s %s"%(git_dp,relfp))
    if git_dp!="":
        old_cwd = os.getcwd()
        #logging.debug("old:%s"%os.getcwd())
        
        tmpdp = os.tmpnam()+".HEAD"
        os.mkdir(tmpdp)
        os.chdir(tmpdp)
        
        #logging.debug("change to %s"%os.getcwd())
        fn = os.path.split(relfp)[-1]
        #I learn this command in here:
        #http://article.gmane.org/gmane.comp.version-control.git/167064
        cmd = 'git --work-tree=. --git-dir="%s" cat-file blob HEAD:%s>%s'%(git_dp,relfp,fn)
        ret = os.system(cmd)
        #logging.debug("%s return %s"%(cmd,ret))
        if ret==0:
            if os.path.exists(fn):
                cmd = '%s %s %s'%(DIFFTOOL,fp,fn)
                #logging.debug(cmd)
                os.system(cmd)
        shutil.rmtree(tmpdp)
        
        os.chdir(old_cwd)
        #logging.debug("change back to %s"%os.getcwd())

if __name__ == '__main__':
    if len(sys.argv)>1:
        main(sys.argv[1])
