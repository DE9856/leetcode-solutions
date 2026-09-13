class Solution(object):
    def transpose(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """
        m = len(matrix)
        n = len(matrix[0])
        sol = []
        for j in range(n):
            temp = []
            for i in range(m):
                temp.append(matrix[i][j])
            sol.append(temp)
        return sol
