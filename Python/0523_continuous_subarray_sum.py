class Solution(object):
    def checkSubarraySum(self, nums, k):
        hashmap = {0:-1}
        running_sum = 0

        for i in range(len(nums)):
            running_sum+=nums[i]
            remainder = running_sum%k

            if remainder in hashmap:
                if i - hashmap[remainder]>1:
                    return True
            else:
                hashmap[remainder] = i
        return False
        
        return False
