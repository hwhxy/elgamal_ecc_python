#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: HWHXY

import sympy
import math
import random
import sys
import binascii
sys.setrecursionlimit(431005529)

_mrpt_num_trials=5
#判断大整数是不是素数
#mil判定素数方法

def is_probable_prime(n):
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)

    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True # n is definitely composite

    for i in range(_mrpt_num_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False

    return True # no base tested showed n as composite
#生成大整数p
def Ramdom_Prime(x):
    s=""
    for i in range(x):
        if i == x-1:
            s+=str(int(random.randrange(1,9,2)))
        else:
            s+=str(int(random.randint(0,9)))
    n = int(s)
    if is_probable_prime(n) == True:
        print n
        return n
    else:
        while False == is_probable_prime(n):
            n += 2
            i += 1
            if i > 123456789:
                print "i try!"
                break;
        return n

p=Ramdom_Prime(256)
#指数快速幂
def fastExpMod(b, e, m):
    result = 1
    while e != 0:
        if (e&1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
        e >>= 1
        # b, b^2, b^4, b^8, ... , b^(2^n)
        b = (b*b) % m
    return result

def randomAB(x):
	s=""
	for i in range(x):
		s+=str(int(random.randint(0,9)))
	A = int(s)
	s=""
	for i in range(x):
		s+=str(int(random.randint(0,9)))
	B = int(s)
	if 4*fastExpMod(A,3,p)+27*fastExpMod(B,2,p) % p !=0:
		return A,B

A,B= randomAB(256)
#椭圆曲线方程
def equation(x):
	return (x**3 + A*x + B) % p


#判定是否二次剩余，勒让德符号
def isremainder(g,p):
	if fastExpMod(g,(p-1)/2,p) == 1:
		return 1
	else:
		return 0

#求解二次剩余
def tworemainder(g,p):
	if g == 0:
		y = 0
		return y
	if p % 4 == 3:
		u = p / 4
		y = fastExpMod(g,u+1,p)
		z = y**2 % p
		if z == g:
			return y
	if p % 5 == 8:
		u = p / 8
		z = fastExpMod(g,2*u+1,p)
		if z == 1 :
			y = fastExpMod(g,u+1,p)
			return y
		elif z == p-1 :
			y = 2*g*fastExpMod(4*g,u,p) % p
			return y


#判断y是否为平方数
def issql(n):
    a = int (math.sqrt(n))
    if n == a*a :
        return 1
    else:
        return 0

#生成G点
def g_():
	i = random.randint(1,10000)
	while 1:
		n = equation(i)
		if isremainder(n,p) == 1:
			return i % p , tworemainder(n,p)
		i+=1

#欧几里得算法求最大公约数
def get_gcd(a, b):
	k = a // b
	remainder = a % b
	while remainder != 0:
		a = b
		b = remainder
		k = a // b
		remainder = a % b
	return b

#改进欧几里得算法求线性方程的x与y
def get_(a, b):
	if b == 0:
		return 1, 0
	else:
		k = a // b
		remainder = a % b
		x1, y1 = get_(b, remainder)
		x, y = y1, x1 - k * y1
	return x, y

#ecc点加法
def add(x1,y1,x2,y2,p):
	if x1 == x2 and y1 == y2:
		denominator,d=get_(2*y1,p)
		denominator = denominator % p
		numerator = (3*(x1**2) + 1)
		k = (numerator * denominator) % p
		x3 = k**2 -x1 -x2
		y3 = k*(x1-x3)-y1
		x3 = x3 % p
		y3 = y3 %p
		return x3,y3
	else:
		denominator,d=get_(x2-x1,p)
		denominator = denominator % p
		numerator = y2 -y1
		k = (numerator * denominator) % p
		x3 = k**2 -x1 -x2
		y3 = k*(x1-x3)-y1
		x3 = x3 % p
		y3 = y3 % p
		return x3,y3

#n倍点加法
def nadd(n,x1,y1,p):
	i=1
	x3=x1
	y3=y1
	while i<n :
		x3,y3=add(x3,y3,x1,y1,p)
		i=i+1
	return x3,y3
#明文转化成大数
def string_to_int(s):
	return int(binascii.b2a_hex(s),16)

#数转化成字符串
def int_to_string(i):
	return binascii.a2b_hex(hex(i)[2:-1])
#明文转化为点坐标
def inttopoint(m):
    for i in range(1000):
		n = equation(m+i)
		if isremainder(n,p) == 1 and tworemainder(n,p)!=None:
			return m+i,tworemainder(n,p),i


#明文
m="wangxiyu"
m=string_to_int(m)
#明文坐标(x,y),明文为x-i
mx,my,i = inttopoint(m)
print "<=========================Encrypted information coordinates=========================>"
print "("+str(mx)+","+str(my)+"),i="+str(i)
#mx,my,i = 72,611,62
# G点
gx,gy=g_()
print "<=========================       This is G coordinates     =========================>"
print "("+str(gx)+","+str(gy)+")"
#gx,gy = 18196,20730



#gx,gy=4,0
# 阶
n = p
#私钥
private_key=random.randint(1,p)
#private_key=22
print "<=========================       This is A,B parameter     =========================>"
print "("+str(A)+","+str(B)+")"
print "<=========================      This is my private key     =========================>"
print "private_key: "+ str(private_key)
#公钥
public_keyx,public_keyy= nadd(private_key,gx,gy,p)
print "<=========================      This is my public key      =========================>"
print "public_key: "+"{Y :"+"("+str(public_keyx)+","+str(public_keyy)+"), E:y2=x3+ax+b ,G: "+"("+str(gx)+","+str(gy)+")}"

#加密
k=random.randint(1,n-1)
encrypt_x1,encrypt_y1=nadd(k,gx,gy,p)
#print encrypt_x1,encrypt_y1
a,b=nadd(k,public_keyx,public_keyy,p)
encrypt_x2,encrypt_y2=add(mx,my,a,b,p)
#print encrypt_x2,encrypt_y2
print "<=========================   This is my encrpt coordinates =========================>"
print "encrption:{kG: "+"("+str(encrypt_x1)+","+str(encrypt_y1)+"),m+kY: "+"("+str(encrypt_x2)+","+str(encrypt_y2)+")}"

#解密
decrypt_x,decrypt_y=nadd(private_key,encrypt_x1,encrypt_y1,p)
decrypt_x,decrypt_y=add(encrypt_x2,encrypt_y2,decrypt_x,decrypt_y*(-1),p)
print "<======================   This is my encrption information   =======================>"
print "encrption:" + str(m)
print "<======================   This is my decrption coordinates   =======================>"
print "decryption:{m:"+"("+str(decrypt_x)+","+str(decrypt_y)+") , i :"+str(42)+"}"
print "<======================   This is my decrption information   =======================>"
print "decryption: "+int_to_string(decrypt_x-i)
