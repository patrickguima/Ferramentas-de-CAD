#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int explorado[100000];
int posicao[8];

typedef struct Folha folha;
struct Folha{
	folha *pai;
	char movimento;
	int i;
	int j;
	int custo;
	int custo2;
};
typedef struct Fila fila;
struct Fila{
	fila *next;
	folha *estado;
	fila *prev;
};
int setExplorado(int i, int j, int T){
	return ((T*(i-1))+(j-1));
}
int sucessores(char M[][100],int i, int j,int tamColuna){
	int size=0;
	int cont=0;
	if(M[i-1][j]!='#' && explorado[setExplorado(i-1,j,tamColuna)]!=1){ //UP
		
		posicao[size]=i-1;
		posicao[size+1]=j;
		size=size+2;
		cont++;
		
	}
	if(M[i][j-1]!='#' && explorado[setExplorado(i,j-1,tamColuna)]!=1){// LEFT
		posicao[size]=i;
		posicao[size+1]=j-1;
		size=size+2;
		cont++;
	}
	if(M[i+1][j]!='#' && explorado[setExplorado(i+1,j,tamColuna)]!=1){ //DOWN
		posicao[size]=i+1;
		posicao[size+1]=j;
		size=size+2;
		cont++;
	}
	if(M[i][j+1]!='#' && explorado[setExplorado(i,j+1,tamColuna)]!=1){ //RIGHT
		posicao[size]=i;
		posicao[size+1]=j+1;
		size=size+2;
		cont++;
	}

	return cont;

	

}
fila *insereFila(fila *L,folha *H){
	fila *auxFila2=L;
	fila *auxFila=malloc(sizeof(fila));
	auxFila->estado=H;
	
	while(1){
		
		if( L->estado->custo > H->custo){
			auxFila->next=L;
			auxFila->prev=L->prev;
			L->prev->next=auxFila;
			L->prev=auxFila;
			return auxFila2;
		}else{
			if(L->next==NULL){
				L->next=auxFila;
				auxFila->next=NULL;
				auxFila->prev=L;
				return auxFila2;
		}}
	
		
		L=L->next;
	}
		
	free(auxFila);	
	return auxFila2;
}

fila *retiraFila(fila *L){
	fila *aux=L;
	L->prev=NULL;
	L=L->next;
	L->prev=NULL;
	return L;
}
int main(){
	int encontrou = 0;
	char nomeFile[30];
	int i=0,j=0;
	int iInicial=1,jInicial=1;
	int iFinal=1,jFinal=1;
	int numSucessores;
	int tamLinhas=0;
	int tamColuna=0;
	char M[100][100];
	char c;

	FILE *F;
	folha *auxH;
	fila *L=malloc(sizeof(fila));
	folha *H=malloc(sizeof(folha));

	H->pai=NULL;
	H->custo=1;
	
	L->next=NULL;
	L->prev=NULL;
	L->estado=H;
	printf("informe o labirinto: ");
	scanf("%s", nomeFile);
	F = fopen(nomeFile,"r");
	while((c=(fgetc(F)))!=EOF){
		if(c=='I'){
			iInicial=i;
			jInicial=j;
		}
		if(c=='F'){
			iFinal=i;
			jFinal=j;
		}
		if(c=='\n'){

			i++;
			tamColuna=j;
			j=0;

		}
		else{
			M[i][j]=c;
			j++;
		}
		
	}
	
	tamLinhas=i+1;
	i=0;
	j=0;

	
	fclose(F);
	H->i=iInicial;
	H->j=jInicial;
	memset(explorado,0,sizeof(explorado));
	while(1){
		if(H->i==iFinal && H->j==jFinal){
			encontrou =1;
			break;
		}
		
		explorado[setExplorado(H->i,H->j,tamColuna)]=1;
		
		memset(posicao,0,sizeof(posicao));
		numSucessores=sucessores(M,H->i,H->j,tamColuna);
		
		for(i=0;i<numSucessores;i++){
			if(posicao[0]==0){
				break;
			}
			auxH=malloc(sizeof(folha));
			auxH->i=posicao[(i*2)];
			auxH->j=posicao[(i*2)+1];
			auxH->custo=H->custo+1;
			auxH->pai=H;
			L=insereFila(L,auxH);
		}
		if(L->next ==NULL){
			printf("RESULTADO NAO ENCONTRADO");
			break;
		}
		L=retiraFila(L);

		H=L->estado;
	}
	
	printf("\n");
	
	printf("ENTRADA \n");
	for(i=0;i<tamLinhas;i++){
		for(j=0;j<tamColuna;j++){
			printf("%c",M[i][j]);
		}
		printf("\n");
	}
	printf("\n");

	while(H!=NULL){
		M[H->i][H->j]='0';
		H=H->pai;
	}
	M[iInicial][jInicial] ='I';
	M[iFinal][jFinal] ='F';

	printf("SAIDA\n");
	for(i=0;i<tamLinhas;i++){
		for(j=0;j<tamColuna;j++){
			printf("%c",M[i][j]);
		}
		printf("\n");	
	}
	
	free(L);
	free(H);




}