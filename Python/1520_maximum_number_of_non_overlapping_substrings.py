class Solution(object):
    def maxNumOfSubstrings(self, s):
        """
        :type s: str
        :rtype: List[str]
        """
        table = {}
        intervals = []

        for i in range(len(s)):
            ch = s[i]
            if ch not in table:
                table[ch]=[i,i]
            else:
                table[ch][1] = i

        for ch in table:
            left = table[ch][0]
            right = table[ch][1]
            i = left
            valid = True
            while i<=right:
                char = s[i]
                if table[char][0]<left:
                    valid = False
                    break
                right = max(right, table[char][1])
                i+=1
            if valid:
                intervals.append([left,right])

        intervals.sort(key=lambda x: x[1])
        result = []
        k = -1
        
        for left, right in intervals:
            if left>k:
                result.append(s[left:right + 1])
                k = right
        return result
