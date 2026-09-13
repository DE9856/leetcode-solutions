class Solution(object):
    def getRow(self, rowIndex):
        """
        :type rowIndex: int
        :rtype: List[int]
        """
        sol = []
        for i in range(rowIndex+1):
            new = [1]*(i+1)
            for j in range(1,i):
                new[j] = sol[i-1][j-1] + sol[i-1][j]
            sol.append(new)
        return sol[-1]
        
        
