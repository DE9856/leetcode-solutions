class Solution(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        candidates.sort()
        result = []
        def solve(i,current,total):
            if total==target:
                result.append(current[:])
                return
            if i==len(candidates) or total > target:
                return
            current.append(candidates[i])
            solve(i,current,total+candidates[i])
            
            current.pop()
            solve(i+1,current,total)
        solve(0,[],0)
        return result

        
