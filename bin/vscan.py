#!/usr/bin/env python

from vtool.util import *
import os, getopt
import sys

__author__ = ""
__date__ = "2013/11/25"

__version__ = "$Revision: 0.1$"


def makeScanJob(poscars, elements = None):
    i = 0
    g = GJF()
    for p in poscars:
        dir = "0%d" %(i) if i < 10 else "%2d" %(i)
        if os.path.isdir(dir):
            pass
        else:
            os.mkdir(dir)

        if os.path.isfile(os.path.join(dir, 'POSCAR') ):
            overwriteFlag = raw_input("Overwrite %s/POSCAR[Y/n] : " %dir)
            if overwriteFlag.lower() == 'y':
                p.writePOSCAR(os.path.join(dir, 'POSCAR') )
                poscar2gjf(p, g, elements)
                g.writeGJF(os.path.join(dir, dir + ".gjf") )

        else:
            p.writePOSCAR(os.path.join(dir, 'POSCAR') )
            poscar2gjf(p, g, elements)
            g.writeGJF(os.path.join(dir, dir + ".gjf") )
        i = i + 1
    pass


def main():
    def usage():
        print "Usage: vscan -i POSCAR -r 1     -m 2 -g 3,4,5 -n 4 -d 1.0  -e H,C,O   # line  scan"
        print "       vscan -i POSCAR -r 1,2   -m 3 -g 4,5,6 -n 4 -d 30.0 -e H,C,O   # angle scan"
        print "       vscan -i POSCAR -r 1,2,3 -m 4 -g 5,6,7 -n 4 -d 30.0 -e H,C,O   # dihedral scan"
        print " -h : help"
        print " -i : input file, POSCAR"
        print " -r : reference atoms"
        print " -m : motion atom"
        print " -g : atom with motion atom"
        print " -n : number of step"
        print " -d : displacement (distance/angle)"
        print " -e : setup element type, ie H,C,O,..."

    def checkFile(f):
        if os.path.exists(f):
            return os.path.abspath(f)
        print "File: " + f + " didn't exist."
        sys.exit(2)
        return False

    try:
        opt_list, args = getopt.getopt(sys.argv[1:], "hi:r:m:g:n:d:e:")

    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    infile = None
    r_indexes = None
    m_indexes = None
    g_indexes = None
    nstep = None
    displacement = None
    elements = None
    for o, a in opt_list:
        if o in ('-h'):
            usage()
            sys.exit()
        elif o in ('-i'):
            infile = a
        elif o in ('-r'):
#            r_indexes = a
            r_indexes = [int(i)-1 for i in a.split(',')]
        elif o in ('-m'):
#            m_indexes = a
            m_indexes = [int(i)-1 for i in a.split(',')]
        elif o in ('-g'):
#            g_indexes = a
            g_indexes = [int(i)-1 for i in a.split(',')]
        elif o in ('-n'):
            nstep = int(a)
        elif o in ('-d'):
            displacement = float(a)
        elif o in ('-e'):
            elements = a.split(',')

    if infile is None:
        print "Intput file: "
        infile = sys.stdin.readline().rstrip()
#        infile = checkFile(sys.stdin.readline().rstrip())
    poscar = POSCAR(infile)
    poscar.directToCartesian()
    if elements != None:
        poscar.setElementsType(elements)


    if r_indexes is None:
        print "reference atoms: "
        r_indexes = sys.stdin.readline().rstrip()
        r_indexes = [int(i)-1 for i in r_indexes.split(',')]

    if m_indexes is None:
        print "motion atom: "
        m_indexes = sys.stdin.readline().rstrip()
        m_indexes = [int(i)-1 for i in m_indexes.split(',')]

    if g_indexes is None:
#        print "group atoms: "
#        g_indexes = sys.stdin.readline().rstrip()
#        g_indexes = [int(i)-1 for i in g_indexes.split(',')]
        g_indexes = []

    if nstep is None:
        print "number of step: "
        nstep = sys.stdin.readline().rstrip()
        nstep = int(nstep)

    if displacement is None:
        print "displacement distance/angle: "
        displacement = sys.stdin.readline().rstrip()
        displacement = float(displacement)

    if len(r_indexes) == 1:
#    line scan
        poscars = poscar.lineScan(displacement, nstep, r_indexes, m_indexes, g_indexes)
    elif len(r_indexes) == 2:
#    angle scan
        poscars = poscar.angleScan(displacement, nstep, r_indexes, m_indexes, g_indexes)
    elif len(r_indexes) == 3:
#    dihedral angle scan
        poscars = poscar.dihedralScan(displacement, nstep, r_indexes, m_indexes, g_indexes)
    else:
        print "input error of reference atom"
        sys.exit(2)

    makeScanJob(poscars, elements)


if __name__ == "__main__":
    main()

