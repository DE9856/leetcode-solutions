class Solution(object):
    def smallerNumbersThanCurrent(self, nums):
        nums2 = nums[:]
        nums2.sort()
        for i in range(len(nums)):
            nums[i] = nums2.index(nums[i])
        return nums
        
