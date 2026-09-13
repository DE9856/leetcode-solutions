class Solution(object):
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """
        sol = []
        for i in range(numRows):
            new = [1]*(i+1)
            for j in range(1,i):
                new[j] = sol[i-1][j-1] + sol[i-1][j]
            sol.append(new)
        return sol 
        
