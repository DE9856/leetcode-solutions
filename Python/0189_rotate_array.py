class Solution(object):
    def rotate(self, nums, k):
        n = len(nums)
        k = k%n
        
        nums[:] = nums[::-1]
        nums[:k] = nums[:k][::-1]
        nums[k:] = nums[k:][::-1]

        return nums
        
