	ORG $4000
	ABA
	ABA 15
	ADCA #20
	ADCA #-20
	ADCA 20
	ADCA @20
	ADCB $1000
ET1:	ADDA #123
	ASL #20
	ASL @20
	BCC ET1
	BGND	
FIN:	END