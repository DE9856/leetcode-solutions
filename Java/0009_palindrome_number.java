class Solution {
    public boolean isPalindrome(int x) {
        if(x<0)
            return false;
        int num=0;
        int original = x;
        int temp;
        while(x!=0){
            temp = x%10;
            num = (num*10) + temp;
            x = x/10;
        }   
        if(original==num)
            return true;
        else
            return false;
    }
}
