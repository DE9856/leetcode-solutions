class Solution(object):
    def maximumUnits(self, boxTypes, truckSize):
        boxTypes.sort(key = lambda x: x[1], reverse = True)
        total_units = 0
        for boxes,units in boxTypes:
            if truckSize==0:
                break
            take = min(boxes, truckSize)
            total_units+=take*units
            truckSize-=take
        return total_units
        
