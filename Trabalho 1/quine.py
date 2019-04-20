#coding: utf-8
import itertools

def cal_efficient(s): #teste de eficiencia
  count = 0
  for i in range(len(s)):
    if s[i] != '-':
      count+=1

  return count
  
def find_minimum(matriz, vetword): # funçao para achar o minimo
  P_final = []
  essential_prime = find_prime(matriz)
  essential_prime = deleteRedundant(essential_prime)

  for i in range(len(essential_prime)):
    for col in range(len(matriz[0])):
      if matriz[essential_prime[i]][col] == 1:
        for row in range(len(matriz)):
         matriz[row][col] = 0

    
  if check_all_zero(matriz) == True:
    P_final = [essential_prime]
  else:
        
    P = petrick_method(matriz)
    P_cost = []
    for prime in P:
      count = 0
      for i in range(len(vetword)):
        for j in prime:
          if j == i:
            count = count+ cal_efficient(vetword[i])
      P_cost.append(count)

    for i in range(len(P_cost)):
      if P_cost[i] == min(P_cost):
        P_final.append(P[i])

        
    for i in P_final:
      for j in essential_prime:
        if j not in i:
          i.append(j)

  
  return P_final
  
def find_prime(matriz): #funçao que encontra os primos essencias da tabela
  prime = []
  for col in range(len(matriz[0])):
    count = 0
    pos = 0
    for row in range(len(matriz)):
      if matriz[row][col] == 1:
        count += 1
        pos = row

    if count == 1:
      prime.append(pos)
  return prime

def check_all_zero(matriz): #checa zeros da matriz
  for i in matriz:
    for j in i:
      if j != 0:
        return False
  return True
  
def multiplication(list1, list2): #multiplicaçao usada no metodo de petrick
  list_result = []
  if len(list1) == 0 and len(list2)== 0:
    return list_result
  elif len(list1)==0:
    return list2
  elif len(list2)==0:
    return list1

  else:
    for i in list1:
      for j in list2:
        if i == j:
          list_result.append(i)
        else:
          list_result.append(list(set(i+j)))
    list_result.sort()
    return list(list_result for list_result,_ in itertools.groupby(list_result))
    
def petrick_method(matriz):
  P = []
  for col in range(len(matriz[0])):
    p =[]
    for row in range(len(matriz)):
      if matriz[row][col] == 1:
        p.append([row])
    P.append(p)
  for l in range(len(P)-1):
    P[l+1] = multiplication(P[l],P[l+1])

  P = sorted(P[len(P)-1],key=len)
  final = []
  min=len(P[0])
  for i in P:
    if len(i) == min:
      final.append(i)
    else:
      break

  return final

def converterd_b(n,cont):  #funçao para converter para binario
    binary = ""
    while(True):
        binary = binary + str(n%2)
        n = n//2
        if n == 0:
            break
    i=len(binary)
    for i in range(i,cont):
      binary=binary+str(0)
      
    binary = binary[::-1]
    return binary

def combine(vet,num):
  for i in range(len(vet)):
    if vet[i] != '_':
      if vet[i] != num[i]:
        return False

  return True
  
def compare(a,b):   #funçao que compara cada posiçao das strings passadas e checa se elas possuem pelo menos (tamanho -1) em comum
  c=""
  j=0
  cont=0
  for i in range(len(a)):
    if(a[i]!='_'):
      cont=cont+1
  for i in range(len(a)):
    if(a[i]==b[i]):
      j=j+1
  if(j==len(a)-1):      #se tiver mesmo tamanho -1 iguais 
    for i in range(len(a)): 
      if(a[i]==b[i]):   #se for iguais colocar em c
        c=c+a[i]
      else:             #senao coloca o traço
        c=c+'_'
  return c
  
def deleteRedundant(a): #funçao que deleta os valores repeditos que ficam no vetor quando se faz as reduçoes
  aux=[]
  for i in range(len(a)):
    for j in range(i+1,len(a)):
      if(a[i]==a[j]):
        aux.append(j)

  for i in range(len(aux)):
    del a[i]

  return a
  
def result(vetWord): #funçao para imprimir com letras
  for i in range(len(vetWord)):
	  for j in range(len(vetWord[i])):
		  if (vetWord[i][j] != '_'):
			  if(vetWord[i][j] == '1'):
				  print(chr(j+97), end="")
			  else:
				  print(chr(j+97)+"'", end="")

	  if(i != len(vetWord)-1):
		  print(" + ", end="")
	  else:
		  print("\n")

#texto='0101000111010001'
print("Entrada: ")
texto=input()
n=len(texto)
cont=0
while(n!=0):
  cont+=1
  n=n//2
table_ones=[]  
vetWord=[]    
contem=0
a=[] 
Reductions=[] 
vetorControle=[] 
flag=1
print("Entrada: ",texto)
for i in range(len(texto)):
  if (texto[i]=='1'):
    table_ones.append(i)

print("Min termos: ",table_ones)

for i in range(len(table_ones)):
  bina=converterd_b(table_ones[i],cont-1)
  a.append(bina)
  vetWord.append(bina)


while(flag==1):
  flag=0
  for i in range(len(vetWord)):
    value1 = ''.join(vetWord[i])
    for j in range(i+1,len(vetWord)):
      value2=''.join(vetWord[j])
      value2=compare(value1,value2) 
      if(value2!=""):
        flag=1
        Reductions.append(value2)  
        vetorControle.append(i)       
        vetorControle.append(j)
        
  for i in range(len(vetWord)): 
    if i not in vetorControle:
      Reductions.append(vetWord[i])
      

  vetWord=[]
  vetWord=Reductions 
  Reductions=[]
  vetorControle=[]

vetWord=deleteRedundant(vetWord)
matriz = [[0 for x in range(len(a))] for x in range(len(vetWord))]

for i in range(len(a)):
  for j in range (len(vetWord)):
    #term is same as number
    if combine(vetWord[j], a[i]):
      matriz[j][i] = 1
  
primes=find_minimum(matriz, vetWord)
final=[]
for prime in primes:
  for i in range(len(vetWord)):
    for j in prime:
      if j==i:
        final.append(vetWord[j])
       
print("Resultado: ")
result(final)
  
