class Solution(object):
    def largestOverlap(self, img1, img2):
        """
        :type img1: List[List[int]]
        :type img2: List[List[int]]
        :rtype: int
        """
        n = len(img1)
        ans = 0
        for dx in range(-n + 1, n):
            for dy in range(-n + 1, n):
                count = 0
                for i in range(n):
                    for j in range(n):
                        x = i + dx
                        y = j + dy
                        if 0 <= x < n and 0 <= y < n:
                            if img1[i][j] == 1 and img2[x][y] == 1:
                                count += 1
                ans = max(ans, count)
        return ans
        
