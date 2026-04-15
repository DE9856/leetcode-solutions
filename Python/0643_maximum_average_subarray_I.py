class Solution(object):
    def findMaxAverage(self, nums, k):
        sum1 = sum(nums[0:k])
        maxsum = sum1
        for i in range(k,len(nums)):
            sum1-=nums[i-k]
            sum1+=nums[i]
            maxsum = sum1 if sum1 > maxsum else maxsum
        return maxsum/float(k)
        
