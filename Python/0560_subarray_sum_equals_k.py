class Solution(object):
    def subarraySum(self, nums, k):
        count = 0
        prefix_sum = 0
        hashmap = {0:1}

        for num in nums:
            prefix_sum+=num
            if(prefix_sum-k) in hashmap:
                count+= hashmap[prefix_sum-k]

            hashmap[prefix_sum] = hashmap.get(prefix_sum,0)+1
        return count
        
