#ifndef __ERR_OUT_H

#define	DBG_VERSION					0x00000001		//	Show version of opc device driver
#define	DBG_READ					0x00000002		//	Read values
#define	DBG_WRITE					0x00000004		//	Write values
#define	DBG_BAD						0x00000008		//	Bad values
#define	DBG_OPC_INIT				0x00000010		//	Show OPC init
#define	DBG_OPC_VARS				0x00000020		//	Show all OPC variables
#define	DBG_OPC_MAP					0x00000040		//	Show OPC-EPICS-MAPPING
#define	DBG_TEMPLATE				0x00000080		//	Show template processing
#define	DBG_OPC_REFRESH				0x00000100		//	Show OPC-group refreshing
#define	DBG_UNDEF1					0x00000200		//	undefined
#define	DBG_UNDEF2					0x00000400		//	undefined
#define	DBG_UNDEF3					0x00000800		//	undefined
#define	DBG_UNDEF4					0x00001000		//	undefined
#define	DBG_AI_AIR					0x00002000		//	Show only ai(r) variables
#define	DBG_AAI						0x00004000		//	Show only aai variables
#define	DBG_BI_BIR					0x00008000		//	Show only bi(r) variables
#define	DBG_LONGIN					0x00010000		//	Show only longin variables
#define	DBG_MBBI_MBBIR				0x00020000		//	Show only mbbi(r) variables
#define	DBG_MBBIDIRECT_MBBIDIRECTR	0x00040000		//	Show only mbbiDirect(r) variables
#define	DBG_STRINGIN				0x00080000		//	Show only stringin variables
#define	DBG_EVENTVAL				0x00100000		//	Show only eventval variables
#define	DBG_HISTOGRAMVAL			0x00200000		//	Show only histogramval variables
#define	DBG_AO_AOR					0x00300000		//	Show only ao(r) variables
#define	DBG_AAO						0x00800000		//	Show only aao variables
#define	DBG_BO_BOR					0x01000000		//	Show only bo(r) variables
#define	DBG_LONGOUT					0x02000000		//	Show only longout variables
#define	DBG_MBBO_MBBOR				0x04000000		//	Show only mbbo(r) variables
#define	DBG_MBBODIRECT_MBBIDORECTR	0x08000000		//	Show only mbboDirect(r) variables
#define	DBG_STRINGOUT				0x10000000		//	Show only stringout variables
#define	DBG_WAVEFORMAL				0x20000000		//	Show only waveformval variables
#define	DBG_COLORED					0x40000000		//	Colored output
#define	DBG_UNDEF5					0x80000000		//	undefined

#define __ERR_OUT_H



int CheckType(int iActualType);
void dbgPrintf(int iLevel, int iActualType=0);

#endif
