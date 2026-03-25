class Solution(object):
    def minWindow(self, s, t):
        if not s or not t:
            return "" #returns empty string is s or t are NULL

        need = {} #hashmap of frequency of characters in 't' string
        for c in t:
            need[c] = need.get(c,0)+1 #storing frequencies of characters in 't' string

        window = {} #hashmap of frequency of characters in window
        have = 0 #count of characters that have same amount of freuquency in window and t
        need_count = len(need) #length of characters that are needed

        res = [-1,-1] #stores left and right index value of shortest window
        res_len = float('inf') #stores length of res

        left = 0 #starting left pointer
        for right in range(len(s)): #sliding window right pointer
            c = s[right] #getting character in right index value
            window[c] = window.get(c,0)+1 #adds frequency of character in hashmap
            if c in need and window[c]==need[c]: #checks condition if character is in t string, and if frequency of character is same in 's' and 't' string
                have+=1 #incr

            while have == need_count: #loop used to see if its the same if windows is shrunk from left side
                if(right-left+1)<res_len: #condition if window length is less than minimum window length
                    res = [left,right] #adds left and right index values into res
                    res_len = right-left+1 #sets length of minimum window

                window[s[left]]-=1 #decrements left character frequency

                if s[left] in need and window[s[left]] < need[s[left]]: #checks if condition is satisfied
                    have -=1 #while loop gets broken
                left+=1 #moves pointer to the right side

        l,r = res #gets index values of result
        return s[l:r+1] if res_len !=float('inf') else "" #prints the output
        
