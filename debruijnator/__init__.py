import screed
import string
import igraph
import kmertree

"""
A simple de Bruijn graph implementation.
"""

ttable = string.maketrans( 'atgc', 'tacg' )
SHORT_SEQS = False

def rc( seq ) :
    """
    Return the reverse compliment.
    """
    return seq.lower().translate( ttable )[::-1]

def get_kmers( k, seq ) :
    """
    Generate kmers for forward and reverse strands
    """

    seq = seq.lower()

    # handle very short sequences
    if k > len(seq) :
        if SHORT_SEQS :
            return [ seq, rc(seq) ]
        else :
            return []
    
    fkmers = []
    rkmers = []
    rvc = rc( seq )
    for i in range(len( seq ) - k + 1 ) :
        fkmers.append( seq[ i : i+k ] )
        rkmers.append( rvc[ i : i+k ] )
    
    return { 'forward' : fkmers, 'reverse' : rkmers }

class deBruijnGraph :
    """
    down        : forward link in graph
    up          : reverse link in graph
    forward     : forward strand on DNA
    reverse     : reverse compliment strand on DNA
    """

    def __init__( self, k ) :
        self.k = k
        self.graph = {}
        self.otable = { ( 1, 1) : 'ff', 
                        ( 1,-1) : 'fr', 
                        (-1, 1) : 'rf', 
                        (-1,-1) : 'rr', }
        
        self.g = igraph.Graph( directed=True )
        self.kmertree = kmertree.KmerTree()
        self.kmers = []

    def add_edge( self, kmer1, kmer2, strand1, strand2 ) :
        """
        Add an edge to the de Bruijn graph.

            kmer1   : first kmer (a string)
            kmer2   : second kmer (a string)
            strand1 : strand orientation of first kmer (1 or -1)
            strand2 : strand orientation of second kmer (1 or -1)
        """
        if not self.graph.has_key( kmer1 ) :
            self.graph[ kmer1 ] = { 'down' : {}, 'up' : {} }
        if not self.graph.has_key( kmer2 ) :
            self.graph[ kmer2 ] = { 'down' : {}, 'up' : {} }
        
        s1 = strand1
        s2 = strand2
        k1 = kmer1 
        k2 = kmer2
        for direction in [ 'down', 'up' ] :
            ori = self.otable[ (s1, s2) ]

            if not self.graph[ k1 ][direction].has_key( k2 ) :
                self.graph[ k1 ][direction][ k2 ] = { ori : 1 }
            else :
                if not self.graph[ k1 ][direction][ k2 ].has_key(ori) :
                    self.graph[ k1 ][direction][ k2 ][ori] = 1
                else :
                    self.graph[ k1 ][direction][ k2 ][ori] = self.graph[ k1 ][direction][ k2 ][ori] + 1
            
            s2 = strand1
            s1 = strand2
            k2 = kmer1
            k1 = kmer2

    def add_edge_igraph( self, kmer1, kmer2, strand1, strand2 ) :
        """
        Add an edge to the de Bruijn graph.

            kmer1   : first kmer (a string)
            kmer2   : second kmer (a string)
            strand1 : strand orientation of first kmer (1 or -1)
            strand2 : strand orientation of second kmer (1 or -1)

            NOTE : This implementation doesn't use the strand
                   orientation for anything.
        """

        ori = self.otable[ ( strand1, strand2 ) ]
        
        if self.g.vcount() == 1 :
            self.g.vs[0]['kmer'] = kmer1
            self.kmertree[kmer1] = 0
            self.kmers.append(kmer1)

        i = 0
        for kmer in [ kmer1, kmer2 ] :
            j = i
            if not kmer in self.kmers :
                self.g.add_vertices( 1 )
                j = self.g.vcount() - 1
                self.kmertree[kmer] = j
                #self.g.vs[ i ]['kmer'] = kmer
                self.kmers.append(kmer)
            else : 
                j = self.kmertree[kmer]
                
        try : 
            edge = self.g.get_eid( i, j )
            self.g.es[ edge ][ori] = self.g.es[ edge ][ori] + 1
        except igraph.InternalError :
            self.g.add_edges( (i,j) )
            edge = self.g.get_eid( i, j )
            for o in self.otable.values() :
                self.g.es[ edge ][o] = 0
            self.g.es[edge][ori] = 1
        

    def consume_seq( self, seq ) :
        """
        
        """
        for orientation, kmers in get_kmers( self.k, seq ).items() :
        
            if orientation == 'forward' :
                o = 1
            if orientation == 'reverse' :
                o = -1
            
            for i in range( len(kmers) - 1 ) :
                self.add_edge_igraph( kmers[i], kmers[i+1], o, o )
        

    def consume_fasta( self, seqfile ) :
        """
        """
        for n, record in enumerate( screed.fasta.fasta_iter( open( seqfile ) ) ) :
            
            if n % 10000 == 0 :
                print '...', n

            self.consume_seq( record['sequence'] )
