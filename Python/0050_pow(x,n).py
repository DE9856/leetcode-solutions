double myPow(double x, int n) {
    double prod = 1;
    if(n>=0)
        for(int i=0;i<n;i++)
            prod *=x;
    else
        for(int i=0;i<-n;i++)
            prod /=x;
    return prod;
}
