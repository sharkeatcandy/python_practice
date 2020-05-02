def count_str(input_str, specific_str):#帶入字串和要找的字並計算出現次數
    input_str=input_str.lower() #字串轉小寫
    count=input_str.count(specific_str) #python內建的計算出現次數函式
    return count #回傳找到的次數
    
if __name__ == "__main__":
    txt_read = open('count_str_in_text.txt', 'r', encoding = 'UTF-8').read() #打開檔案
    str1='p' #設定第一個需要找的字
    count_char1=count_str(str(txt_read), str1) #把檔案轉成string(字串)，和要找的字一起傳給函式
    
    str2='y'#設定第二個需要找的字
    count_char2=count_str(str(txt_read), str2) #把檔案轉成string(字串)，和要找的字一起傳給函式

    print('Python Project 之中 %s 的出現次數是 %d'%(str1, count_char1)) #把第一個要找的字和出現次數印出來
    print('Python Project 之中 %s 的出現次數是 %d'%(str2, count_char2)) #把第二個要找的字和出現次數印出來