class Solution(object):
    def merge(self, intervals):
        intervals = sorted(intervals, key = lambda x:x[0])
        final = []
        start,end = intervals[0]
        for s,e in intervals[1:]:
            if s<=end:
                end = max(end,e)
            else:
                final.append([start,end])
                start,end = s,e
        final.append([start,end])
        return final 
