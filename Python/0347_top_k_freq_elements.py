class Solution(object):
    def topKFrequent(self, nums, k):
        d1 = {}
        for num in nums:
            d1[num] = d1.get(num,0)+1

        l1 = sorted(d1,key = d1.get,reverse = True)

        return l1[:k]


# or using hashmaps
class Solution(object):
    def topKFrequent(self, nums, k):
        hashmap = {}
        for num in nums:
            if num in hashmap:
                hashmap[num]+=1
            else:
                hashmap[num]=1
        
        items = hashmap.items()
        items.sort(key = lambda x: x[1], reverse = True)
        result = []
        for i in range(k):
            result.append(items[i][0])

        return result
