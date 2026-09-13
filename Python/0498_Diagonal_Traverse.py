class Solution(object):
    def findDiagonalOrder(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: List[int]
        """
        m = len(mat)
        n = len(mat[0])
        sol = []

        for diag in range(m+n-1):
            temp = []
            for i in range(m):
                j = diag - i
                if j>=0 and j<n:
                    temp.append(mat[i][j])
            if diag%2==0:
                temp.reverse()
            sol+=temp

        return sol
        
