class Solution(object):
    def racecar(self, target):
        values = [[0,1,0]]
        visited = {(0,1)}
        head = 0

        while head < len(values):
            position, speed, stepcount = values[head]
            head+=1

            if position == target:
                return stepcount

            posA=position+speed
            speedA = speed *2 
            if 0<=posA<2*target and (posA,speedA) not in visited:
                visited.add((posA,speedA))
                values.append([posA,speedA,stepcount+1])

            speedR = -1 if speed>0 else 1
            if(position,speedR) not in visited: 
                visited.add((position,speedR))
                values.append([position,speedR,stepcount+1])
        
