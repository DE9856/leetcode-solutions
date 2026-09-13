class Solution(object):
    def luckyNumbers(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        sol = []
        n = len(matrix)
        m = len(matrix[0])
        for i in range(n):
            minimum = min(matrix[i])
            for j in range(m):
                if matrix[i][j]==minimum:
                    column = [matrix[k][j] for k in range(n)]
                    if minimum == max(column):
                        sol.append(minimum)
        return sol
        
