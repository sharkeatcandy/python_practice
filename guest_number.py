# -*- coding: UTF-8 -*-
import random    
import string    

def set_ans():    
    a=[]          
    ans=''        
    while(len(a)<4):    
        ans_num=random.randint(0,9)    
        if(ans_num not in a):          
            a.append(ans_num)
        else:
            continue
    for i in range(4):                 
        ans+=str(a[i])
    return ans
    
def guest(guest_num,ans):
    A=0
    B=0
    status=''    
    if(guest_num.isnumeric()==False or len(guest_num)!=4):
        print('Error input')    
        return None
    if(guest_num==ans):    
        print('Correct!')
        return True             
    for i in range(4):          
        if(guest_num[i] in ans):
            if(i==ans.find(guest_num[i])):
                A+=1
            else:                         
                B+=1
    print("Guess： "+guest_num+'； Result： '+str(A)+'A'+str(B)+'B')
    return status
    
    
if __name__ == "__main__":
    status=False
    # ans=set_ans()
    ans = "3478"
    while not status:
        print('請猜四位數字：', end='')
        guest_num=input()
        status=guest(guest_num,ans)