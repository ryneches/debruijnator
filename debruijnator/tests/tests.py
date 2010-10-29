import debruijnator as d

def test_rc() :
    assert d.rc( 'ggaattcc' ) == 'ggaattcc'
    assert d.rc( 'tgactgac' ) == 'gtcagtca'
    assert d.rc( 'tttttttt' ) == 'aaaaaaaa'
    assert d.rc( 'AAAATTTT' ) == 'aaaatttt'
    assert d.rc( 'GGGGcccc' ) == 'ggggcccc'

def test_kmers() :
    assert len( d.get_kmers( 4, 'atatat' )['forward'] ) == 3
    assert d.get_kmers( 4, 'atatat' )['forward'][0] == 'atat'

def test_create_graph_object() :
    db = d.deBruijnGraph( 4 )

def test_add_edge() :
    db = d.deBruijnGraph( 4 )
    db.add_edge( 'atat', 'tata', 1, 1, )
    assert db.graph.has_key( 'atat' )
    assert db.graph[ 'atat' ]['down'].has_key( 'tata' )

def test_consume_seq() :
    db = d.deBruijnGraph( 4 )
    db.consume_seq( 'atatat' )
    assert db.graph.has_key( 'atat' )
    
    # this graph should be a ring
    assert db.graph[ 'atat' ]['down'].has_key( 'tata' )
    assert db.graph[ 'tata' ]['up'].has_key( 'atat' )
    assert db.graph[ 'tata' ]['down'].has_key( 'atat' )

