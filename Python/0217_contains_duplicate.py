#implementation using set
class Solution(object):
    def containsDuplicate(self, nums):
        nums1 = set()
        for i in nums:
            if i in nums1:
                return True
            nums1.add(i)
        return False

#or

#hashmap implementation
class Solution(object):
    def containsDuplicate(self, nums):
        hashmap = {}
        for num in nums:
            if num in hashmap:
                return True
            hashmap[num] = 1

        return False
