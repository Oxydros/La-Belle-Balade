import itertools
import random
import sys


def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)
    
    if n==2:
        return dists[0,1], [0,1]
    
    else:
        # Maps each subset of the nodes to the cost to reach that subset, as well
        # as what node it passed before reaching this subset.
        # Node subsets are represented as set bits.
        C = {}
    
        # Set transition cost from initial state
        for k in range(1, n):
            C[(1 << k, k)] = (dists[0][k], 0)
    
        # Iterate subsets of increasing length and store intermediate results
        # in classic dynamic programming manner
        for subset_size in range(2, n-1):
            for subset in itertools.combinations(range(1, n-1), subset_size):
                # Set bits for all nodes in this subset
                bits = 0
                for bit in subset:
                    bits |= 1 << bit
    
                # Find the lowest cost to get to this subset
                for k in subset:
                    prev = bits & ~(1 << k)
    
                    res = []
                    for m in subset:
                        if m == 0 or m == k:
                            continue
                        res.append((C[(prev, m)][0] + dists[m][k], m))
                    C[(bits, k)] = min(res)
        
        subset = range(1,n)
        bits = 0
        for bit in subset:
            bits |= 1 << bit
    
        # Find the lowest cost to get to this subset
        k = n-1
        prev = bits & ~(1 << k)
        
        res = []
        for m in subset:
            if m == 0 or m == k:
                continue
            res.append((C[(prev, m)][0] + dists[m][k], m))
        opt, parent = min(res)
        
        # We're interested in all bits but the least significant (the start state)
        bits = (2**(n) - 1) - 1
        bits = bits - 2**(n-1)
    
        # Backtrack to find full path
        path = []
        for i in range(n - 2):
            path.append(parent)
            new_bits = bits & ~(1 << parent)
            _, parent = C[(bits, parent)]
            bits = new_bits
    
        # Add implicit start state
        path.append(0)
        path = list(reversed(path))
        path.append(n-1)
        return opt, path