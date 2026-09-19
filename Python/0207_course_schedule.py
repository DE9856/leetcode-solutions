class Solution(object):
    def canFinish(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: bool
        """
        graph = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[course].append(prereq)
        visited = [0] * numCourses
        def dfs(course):
            if visited[course] == 1:
                return False
            if visited[course] == 2:
                return True
            visited[course] = 1
            for prereq in graph[course]:
                if not dfs(prereq):
                    return False
            visited[course] = 2
            return True
        for course in range(numCourses):
            if not dfs(course):
                return False
        return True
        
