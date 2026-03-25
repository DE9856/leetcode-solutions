class Solution(object):
    def findMaxAverage(self, nums, k):
        window_sum=0
        for i in range(k):
            window_sum+=nums[i]
        max_sum = window_sum
        for i in range(k, len(nums)):
            window_sum+=nums[i]
            window_sum-=nums[i-k]
            max_sum = window_sum if window_sum > max_sum else max_sum
        
        return max_sum/float(k)
                

        
