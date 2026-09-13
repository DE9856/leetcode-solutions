class Solution(object):
    def construct2DArray(self, original, m, n):
        """
        :type original: List[int]
        :type m: int
        :type n: int
        :rtype: List[List[int]]
        """
        length = len(original)
        if length!=m*n:
            return []
        sol = []
        for i in range(m):
            row = []
            for j in range(n):
                row.append(original[i*n + j])
            sol.append(row)
        return sol
