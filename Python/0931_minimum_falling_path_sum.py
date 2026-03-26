class Solution(object):
    def minFallingPathSum(self, matrix):
        n = len(matrix)
        for i in range(1,n):
            for j in range(n):
                up = matrix[i-1][j]
                left = matrix[i-1][j-1] if j>0 else float('inf')
                right = matrix[i-1][j+1] if j<n-1 else float('inf')

                matrix[i][j] += min(up,left,right)

        return min(matrix[-1])
        
