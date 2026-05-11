class Solution(object):
    def sortedSquares(self, nums):
        for i in range(len(nums)):
            nums[i] = nums[i]**2
        nums.sort()
        return nums

#or

class Solution(object):
    def sortedSquares(self, nums):
        n = len(nums)
        ans = [0]*n
        left = 0
        right = n-1
        pos = n-1
        while left<=right:
            ls = nums[left]**2
            rs = nums[right]**2
            if ls > rs:
                ans[pos] = ls
                left+=1
            else:
                ans[pos] = rs
                right -=1

            pos -=1
        return ans
