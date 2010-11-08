#!/usr/bin/python2.6

import os
import sys
import debruijnator
import string
import random
import screed

K = 32

def mem() :
    return int(os.popen('ps -p %d -o %s | tail -1' % (os.getpid(), 'rss')).read())

def randomDNA( length ) :
    dna = []
    for i in range(length+1) :
        dna.append( random.choice(['a', 't', 'g', 'c']) )
    return ''.join(dna)

db = debruijnator.deBruijnGraph( K )

es = []
vs = []
mm = []

f = open( sys.argv[1] + '_mem.csv', 'w' )

for n, record in enumerate( screed.fasta.fasta_iter( open( sys.argv[1] ) ) ) :
    print n, record['name']
    es.append( db.g.ecount() )
    vs.append( db.g.vcount() )
    mm.append( mem() )
    f.write( str(es[-1]) + ',' + str(vs[-1]) + ',' + str(mm[-1]) + '\n' )

    db.consume_seq( record['sequence'] )

f.close()
