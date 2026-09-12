class Solution(object):
    def maximumWeight(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[int]
        """
        n = len(intervals)
        intervals = [[start, end, weight, i] for i, (start, end,weight) in enumerate(intervals)]
        intervals.sort()
        dp = [[None]*5 for _ in range(n+1)]
        def solve(i,j):
            if i==n or j==4:
                return (0,[])
            if dp[i][j] is not None:
                return dp[i][j]
            skipped = solve(i+1,j)
            start,end,weight,index = intervals[i]
            left = i+1
            right = n
            while left<right:
                mid = (left+right)//2
                if intervals[mid][0]>end:
                    right = mid
                else:
                    left = mid+1
            next_weight,next_indices = solve(left,j+1)
            take = (weight + next_weight, sorted([index] + next_indices))
            if take[0] > skipped[0]:
                ans = take
            elif take[0] < skipped[0]:
                ans = skipped
            else:
                ans = min(take, skipped)
            dp[i][j] = ans
            return ans
        return sorted(solve(0, 0)[1])

        
