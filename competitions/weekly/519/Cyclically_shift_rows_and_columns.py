class Solution(object):
    def cyclicShift(self, n, grid, rowShift, colShift):
        """
        :type n: int
        :type grid: List[List[int]]
        :type rowShift: List[int]
        :type colShift: List[int]
        :rtype: List[List[int]]
        """
        for i in range(n):
            rem = rowShift[i]%n
            grid[i] = grid[i][rem:] + grid[i][:rem]

        for i in range(n):
            rem = colShift[i]%n
            cols = []
            for j in range(n):
                cols.append(grid[j][i])
            cols = cols[rem:] + cols[:rem]
            for j in range(n):
                grid[j][i] = cols[j]
        return grid        
