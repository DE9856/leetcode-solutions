class Solution(object):
    def longestOnes(self, nums, k):
        maxfreq = 0
        left = 0
        count = 0

        for right in range(len(nums)):
            if(nums[right]==0):
                count+=1
            while count>k:
                if(nums[left]==0):
                    count-=1
                left+=1
            maxfreq = maxfreq if maxfreq > right-left+1 else right-left+1
        return maxfreq
