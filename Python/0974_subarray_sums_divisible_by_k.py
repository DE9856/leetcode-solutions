class Solution(object):
    def subarraysDivByK(self, nums, k):
        remainder_count = {0:1}
        prefix_sum=0
        count = 0
        for num in nums:
            prefix_sum+= num
            remainder = prefix_sum % k
            if remainder < 0:
                remainder+=k
            if remainder in remainder_count:
                count+=remainder_count[remainder]
            remainder_count[remainder] = remainder_count.get(remainder,0)+1
        return count
        
