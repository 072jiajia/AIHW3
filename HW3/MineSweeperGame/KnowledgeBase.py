from .Clause import *


class KnowledgeBase:
    '''class of kwowledge base'''

    def __init__(self):
        '''
        it contains only one object 'clause'
        it is a list which contains every clause of this KB
        '''
        self.clauses = []

    def insert(self, clause):
        '''insert a clause to the KB'''
        # if there is any stricter clauses in the KB, don't insert it
        if self.exist(clause):
            return True
        # remove the useless clauses in the KB which clause is stricter than it
        self.removeuselessclause(clause)

        # match the insert clause and the matchable clauses in the KB
        # and append it to the recursive-insert list
        rec_append = []
        for c in self.clauses:
            new_c = clause.match(c)
            if new_c is not None:
                rec_append.append(new_c)
        # append clause and do recursive insert
        self.clauses.append(clause)
        for c in rec_append:
            self.insert(c)

    def exist(self, C):
        '''check whether there is any stricter clause in KB'''
        for clause in self.clauses:
            if clause.isstickerthan(C):
                return True
        return False

    def removeuselessclause(self, C):
        '''remove the clauses in KB that C is stricter than it '''
        idx = 0
        while idx < len(self.clauses):
            if C.isstickerthan(self.clauses[idx]):
                self.clauses.pop(idx)
                continue
            idx += 1

    def insert_clauses(self, objs, n):
        '''do C(m, m-n+1) positive-clause insertion
            and C(m, n+1) negative-clause insertion
        '''
        clauses = get_clauses(objs, n)
        for clause in clauses:
            self.insert(Clause(clause))

    def PRINT(self):
        '''print the pliterals and nliterals of every clause in KB'''
        for cl in self.clauses:
            print(cl.pliterals, cl.nliterals)
