   ORG $4000
   LDAA #20
E1:	ORG $4010
   LDAA @20
   LDAA 16,SP
   LDAA -16,PC
   BNE E1
   JMP E1
   LBNE E1
   IBNE A,E1
E2:	START
   BSZ 10
   DC.W 1,30
E3:	LDAA -10,S<P
   LDAA [16,SP]
   LDAA [256,SP]
   LDAA [-16,SP]
E4:	END