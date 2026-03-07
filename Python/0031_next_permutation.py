class Solution(object):
    def nextPermutation(self, nums):
        length = len(nums)
        i = length-2
        while(i>=0 and nums[i]>=nums[i+1]):
            i-=1
        if i>=0:
            last = length-1
            while(nums[last]<=nums[i]):
                last-=1
            nums[i],nums[last] = nums[last],nums[i]
        nums[i+1:] = reversed(nums[i+1:])
        
