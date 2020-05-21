
class Clause:
    '''this is a class to save the literals of a clause'''

    def __init__(self, literals):
        '''
        - pliterals: a set containing all the positive literal of this clause
        - nliterals: a set containing all the negative literal of this clause
        input 'literals' should be like [('-', obj1), ('+', obj2),...]
        '''
        self.pliterals = set()
        self.nliterals = set()
        for literal in literals:
            if literal[0] == '-':
                self.nliterals.add(literal[1])
            else:
                self.pliterals.add(literal[1])

    def isstickerthan(self, C):
        '''to check whether self is a stricter clause than C'''
        if self.pliterals.issubset(C.pliterals):
            if self.nliterals.issubset(C.nliterals):
                return True
        return False

    def match(self, C):
        '''match two clauses'''
        # if both have more than two literals, return None
        if (len(self.nliterals) + len(self.pliterals) >= 3 and
                len(C.nliterals) + len(C.pliterals) >= 3):
            return None

        # get the object remove
        removeobj = None

        for p in self.pliterals:
            if p in C.nliterals:
                if removeobj is None:
                    removeobj = p
                else:
                    # return None when there's more than one
                    # pair of complementary literals
                    return None
        for p in C.pliterals:
            if p in self.nliterals:
                if removeobj is None:
                    removeobj = p
                else:
                    # return None when there's more than one
                    # pair of complementary literals
                    return None

        if removeobj is None:
            # return None when there's no any pairs of complementary literals
            return None

        # get the matched clause
        ret = Clause([])
        ret.pliterals = self.pliterals.union(C.pliterals)
        ret.nliterals = self.nliterals.union(C.nliterals)
        ret.nliterals.remove(removeobj)
        ret.pliterals.remove(removeobj)
        return ret


def get_pclause_rec(objs, N, idxs, ret):
    '''get pisotive clauses using recursive way'''
    # if all index has been generated, generate the clause
    if len(idxs) == N:
        ins = []
        for idx in idxs:
            ins.append(('+', objs[idx]))
        ret.append(ins)
        return

    # else generate the next index
    idxs.append(None)
    for idx in range(idxs[-2]+1, len(objs)-N+len(idxs)):
        idxs[-1] = idx
        get_pclause_rec(objs, N, idxs, ret)
    idxs.pop()


def get_nclause_rec(objs, N, idxs, ret):
    '''get negative clauses using recursive way'''
    # if all idx has been generated, generate the clause
    if len(idxs) == N:
        ins = []
        for idx in idxs:
            ins.append(('-', objs[idx]))
        ret.append(ins)
        return

    # else generate the next index
    idxs.append(None)
    for idx in range(idxs[-2]+1, len(objs)-N+len(idxs)):
        idxs[-1] = idx
        get_nclause_rec(objs, N, idxs, ret)
    idxs.pop()


def get_clauses(objs, n):
    '''get C(m, m-n+1) positive
    and get C(m, n+1) negative
    '''
    # if n equals to lower or upper bound
    # of the constraint, simply make the clauses
    ret = []
    if n == 0:
        for obj in objs:
            ret.append([('-', obj)])
        return ret
    if n == len(objs):
        for obj in objs:
            ret.append([('+', obj)])
        return ret

    # else, make the positive and negative clauses
    idxs = [None]
    for idx in range(len(objs)):
        idxs[0] = idx
        get_pclause_rec(objs, len(objs)-n+1, idxs, ret)

    for idx in range(len(objs)):
        idxs[0] = idx
        get_nclause_rec(objs, n+1, idxs, ret)

    return ret
