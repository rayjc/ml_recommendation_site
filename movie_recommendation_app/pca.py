import numpy as np

from scipy.sparse import linalg

class PCA:
    '''
    Solves the PCA problem min_Z,W (Z*W-X)^2 using SVD
    '''

    def __init__( self, k=10 ):
        self.k = k

    def fit( self, X ):
        # self.mu = np.mean( X, axis=0 )
        # X = X - self.mu

        # U, s, Vh = np.linalg.svd( X )
        # self.W = Vh[ :self.k ]
        self.mu = np.mean( X, axis=0 )
        X = X - self.mu

        U, s, Vh = linalg.svds( X, self.k )
        self.W = Vh

    def compress( self, X ):
        X = X - self.mu
        Z = X @ self.W.T
        return Z

    def expand( self, Z ):
        X = Z @ self.W + self.mu
        return X