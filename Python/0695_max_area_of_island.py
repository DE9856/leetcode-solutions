class Solution(object):
    def maxAreaOfIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        n = len(grid)
        m = len(grid[0])
        maxsize = 0
        def dfs(r,c):
            if r<0 or r>=n or c<0 or c>=m:
                return 0
            if grid[r][c]==0:
                return 0
            grid[r][c]=0
            return(1+dfs(r+1,c)+dfs(r-1,c)+dfs(r,c-1)+dfs(r,c+1))
        
        for i in range(n):
            for j in range(m):
                if grid[i][j]==1:
                    area = dfs(i,j)
                    maxsize = maxsize if maxsize > area else area
        return maxsize
            
        
