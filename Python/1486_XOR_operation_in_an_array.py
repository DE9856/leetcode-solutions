class Solution(object):
    def xorOperation(self, n, start):
        nums = []
        for i in range(n):
            nums.append(start+2*i)
        ans = nums[0]
        for i in range(1,n):
            ans = ans ^ nums[i]
        return ans
        
