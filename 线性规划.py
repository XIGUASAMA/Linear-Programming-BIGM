#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import re
import copy
import sys
from scipy import optimize
M=-99999


# In[2]:


f=open("input.txt", "r", encoding="utf-8")
str_f=f.read()
f.close()


# In[3]:


list_origin=[]
list_origin=str_f.split("\n")


# In[4]:


def confirm():
    xmax=1
    for i in list_origin:
        while(1):
            if "x"+str(xmax) in i:
                xmax+=1
            else: break
    return xmax-1
xmax=xused=confirm()


# In[5]:


free=[]
positive=[]
negtive=[]
for i in range(1,xused+1):
    if "x"+str(i)+">=0" in list_origin:
        positive.append(i)
    elif "x"+str(i)+"<=0" in list_origin:
        negtive.append(i)
    else:
        free.append(i)


# In[6]:


for a in range(1,xused+1):
    for i in list_origin:
        if i == "x"+str(a)+">=0":
            list_origin.remove(i)


# In[7]:


GE_EQ=[]
Base=[]
NUM=[]
addxi=xused
l=1
def Normalization(i):
    global addxi,CE,EQ,NUM,l
    if "<=" in i:
        addxi+=1
        Base.append(addxi)
        return i.replace("<=","+x"+str(addxi)+"=")
    elif ">=" in i:
        GE_EQ.append(list_origin.index(i))
        NUM.append(l)
        l+=1
        addxi+=1
        return i.replace(">=","-x"+str(addxi)+"=")
    elif "=" in i and 'max'not in i and 'min' not in i:
        GE_EQ.append(list_origin.index(i))
        NUM.append(l)
        l+=1
    return i
list_normal=list(map(Normalization,list_origin))
del l

l=0
for i in GE_EQ:
    list_normal[i]=list_normal[i].replace("=","+x"+str(addxi+NUM[l])+"=") 
    l+=1
del l
artificial=[i+addxi for i in NUM]
for i in artificial:
    Base.append(i)

GE_ED=copy.deepcopy(NUM)
del NUM

k=0

if GE_EQ==[]:
    GE_EQ.append(0)

for i in list_normal:
    for j in range(1,addxi+1+max(GE_EQ)):
        i=list_normal[k]
        if ("*x"+str(j)) not in i:
            list_normal[k]=i.replace("x"+str(j),"1*x"+str(j))
    k+=1

fn=[[]]
p=0
for i in list_normal:
    num=0
    flag1=0
    flag2=0
    for j in i:
        if j in ["0","1","2","3","4","5","6","7","8","9"]:
            num=num+1
        if j is "-":
            if flag1==0:
                fn.append([])
                flag2=1
                flag=1
            fn[p].append(num)
    if flag2==0:
        fn.append([])
    p=p+1


# In[8]:


TEMP=[]
A=[]
max_GE=max(GE_EQ)
for i in range(len(list_normal)-1):
    A.append([])
    for j in range(addxi+max_GE):
        A[i].append(0)

B=[]
for i in range(len(list_normal)-1):
    B.append(0)

C=[0 for i in range(0,len(list_normal))]

for i in list_normal:
    temp=re.findall(r"\d+\.?\d*",i)
    TEMP.append(temp)
TEMP=list(map(lambda x:list(map(int, x)), TEMP))

for i in range(0,len(TEMP)):
    if fn != [[]]:
        for j in range(0,len(fn[i])):
            TEMP[i][fn[i][j]]=TEMP[i][fn[i][j]]*-1
    
for i in range(1,len(TEMP)):
    for j in range(0,len(TEMP[i])-1,2):
        A[i-1][TEMP[i][j+1]-1]=TEMP[i][j]

for i in range(1,len(list_normal)):
    B[i-1]=TEMP[i][-1]

C=TEMP[0][::2]
C += [0 for i in range(len(C),addxi)]
if "min" in list_origin[0]:
    CNEW=[-l for l in C]
else:
    CNEW=copy.deepcopy(C)
for i in range(max(GE_EQ)):
    CNEW.append(M)


# In[9]:


X=copy.deepcopy(A)
b=0
for i in X[::]:
    i.insert(0,B[b])
    b+=1
for i in range(len(X)):
    flag=0
    for j in range(1,len(X[i])):
        if (X[i][0]*X[i][j])>0 or X[i][0] == 0:
            flag=1
            break
    if flag == 0:
        print("Status: No Feasible Solution!")
        f=open("output.txt", "w", encoding="utf-8")
        f.truncate()
        f.write("Status: No Feasible Solution!"+"\n")
        f.close()
        sys.exit(2)


# In[10]:


check_number=[]
while(1):
    check_number.clear()
    j=0
    for i in X:
        i.insert(0,CNEW[Base[j]-1])
        j+=1
    for i in range(2,len(X[0])):
        summ=0
        for j in range(len(X)):
            summ+=X[j][0]*X[j][i]
        check_number.append(CNEW[i-2]-summ)
    if max(check_number)<=0:
        break;
    IN=check_number.index(max(check_number))+1
    theta=[X[i][1]/(X[i][IN+1]+0.000001) for i in range(len(X))]
    minnum=99999
    for i in theta:
        if i<minnum and i>0:
            minnum=i
    if minnum==99999:
        print("Status: Unbounded Solution!")
        f=open("output.txt", "w", encoding="utf-8")
        f.truncate()
        f.write("Status: Unbounded Solution!"+"\n")
        f.close()
        sys.exit(1)
    OUT=Base[theta.index(minnum)]
    position_line=theta.index(minnum)
    Base[position_line]=IN
    X_np=np.array(X)
    X_np = X_np.astype(np.float64)
    X_np = np.delete(X_np,0, axis = 1)
    X_np[position_line]=X_np[position_line]/X_np[position_line][IN]
    for i in range(len(X_np)):
        if i != position_line:
            X_np[i]=X_np[i]+(-X_np[i][IN]/X_np[position_line][IN])*X_np[position_line]
    X_np
    X=X_np.tolist()
    j=0


# In[11]:


f=open("output.txt", "w", encoding="utf-8")
f.truncate()
if list(set(Base).intersection(set(artificial)))!=[]:
    print("Status: No Feasible Solution!")
    f.write("Status: No Feasible Solution!"+"\n")
    f.close()
    sys.exit(2)
elif set([i+1 for i in range(len(check_number)) if check_number[i] == 0]) > set(Base):
    print("Status: Infinite Optimal Solutions!")
    f.write("Status: Infinite Optimal Solutions!"+"\n")
else:
    print("Status: Global Optimal Solution")
    f.write("Status: Global Optimal Solution"+"\n")
    
VALUE=[]
for i in range(len(X)):
    VALUE.append([X[i][1],Base[i]])
Displayed=[]

for i in range(len(VALUE)):
    if VALUE[i][1]<=xused:
        print("x"+str(VALUE[i][1])+" = %.3f"%VALUE[i][0])
        f.write("x"+str(VALUE[i][1])+" = %.3f"%VALUE[i][0]+"\n")
        Displayed.append(VALUE[i][1])

for i in range(1,xused+1):
    if i not in Displayed:
        print("x"+str(i)+" = 0")
        f.write("x"+str(i)+" = 0")
    
Objective_value=0
for i in range(len(VALUE)):
    Objective_value=Objective_value+VALUE[i][0]*CNEW[VALUE[i][1]-1]
if "min" in list_origin[0]:
    Objective_value=-1*Objective_value
print("Objective value: ",Objective_value)
f.write("Objective value: "+str(Objective_value)+"\n")
f.close()


# In[ ]:




