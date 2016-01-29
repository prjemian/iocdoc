/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/devOpc.c

Project:        Device support for OPC

Description:    Implementation of dset for this records:
                   ai, bi, mbbi, mbbiDirect, longin, stringin
                   ao, bo, mbbo, mbboDirect, longout, stringout
                  
                epics related stuff is implemented here in C-language:  
                  dset's, record
                related data conversion (mask, shift).
                All opc access and conversion of data type is done in 
                drv.cpp.

Author:         Bernhard Kuner

Version:        $Revision: 1.11 $

History:

  $Log: devOpc.c,v $
  Revision 1.11  2003/12/11 12:49:04  kuner
  Array Access added, outsource console functions to opcConsoleCmd.cpp

  Revision 1.10  2003/07/16 17:12:09  kuner
  *** empty log message ***

  Revision 1.9  2003/07/16 17:09:52  kuner
  Adapted to base3.14.2, new io report function: opcIor, use iocLogClient for error logging

  Revision 1.7  2003/03/18 12:08:00  kuner
  add cvs id variables and print it by showVersion()

  Revision 1.6  2003/03/11 12:42:55  winkler
  printInfo: changed output to log-file

  Revision 1.5  2003/03/04 18:44:39  kuner
  New translation of opc item names with more than 29 char to short names with opcClr2db.pl and support of read this names from file drvopc.cpp: opcSetNames

  Revision 1.4  2003/03/03 14:04:14  kuner
  init_record: if opcCreateItem fails: report error, set prec->pact=TRUE to disable record

  Revision 1.3  2003/03/03 11:13:12  winkler
  *** empty log message ***


Copyright:
  This software is copyrighted by the BERLINER SPEICHERRING
  GESELLSCHAFT FUER SYNCHROTRONSTRAHLUNG M.B.H., BERLIN, GERMANY.
  The following terms apply to all files associated with the software.

  BESSY hereby grants permission to use, copy and modify this
  software and its documentation for non-commercial, educational or
  research purposes provided that existing copyright notices are
  retained in all copies.

  The receiver of the software provides BESSY with all enhancements,
  including complete translations, made by the receiver.

  IN NO EVENT SHALL BESSY BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
  SPECIAL, INCIDENTIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE
  OF THIS SOFTWARE, ITS DOCUMENTATION OR ANY DERIVATIVES THEREOF, EVEN
  IF BESSY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

  BESSY SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED
  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
  PURPOSE, AND NON-INFRINGEMENT. THIS SOFTWARE IS PROVIDED ON AN "AS IS"
  BASIS, AND BESSY HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT,
  UPDATES, ENHANCEMENTS OF MODIFICTAIONS.
*/
char * devOpcId =
"devOpc.c: $Revision: 1.11 $\n";
#include <string.h>
#include <stdio.h>
#include <malloc.h>

#include <winsock2.h> //need definition of: FILETIME

#include "alarm.h"
#include "cvtTable.h"
#include "dbDefs.h"
#include "dbAccess.h"
#include "dbCommon.h"
#include "dbScan.h"
#include "recGbl.h"
#include "recSup.h"
#include "devSup.h"
#include "link.h"
#include "menuConvert.h"
#include "epicsExport.h"


#include "aiRecord.h"
#include "aaiRecord.h"
#include "aoRecord.h"
#include "aaoRecord.h"
#include "biRecord.h"
#include "boRecord.h"
#include "longinRecord.h"
#include "longoutRecord.h"
#include "stringinRecord.h"
#include "stringoutRecord.h"
#include "mbbiRecord.h"
#include "mbboRecord.h"
#include "mbbiDirectRecord.h"
#include "mbboDirectRecord.h"

#include "menuAlarmStat.h"
#include "menuAlarmSevr.h"
#include "devOpc.h"
#include "drvOpc.h"
#include "errlog.h"
#include "menuFtype.h"

static long init(int after);
static long get_ioint_info(int cmd, struct dbCommon *prec, IOSCANPVT *ppvt);
static long read(dbCommon *prec);
static long write(dbCommon *prec);
static void outRecordCallback(CALLBACK *pcallback);
int iIocInitReady = 0;

/* special record type dependant initialisation */
long initRecordDependants(OpcToEpics *pO2E);

/* record properties: 
        r/valType Type of value field for arrays it may be changed to desired type
	cnt       Nr of elements = 1 for record with scalar val field, 
	          arrays=0, means nr of elements is specified in nelm field
		  strings= string length
	convert   2 means record process routine should not try to convert
	RecType   recordname + field to put the value to: val or rval
*/
  RecPropStruct recProp[] = {
/*        r/valType       cnt convert RecType*/
/*	{ aitEnumInvalid   ,0  ,0,    "aaival"           },*/
/*	{ aitEnumInvalid   ,0  ,0,    "aaoval"           },*/
	{ aitEnumFloat64   ,0  ,0,    "aaival"           },
	{ aitEnumFloat64   ,0  ,0,    "aaoval"           },
	{ aitEnumFloat64   ,1  ,2,    "aival"            },
	{ aitEnumFloat64   ,1  ,0,    "aoval"            },
	{ aitEnumUint16    ,1  ,2,    "bival"            },
	{ aitEnumUint16    ,1  ,2,    "boval"            },
	{ aitEnumUint16    ,1  ,0,    "eventval"         },
	{ aitEnumInvalid   ,1  ,0,    "histogramval"     },
	{ aitEnumInt32     ,1  ,2,    "longinval"        },
	{ aitEnumInt32     ,1  ,0,    "longoutval"       },
	{ aitEnumUint16    ,1  ,2,    "mbbival"          },
	{ aitEnumUint16    ,1  ,0,    "mbboval"          },
	{ aitEnumUint16    ,1  ,2,    "mbbiDirectval"    },
	{ aitEnumUint16    ,1  ,0,    "mbboDirectval"    },
	{ aitEnumString    ,40 ,0,    "stringinval"      },
	{ aitEnumString    ,40 ,0,    "stringoutval"     },
	{ aitEnumInvalid   ,0  ,0,    "waveformval"      },
	{ aitEnumInt32     ,1  ,0,    "airval"           },
	{ aitEnumInt32     ,1  ,0,    "aorval"           },
	{ aitEnumUint32	   ,1  ,0,    "birval"           },
	{ aitEnumUint32    ,1  ,0,    "borval"           },
	{ aitEnumUint32    ,1  ,0,    "mbbiDirectrval"   },
	{ aitEnumUint32    ,1  ,0,    "mbboDirectrval"   },
	{ aitEnumUint32    ,1  ,0,    "mbbirval"         },
	{ aitEnumUint32    ,1  ,0,    "mbborval"         },
  };


