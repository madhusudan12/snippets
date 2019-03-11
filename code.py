t=int(input())
for a0 in range(t):
    n,a,b,k=map(int,input().split())
    na=n//a
    nb=n//b
    nab=n//(a*b)
    res=na+nb-2*nab
    if res>=k:
        print("Win")
    else:
        print("Lose")
