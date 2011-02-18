#! /usr/bin/env python
#coding=utf-8

import os,sys,string,shutil

DEBUG = False

if DEBUG:
    import logging
    from logging import debug as log
    
    pyfp = os.path.abspath(sys.argv[0])

    LOG_FILENAME = '%s.log'%pyfp
    print LOG_FILENAME
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
else:
    def log(str):
        pass

#Here you can use bcompare(beyond compare),meld and so on
DIFFTOOL = "bcompare"

def do_config():
    answer = raw_input("Are you sure to use difftool '%s'(y/n)?"%DIFFTOOL)
    if (answer.lower().find("y")!=-1):
        pyfp = os.path.abspath(sys.argv[0])
        #print pyfp
        cmd = 'git config --global --replace-all guitool.%s.cmd "%s \$FILENAME"'%(DIFFTOOL,pyfp)
        print cmd
        os.system(cmd)
        cmd = 'git config --global --replace-all guitool.%s.noconsole "yes"'%(DIFFTOOL)
        print cmd
        os.system(cmd)
        cmd = 'git config --global --replace-all guitool.%s.needsfile "yes"'%(DIFFTOOL)
        print cmd
        os.system(cmd)
        print "Now you can use the git-gui's menu->Tools->%s to use visual diff tool"%DIFFTOOL
    else:
        print "Pls modify the DIFFTOOL in this py file to visual diff tool you are using."

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
    log("-------")
    fp = os.path.abspath(fp)
    log(fp)
    git_dp,relfp = find_git(fp)
    log("%s %s"%(git_dp,relfp))
    if git_dp!="":
        old_cwd = os.getcwd()
        log("old:%s"%os.getcwd())
        
        tmpdp = os.tmpnam()+".HEAD"
        os.mkdir(tmpdp)
        os.chdir(tmpdp)
        
        log("change to %s"%os.getcwd())
        fn = os.path.split(relfp)[-1]
        #I learn this command in here:
        #http://article.gmane.org/gmane.comp.version-control.git/167064
        cmd = 'git --git-dir="%s" cat-file blob HEAD:%s>%s'%(git_dp,relfp,fn)
        ret = os.system(cmd)
        log("%s return %s"%(cmd,ret))
        if ret==0:
            if os.path.exists(fn):
                cmd = '%s %s %s'%(DIFFTOOL,fp,fn)
                log(cmd)
                os.system(cmd)
        shutil.rmtree(tmpdp)
        
        os.chdir(old_cwd)
        log("change back to %s"%os.getcwd())

if __name__ == '__main__':
    log("%d"%(len(sys.argv)))
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        do_config()
