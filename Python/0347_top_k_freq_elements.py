class Solution(object):
    def topKFrequent(self, nums, k):
        d1 = {}
        for num in nums:
            d1[num] = d1.get(num,0)+1

        l1 = sorted(d1,key = d1.get,reverse = True)

        return l1[:k]
