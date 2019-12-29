for i in range(1,7): #十位數印出1~6
    for j in range(1,i+1): #印出從1開始小於等於十位數的個位數
        number = str(i)+str(j) #合併十位數和個位數
        print(number.ljust(3),end='') #字串向左補齊，若字串不夠長則自動補空白，輸出完成不換行
        # number = i*10+j #用數字格式來做
        # print('{: <3d}'.format(number),end='') #字串向左補齊三位數，若字串不夠長則自動補空白，輸出完成不換行
    print('\n',end='') #輸出完一個十位數循環就換一行。如果不加end=''，會換兩行，因為print內建就會換一行，\n又換一行。如果不輸出\n會換兩行