class Solution(object):
    def countSpecialIntegers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        dict = {}
        sol = 0
        for i in range(len(nums)):
            if nums[i] not in dict:
                dict[nums[i]] = [i]
            else:
                dict[nums[i]].append(i)

        for i in dict:
            if len(dict[i])==3:
                pos1, pos2, pos3 = dict[i]
                if pos3-pos2 == pos2 - pos1:
                    sol+=1
        return sol
                    
