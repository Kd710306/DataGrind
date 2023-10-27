
from collections import defaultdict
def check(p,q):
    if  type(p)!=dict and type(q)!=dict:
        return True
    if type(p)!=dict and type(q)==dict:
        return False
    if type(p)==dict and type(q)!=dict:
        return False
    keys1=list(p.keys())
    keys1.sort()
    keys2=list(q.keys())
    keys2.sort()
    if keys1!=keys2:
        return False
    for i in keys1:
        if type(p[i])!=type(q[i]):
            return False
        if type(p[i])==dict:
            if not check(p[i],q[i]):
                return False
        if type(p[i])==list:
            if len(p[i]) and len(q[i]) and not check(p[i][0],q[i][0]) :
                return False
    return True
def getJsonFormats(jsonList):
    n=len(jsonList)
    vis=[0]*n
    d=defaultdict(list)
    for i in range(n):
        if vis[i]==0:
            d[i].append(i)
            vis[i]=1
            for j in range(i+1,n):
                if check(jsonList[i],jsonList[j]):
                    vis[j]=1
                    d[i].append(j)
    sol=defaultdict(list)
    count=defaultdict(int)
    i=1
    for key, val in d.items():
        for index in val:
            sol['format_'+str(i)].append(jsonList[index])
            count['format_'+str(i)]+=1
        i+=1
    return {"formats":sol, "fomats_counts":count}



