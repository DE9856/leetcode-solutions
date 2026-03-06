class Solution(object):
    def containsDuplicate(self, nums):
        nums1 = set()
        for i in nums:
            if i in nums1:
                return True
            nums1.add(i)
        return False
        
