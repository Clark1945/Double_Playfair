#參考：https://github.com/justworm/playfair-cipher
import numpy as np

def matrix(key,offset):
	# print('offset',offset)
	matrix=[] #將key插入列表
	for e in key.upper():
		if e not in matrix:
			matrix.append(e)
                
	alphabet="ABCDEFGHIKLMNOPQRSTUVWXYZ" #將剩餘的字母插入列表
	for e in alphabet:
		if e not in matrix:
			matrix.append(e)	

# 	matrix2=[] #用message的長度做凱薩加密法
# 	for i in matrix:
# 		num=ord(i)
# 		if num+offset>90:
# 			num=num+offset-26
# 		else:
# 			num+=offset
# 		matrix2.append(chr(num))

	matrix_group=[] #將列表分為五個字一組
	for e in range(5):
		matrix_group.append('')
	matrix_group[0]=matrix[0:5]
	matrix_group[1]=matrix[5:10]
	matrix_group[2]=matrix[10:15]
	matrix_group[3]=matrix[15:20]
	matrix_group[4]=matrix[20:25]
	return matrix_group

def message_to_digraphs(message_original): #將訊息整理成列表

	message=[] #建立訊息列表
	for e in message_original:
		message.append(e)

	for unused in range(len(message)): #刪除空白
		if " "  in message:
			message.remove(" ")

	i=0 #重覆出現的字母中穿插X
	for e in range(int(len(message)/2)):
		if message[i] == message[i+1]:
			message.insert(i+1,'X')
		i=i+2

	if len(message)%2==1: #如果是奇數，則最後加上X
		message.append("X")
	
	i=0  #將訊息分為兩個字一組
	new=[]
	for x in range(1,int(len(message)/2)+1):
		new.append(message[i:i+2])
		i+=2
	
	return new


def find_position(key_matrix,letter): #尋找字母的座標
	x=y=0 
	for i in range(5):
		for j in range(5):
			if key_matrix[i][j]==letter:
				x=i
				y=j
	return x,y

def encrypt(message): #加密訊息
	message=message_to_digraphs(message)
	for key_count in key_list: 
	#	print(key_count)
		key_matrix=np.transpose(matrix(key_count,len(message)))
		cipher=[]
		for e in message:
			p1,q1=find_position(key_matrix,e[0]) #p=第幾列,q=第幾行
			p2,q2=find_position(key_matrix,e[1])
			if p1==p2: #同列時，行+1
				if q1==4:
   					q1=-1
				if q2==4:
					q2=-1
				cipher.append(key_matrix[p1][q1+1])
				cipher.append(key_matrix[p1][q2+1])
			elif q1==q2: #同行時，列+1
   				if p1==4:
   					p1=-1
   				if p2==4:
   					p2=-1
   				cipher.append(key_matrix[p1+1][q1])
   				cipher.append(key_matrix[p2+1][q2])		
			else: #不同行列時，行互換
   				cipher.append(key_matrix[p1][q2])
   				cipher.append(key_matrix[p2][q1])
		print("矩陣加密:")
		for xx in key_matrix:
			print(xx)
		message=message_to_digraphs("".join(cipher))
		print("\n",cipher)
	return cipher

def cipher_to_digraphs(cipher): #將訊息整理成列表
	i=0
	new=[]
	for x in range(int(len(cipher)/2)):
		new.append(cipher[i:i+2])
		i=i+2
	return new

def decrypt(cipher): #解密訊息
	cipher=cipher_to_digraphs(cipher) #cipher就是message
	for key_count in key_list[::-1]:
		
		key_matrix=np.transpose(matrix(key_count,len(cipher)))
# 		print(matrix(key_count,len(cipher)))
# 		for xx in key_matrix:
# 			print(xx)
		
		plaintext=[]
		for e in cipher:
			p1,q1=find_position(key_matrix,e[0])
			p2,q2=find_position(key_matrix,e[1])
			if p1==p2: #同列時，行-1
				if q1==4:
					q1=-1
				if q2==4:
					q2=-1
				plaintext.append(key_matrix[p1][q1-1])
				plaintext.append(key_matrix[p1][q2-1])		
			elif q1==q2: #同行時，列-1
				if p1==4:
					p1=-1
				if p2==4:
					p2=-1
				plaintext.append(key_matrix[p1-1][q1])
				plaintext.append(key_matrix[p2-1][q2])
			else: #不同行列時，行互換
				plaintext.append(key_matrix[p1][q2])
				plaintext.append(key_matrix[p2][q1])
			#print(plaintext)
			i=0 #刪除夾在中間的X
			for e in range(int(len(plaintext)/2)-2):
				if plaintext[i]==plaintext[i+2] and plaintext[i+1]=='X':
					del plaintext[i+1]
				i=i+2
		
			if plaintext[-1]=='X': #刪除最後的X
				del plaintext[-1]

			output=""
			for e in plaintext:
				output+=e
# 		print(output)
		cipher=cipher_to_digraphs(output)
            
	return output
# def encrypt2(key_list,message):
#     for key_count in key_list:
#             message=message_to_digraphs(message)
#             key_matrix=np.transpose(matrix(key_count,len(message)))
    

key1='information'
key_list=[]
key_list.append(key1)
key_list.append(key1[::-1])
#for ke in key_list:
#    print(ke)
print ("\n鑰匙: ")
print(key1)

message='KDANGG'
print ("\n原始訊息: ")
print (message)

print ("\n訊息轉列表: ")
print (message_to_digraphs(message))

#print ("\n鑰匙矩陣: ")
matrixkey=matrix(key1,len(message_to_digraphs(message)))
matrixkey=np.transpose(matrixkey)
#for i in matrixkey:
#	print (i)
#print ("\n密文: " )
encryptmessage=encrypt(message)
print ("密文:",''.join(encryptmessage))

print('\n明文：')
print(decrypt(encryptmessage))

