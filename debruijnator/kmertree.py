"""
A string search tree that implements a minimal python dictionary
interface.
"""

class KmerTreeException( Exception ) :
    pass

class KmerTree :
    """
    A string search tree that implements a minimal python dictionary
    interface.

    Once set, key-value pairs cannot be changed.
    """
    def __init__( self ) :
        self.root = {}
    
    def __setitem__( self, key, value ) :
        key = key.lower()
        node = self.root
        for i in key[:-1] :
            if node.has_key( i ) :
                node = node[ i ]
            else :
                node[ i ] = {}
                node = node[ i ]
        if not node.has_key(key[-1]) :
            node[key[-1]] = value
        else :
            raise KmerTreeException( 'Collision : ' + key )

    def __getitem__( self, key ) :
        key = key.lower()
        node = self.root
        for i in key :
            if node.has_key( i ) :
                node = node[ i ]
            else :
                raise KmerTreeException( 'Key not found : ' + key )
        if type(node).__name__ == 'int' :
            return node
        else :
            raise KmerTreeException( 'Bad key : ' + key )