/* Define and create the dset for input record typ */
#define IN_RECORD_OPC_DSET(recName, raw) static long init_##recName##raw##Record(dbCommon *prec);	\
struct { \
	long		number; \
	DEVSUPFUN	report; \
	DEVSUPFUN	init; \
	DEVSUPFUN	init_Record; \
	DEVSUPFUN	get_ioint_info; \
	DEVSUPFUN	read; \
	DEVSUPFUN	special_linconv; \
}dev##recName##raw##Opc={ \
	6, \
	NULL, \
	init, \
	init_##recName##raw##Record, \
	get_ioint_info, \
	read , \
	NULL \
};  \
epicsExportAddress(dset,dev##recName##raw##Opc);\
			\
static long init_##recName##raw##Record(dbCommon *prec) 	\
{															\
  char *opcItemName;								\
  OpcToEpics *pOpcToEpics;							\
													\
  if( ((##recName##Record *)prec)->inp.type != INST_IO) \
  { recGblRecordError(S_db_badField, (void *)prec,	\
         "devAiOpc (init_record) Illegal INP field"); \
    return(S_db_badField);						\
  }												\
  if( ((##recName##Record *)prec)->scan <  SCAN_IO_EVENT  )	\
  { recGblRecordError(S_db_badField, (void *)prec,	\
      "devAiOpc (init_record) Illegal SCAN field");	\
    return(S_db_badField);							\
  }													\
  pOpcToEpics =  (OpcToEpics *) calloc(1,sizeof(OpcToEpics));	\
  pOpcToEpics->pRecVal=&( ((##recName##Record *)prec)->##raw## );	 /*will be set to bptr in initRecordDependants for aa..Records */\
  pOpcToEpics->recType=##recName##raw;			\
  prec->dpvt = (void *) pOpcToEpics;			\
  pOpcToEpics->pRecord = prec;					\
  opcItemName = ((##recName##Record *)prec)->inp.value.instio.string;\
  if( opcCreateItem( (OpcToEpics*)(prec->dpvt), opcItemName, prec) )	\
  { recGblRecordError(S_db_badField, (void *)prec, \
         "devAiOpc (init_record) failed to create opc item"); \
    prec->pact = TRUE;	/* disable this record */ \
    return(S_db_notFound);						\
  }												\
  if( ((##recName##Record *)prec)->scan ==  SCAN_IO_EVENT )	\
  { scanIoInit(&(pOpcToEpics->ioscanpvt) );		\
    pOpcToEpics->isCallback = 1;	\
  }									\
  else								\
  { pOpcToEpics->isCallback = 0;	\
    pOpcToEpics->ioscanpvt=NULL;	\
  }									\
  initRecordDependants(pOpcToEpics); \
  return(0);						\
}

#define OUT_RECORD_OPC_DSET(recName, raw) static long init_##recName##raw##Record(dbCommon *prec);	\
struct { 				\
	long		number; \
	DEVSUPFUN	report; \
	DEVSUPFUN	init; 	\
	DEVSUPFUN	init_Record; 	\
	DEVSUPFUN	get_ioint_info; \
	DEVSUPFUN	write; 	\
	DEVSUPFUN	special_linconv;\
}dev##recName##raw##Opc={ 	\
	6,		\
	NULL,	\
	init,	\
	init_##recName##raw##Record, \
	get_ioint_info, \
	write,	\
	NULL	\
};			\
epicsExportAddress(dset,dev##recName##raw##Opc);\
			\
static long init_##recName##raw##Record(dbCommon *prec) 	\
{ char *opcItemName;								\
  OpcToEpics *pOpcToEpics;							\
													\
  if( ((##recName##Record *)prec)->out.type != INST_IO) \
  { recGblRecordError(S_db_badField, (void *)prec,	\
         "devAiOpc (init_record) Illegal INP field only INST_IO possible"); \
    return(S_db_badField);						\
  }												\
  pOpcToEpics =  (OpcToEpics *) calloc(1,sizeof(OpcToEpics));			\
  pOpcToEpics->pRecVal=&(((##recName##Record *)prec)->##raw##);	 /*will be set to bptr in initRecordDependants for aa..Records */\
  pOpcToEpics->recType=##recName##raw;									\
  pOpcToEpics->isCallback = 1;						\
  pOpcToEpics->isOutRecord = 1;						\
  prec->dpvt = (void *) pOpcToEpics;				\
  opcItemName = ((##recName##Record *)prec)->out.value.instio.string;\
  pOpcToEpics->pRecord = prec;						\
  if( opcCreateItem( (OpcToEpics*)(prec->dpvt), opcItemName, prec) )	\
  { recGblRecordError(S_db_badField, (void *)prec,	\
         "devAiOpc (init_record) failed to create opc item"); \
    prec->pact = TRUE;	/* disable this record */ \
    return(S_db_notFound);						\
  }												\
  callbackSetCallback(outRecordCallback, &(pOpcToEpics->callback) );	\
  callbackSetUser(prec, &(pOpcToEpics->callback) );	\
  initRecordDependants(pOpcToEpics); \
  return(0);										\
}

IN_RECORD_OPC_DSET(ai,val);
IN_RECORD_OPC_DSET(aai,val);
IN_RECORD_OPC_DSET(bi,val);
IN_RECORD_OPC_DSET(bi,rval);
IN_RECORD_OPC_DSET(longin,val);
IN_RECORD_OPC_DSET(mbbi,val);
IN_RECORD_OPC_DSET(mbbi,rval);
IN_RECORD_OPC_DSET(mbbiDirect,val);
IN_RECORD_OPC_DSET(mbbiDirect,rval);
IN_RECORD_OPC_DSET(stringin,val);

OUT_RECORD_OPC_DSET(ao,val);
OUT_RECORD_OPC_DSET(aao,val);
OUT_RECORD_OPC_DSET(longout,val);
OUT_RECORD_OPC_DSET(bo,val);
OUT_RECORD_OPC_DSET(mbbo,val);
OUT_RECORD_OPC_DSET(mbbo,rval);
OUT_RECORD_OPC_DSET(mbboDirect,val);
OUT_RECORD_OPC_DSET(mbboDirect,rval);
OUT_RECORD_OPC_DSET(stringout,val);

/* callback service routine */
static void outRecordCallback(CALLBACK *pcallback)
{ dbCommon *prec;
  
  callbackGetUser(prec, pcallback);
  dbProcess(prec);
}

/* implementation of dset common functions*/
static long init(int after)
{ 
  if(after)
  {	
		 iIocInitReady = 1;        
		 return 0;
  }
  return 1;
}

long initRecordDependants(OpcToEpics *pO2E)
{ dbCommon* prec = pO2E->pRecord;
/* used for mbb... records*/ 
  unsigned long   shft;   /* Shift, TODO: check type for epics release > 3.14*/

  switch(pO2E->recType)
  { case mbbirval:
          if( ((mbbiRecord*)prec)->shft>0) 
            ((mbbiRecord*)prec)->mask <<= ((mbbiRecord*)prec)->shft;
          pO2E->mask = ((mbbiRecord*)prec)->mask;
          break;
    case mbbiDirectrval:
          if( ((mbbiDirectRecord*)prec)->shft>0) 
            ((mbbiDirectRecord*)prec)->mask <<= ((mbbiDirectRecord*)prec)->shft;
          pO2E->mask = ((mbbiDirectRecord*)prec)->mask;
          break;
   
    case mbborval:
          shft = ((mbboRecord*)prec)->shft;
          if( shft>0) 
            ((mbboRecord*)prec)->mask <<= shft;
          pO2E->mask = ((mbboRecord*)prec)->mask;
          pO2E->shft = shft;
          break;
    case mbboDirectrval:
          shft = ((mbboDirectRecord*)prec)->shft;
          if( shft>0) 
            ((mbboDirectRecord*)prec)->mask <<= shft;
          pO2E->mask = ((mbboDirectRecord*)prec)->mask;
          pO2E->shft = shft;
          break;
	case aaival:
          ((aaiRecord *)prec)->bptr = (aitFloat64*) malloc(sizeof(aitFloat64) * ((aaiRecord *)prec)->nelm);
          if( ! ((aaiRecord *)prec)->bptr )
          { recGblRecordError(S_db_badField, (void *)prec,
              "devAiOpc (init_record) failed to malloc buffer");
            prec->pact = TRUE;	/* disable this record */
            return(S_db_noMemory);
          }
          ((aaiRecord *)prec)->ftvl = menuFtypeDOUBLE; /* Attention: set RecTypeEnum recProp */
          pO2E->nelm = ((aaiRecord *)prec)->nelm;
          pO2E->nord = &( ((aaiRecord *)prec)->nord);
          pO2E->pRecVal= ((aaiRecord *)prec)->bptr; /* set to buffer*/
          break;
    case aaoval:
          
          break;
}
  return 0;
}

static long read(dbCommon *prec)
{ OpcToEpics* pO2E = (OpcToEpics*)prec->dpvt;
  long retOk = recProp[ pO2E->recType ].ret;
  if( opcGetScalar( pO2E ) )
  { 
//  prec->pact = TRUE;	/* prevent error storms */
	return retOk;
  }
  if (pO2E->mask)       /* true for raw-mbbi, -mbbiDirect */
    *( (aitUint32*)(pO2E->pRecVal)) &= pO2E->mask;
  prec->pact = FALSE;
  prec->udf = FALSE;
  return retOk;
}

static long write(dbCommon *prec)
{ OpcToEpics* pO2E = (OpcToEpics*)prec->dpvt;
  
  if (pO2E->mask)       /* true for raw-mbbo, -mbboDirect */
  { *( (aitUint32*)(pO2E->pRecVal)) <<= pO2E->shft;
    *( (aitUint32*)(pO2E->pRecVal)) &= pO2E->mask;
  }  

  if( opcSetScalar( ((OpcToEpics*)(prec->dpvt)) ) )
  { 
//	prec->pact = TRUE;	/* prevent error storms */
	return 1;
  }
  prec->pact = FALSE;
  prec->udf = FALSE;
  return 0;
}

static long get_ioint_info(int cmd, struct dbCommon *prec, IOSCANPVT *ppvt)
{ if( !cmd )
  { *ppvt = ((OpcToEpics*)(prec->dpvt))->ioscanpvt;
  }
  else
  { ((OpcToEpics*)(prec->dpvt))->isCallback = 0;
  }
  return 0;
}
