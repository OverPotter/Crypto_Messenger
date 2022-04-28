import random
import re
import string
from hashlib import sha256, sha512

"""
Реализован модуль алгоритма OAEP, содержит следующие функции:
	#OAEP_encr - шифрует текст
	#OAEP_decr - дешифрует текст
	#integrity - проверка целостности 
	#output - выводит зашифрованное сообщение

Рандомное число генерируется с помощью случайной строки, которая далее
подвергается алгоритму хеширования sha256 

Текст должен соответсвовать следующиму условию:
#	try: mess < 2**256
#	except ValueError:
#    	"{0} the biggest 2**256".format(mess)
#    	raise SystemExit
"""
list_az = []
list_AZ = []
list_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
list_spec_symb = ['%', '*', ')','?', '@', '#', '$', '~', '(', '!', '_']
str_for_hash = ""

a = string.ascii_lowercase
for i in a: list_az.append(i)

a = string.ascii_uppercase
for i in a: list_AZ.append(i)

rand_len = random.randint(6, 10)

for i in range(0, rand_len):
	num_list = random.randint(0, 3)
	if num_list == 0:
		symb_in_list = random.randint(0, 25)
		str_for_hash += list_az[symb_in_list]
	elif num_list == 1:
		symb_in_list = random.randint(0, 25)
		str_for_hash += list_AZ[symb_in_list]     
	elif num_list == 2:
		symb_in_list = random.randint(0, 9)
		str_for_hash += str(list_nums[symb_in_list])   
	else:
		symb_in_list = random.randint(0, 10)
		str_for_hash += list_spec_symb[symb_in_list]

def OAEP_encr(messege):
	messege = messege.encode()
	mess = int.from_bytes(messege, 'big', signed = False)
	mess <<= 256
	rand_int = int(sha256(str_for_hash.encode()).hexdigest(),16)
	expansion_rand_int = int(sha512(rand_int.to_bytes(32, 'big', signed = False)).hexdigest(),16)
	encr_mess_step_1 = mess^expansion_rand_int
	compression_encr_mess = int(sha256(encr_mess_step_1.to_bytes(64, 'big', signed = False)).hexdigest(),16)
	encr_mess_step_2 = rand_int^compression_encr_mess
	result_encr = (encr_mess_step_1<<256) | encr_mess_step_2
	return result_encr

def OAEP_decr(result_encr):
	re_encr_mess_step_1 = result_encr>>256
	re_encr_mess_step_2 = result_encr & (2**256 - 1)
	re_compression_encr_mess = int(sha256(re_encr_mess_step_1.to_bytes(64, 'big', signed = False)).hexdigest(),16)
	re_rand_int = re_encr_mess_step_2^re_compression_encr_mess
	re_expansion_rand_int = int(sha512(re_rand_int.to_bytes(32, 'big', signed = False)).hexdigest(),16)
	re_mess = re_encr_mess_step_1^re_expansion_rand_int
	return re_mess

def integrity(re_mess):
	re_mess >>= 256
	size = 3
	re_mess = str(re_mess.to_bytes(64, 'big', signed = False))
	re_mess = re_mess[2:-1]
	re_mess = re.sub(r'[\\\\]', '', re_mess)
	len_mess = len(re.sub(r'x0{2}', '', re_mess))
	re_mess = re_mess[:-len_mess] 
	byte_list = []

	while len(re_mess) > size:
		pice = re_mess[:size]
		byte_list.append(pice)
		re_mess = re_mess[size:]
	byte_list.append(re_mess)

	for i in range(0, len(byte_list)):
		while len(byte_list[i]) != 3: byte_list[i] += "0"

	for i in range(0, len(byte_list)):
		if bool(re.search(r'x0{2}', byte_list[i])) == True: pass
		else: pass #print('Broken messege integrity')

def output(re_mess):
	result_messege = str(re_mess.to_bytes(64, 'big', signed = False))
	sign_1 = "b'\\x00"
	sign_2 = "\\x00"
	result_messege = result_messege.replace(sign_1, "").replace(sign_2, "")
	result_messege = result_messege[:-1]
	return result_messege