/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/drvOpc.cpp

Project:        Device support for OPC

Description:    All opc access and conversion of data type is done here.
                Epics related stuff is implemented in devOpc.c

Author:         Bernhard Kuner

Version:        $Revision: 1.18 $

History:

  $Log: drvOpc.cpp,v $
  Revision 1.18  2003/12/11 12:49:04  kuner
  Array Access added, outsource console functions to opcConsoleCmd.cpp

  Revision 1.17  2003/09/23 05:48:11  winkler
  *** empty log message ***

  Revision 1.16  2003/07/16 17:12:09  kuner
  *** empty log message ***

  Revision 1.15  2003/07/16 17:09:53  kuner
  Adapted to base3.14.2, new io report function: opcIor, use iocLogClient for error logging

  Revision 1.13  2003/03/18 12:08:00  kuner
  add cvs id variables and print it by showVersion()

  Revision 1.12  2003/03/14 15:57:57  kuner
  Bugfix: set epics timestamp to opc timestamp only for READ values, do nothing in
    case of WRITE values

  Revision 1.11  2003/03/12 15:03:51  kuner
  Disconnect opc-server when ctrl-c
  drvOpc.cpp opcPrintItemList Line 314: continue if there is no object

  Revision 1.10  2003/03/11 12:49:27  winkler
  opcSetNames: excepts comments and skips leading blanks and/or tabs

  Revision 1.9  2003/03/10 07:03:11  winkler
  setSecondaryAttributes new ELSE-branch
  onSetReadQuality(void) new function

  Revision 1.8  2003/03/06 11:59:21  winkler
  *** empty log message ***

  Revision 1.7  2003/03/06 11:50:48  winkler
  m_pServer->disconnect() into ~OpcRegisterToIocShell()

  Revision 1.6  2003/03/05 08:11:08  winkler
  opcGetScalar: check quality before read value

  Revision 1.5  2003/03/04 18:44:39  kuner
  New translation of opc item names with more than 29 char to short names with 
  opcClr2db.pl and support of read this names from file drvopc.cpp: opcSetNames

  Revision 1.4  2003/03/03 14:14:39  kuner
    opcSetServer: before exit function: psvrbrw.release(); (winkler)
    opcSetServer: put variables outside loop: srcDesc, srvId, srv (kuner)
    opcCreateItem: check opcCreateGroupFlag and don't create without group (winkler)

  Revision 1.3  2003/03/03 11:13:54  winkler
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
char * drvOpcId =
"drvOpc: $Revision: 1.18 $\n";

#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <string.h> 	// need strncpy

#include <winsock2.h>	//need definition of: FILETIME
#include <signal.h>	// disconnect opc-Server when CTRL-C

#include <sodac.h>
#include <SOCmnTrace.h>

#include "dbCommon.h"
#include "dbAccessDefs.h"
#include "dbStaticLib.h"
#include <epicsTime.h>
#include <aitTypes.h>
#include <aitConvert.h>
#include <menuAlarmSevr.h>
#include <menuAlarmStat.h>
#include "iocsh.h"

#include "devOpc.h"
#include "drvOpc.h"
#include "opcConsoleCmd.h"

#include "stdafx.h"
#include "Item.h"
#include "opc.h"

#include "errDbg.h"
extern int dbg_level;
extern char szDbgMessage[256];

enum VARENUM ait2vtTable[AIT_MAX]={	/* to convert numeric ait types to variant types */
		 VT_EMPTY,  /*0 = aitEnumInvalid */
		 VT_I1,     /*1 = aitEnumInt8 */
		 VT_UI1,    /*2 = aitEnumUint8 */
		 VT_I2,     /*3 = aitEnumInt16 */
		 VT_UI2,    /*4 = aitEnumUint16 */
		 VT_UI2,    /*5 = aitEnumEnum16 */
		 VT_I4,     /*6 = aitEnumInt32 */
		 VT_UI4,    /*7 = aitEnumUint32 */
		 VT_R4,	    /*8 = aitEnumFloat32 */
		 VT_R8,     /*9 = aitEnumFloat64 */
		 VT_EMPTY,  /*10= aitEnumFixedString */
		 VT_EMPTY,  /*11= aitEnumString */
		 VT_EMPTY   /*12= aitEnumContainer */
	};
/* convert numeric variant types to ait types*/
aitEnum vt2aitTable[32]={		/* variant definition see: .../VC98/Include/OAIDL.H*/
        aitEnumInvalid, 	/* VT_EMPTY	= 0 */
	    aitEnumInvalid,	/* VT_NULL	= 1 */
	    aitEnumInt16,	/* VT_I2	= 2 */
	    aitEnumInt32,	/* VT_I4	= 3 */
	    aitEnumFloat32,	/* VT_R4	= 4 */
	    aitEnumFloat64,	/* VT_R8	= 5 */
	    aitEnumInvalid,	/* VT_CY	= 6 */
	    aitEnumInvalid,	/* VT_DATE	= 7 */
	    aitEnumInvalid,	/* VT_BSTR	= 8 */
	    aitEnumInvalid,	/* VT_DISPATCH	= 9 */
	    aitEnumInvalid,	/* VT_ERROR	= 10 */
	    aitEnumInt16,	/* VT_BOOL	= 11 VT_BOOL = VARIANT_BOOL = SHORT - see WTYPES.H*/
	    aitEnumInvalid,	/* VT_VARIANT	= 12 */
	    aitEnumInvalid,	/* VT_UNKNOWN	= 13 */
	    aitEnumInvalid,	/* VT_DECIMAL	= 14 */
	    aitEnumInvalid,	/* not used	= 15 */
	    aitEnumInt8 ,	/* VT_I1	= 16 */
	    aitEnumUint8,	/* VT_UI1	= 17 */
	    aitEnumUint16,	/* VT_UI2	= 18 */
	    aitEnumUint32,	/* VT_UI4	= 19 */
	    aitEnumInvalid,	/* VT_I8	= 20 */
	    aitEnumInvalid,	/* VT_UI8	= 21 */
	    aitEnumInt32,	/* VT_INT	= 22 */
	    aitEnumInvalid,	/* VT_UINT	= 23 */
	    aitEnumInvalid,	/* VT_VOID	= 24 */
	    aitEnumInvalid,	/* VT_HRESULT	= 25 */
	    aitEnumInvalid,	/* VT_PTR	= 26 */
	    aitEnumInvalid,	/* VT_SAFEARRAY	= 27 */
	    aitEnumInvalid,	/* VT_CARRAY	= 28 */
	    aitEnumInvalid,	/* VT_USERDEFINED	= 29 */
	    aitEnumString,	/* VT_LPSTR	= 30 */
	    aitEnumInvalid	/* VT_LPWSTR	= 31 */
  };
std::ostream &operator<<(std::ostream &s, const SYSTEMTIME *t)
{ 
	return s << t->wYear<<"/"<<t->wMonth<<"/"<<t->wDay<<" "<<t->wHour<<":"<<t->wMinute<<":"<<(double)(t->wSecond+((double)t->wMilliseconds/1000));
}
std::ostream &operator<<(std::ostream &s, const epicsTimeStamp *et)
{ 
	char nowText[40];
	size_t rtn;
	nowText[0] = 0;
	rtn = epicsTimeToStrftime(nowText,sizeof(nowText),"%Y/%m/%d %H:%M:%S.%06f",et);
	if( rtn )
		return s <<nowText;
	else
		return s <<" *** can't convert epicsTimeStamp *** ";
}

SOCmnString strDbg;
COpc myOpc;
extern "C" int iIocInitReady;

// called to start initialized OPC session
// assures OPC session is running
long opcInit( void)
{
	long lResult = 0;
	myOpc.ReadCmd(__argv[1]);
	int iWatchDog = 0;
	do
	{
		lResult = myOpc.Start();
		if(!lResult)
			Sleep(5000);
	}
	while(!lResult && ++iWatchDog < 30);

	return lResult;
}

long opcStartServer( void )
{
	return 0;
}

// connect PVs to OPC items
long opcCreateItem( OpcToEpics *opcTepics, char *opcName, dbCommon *prec)
{
	static unsigned long lCounter=0;
	if(opcTepics && myOpc.Start())
	{
		myOpc.m_PointerMapPos = myOpc.m_PointerMap.find(prec->name);
		if(myOpc.m_PointerMapPos != myOpc.m_PointerMap.end())
		{
			IorItem *ior;
			ior = new IorItem(prec->name, opcName);		// opcIor informations
			ior->opcFullName = (LPCTSTR)(*myOpc.m_PointerMapPos).second->m_soItemID;
			iorItems.push_back(ior);

			CItem *pOpcItem = (*myOpc.m_PointerMapPos).second;
			pOpcItem->setRec(opcTepics);
			printf("%5lu OPC variables connected to IOC\x0D",++lCounter);
			//printf("Counter = %6lu%25s%25s%25s\n",++lCounter, opcName, prec->name, ((CItem*)opcTepics->pOpcItem)->m_sPvName.c_str());
			//Sleep(1);
			return 0;
		}
	}
	if(opcName[0])
		errlogPrintf("opcCreateItem: Warning! Invalid address (%s)\n",opcName);
	return 1;
}

// read and set time stamp and stat/sevr according to signal quality.
long setSecondaryAttributes(CItem *oi, dbCommon *prec, unsigned short stat)
{
	if(oi && prec)
	{
		if( oi->isBad() )
		{
			prec->nsta = stat;
			prec->nsev = menuAlarmSevrINVALID;
			// prec->pact = TRUE;
			if(DBG_BAD & dbg_level)
			{
				sprintf(szDbgMessage,"%s: Bad Quality",prec->name);
				dbgPrintf(DBG_BAD, ((OpcToEpics*)(prec->dpvt))->recType);
				szDbgMessage[0] = NULL;
			}
			return 1;
		}
		else
		{
			prec->nsta = menuAlarmStatNO_ALARM;
			prec->nsev = menuAlarmSevrNO_ALARM;
		}
		prec->pact = FALSE;
		return 0;
	}
	errlogPrintf("setSecondaryAttributes: Warning! Invalid address ");
	if(oi)
		errlogPrintf("(%s)\n",oi->m_sPvName.c_str());
	else if(prec)
		errlogPrintf("(%s)\n",prec->name);
	else
		errlogPrintf("(unknown PV)\n");
	return 1;
}

long opcGetArray(OpcToEpics * pOpc2epics)
{
	if(pOpc2epics && pOpc2epics->pRecord && pOpc2epics->pOpcItem)
	{
		dbCommon *prec = pOpc2epics->pRecord;
		CItem *oi = (CItem*) pOpc2epics->pOpcItem;
		RecPropStruct *pRecProp = &(recProp[ pOpc2epics->recType ]);
		aitEnum aitRec = pRecProp->valAitType;
		aitEnum aitVar = vt2aitTable[(oi->m_readValue.vt & ~VT_ARRAY)];
		HRESULT hr;
		LONG lBound, uBound, nrOfElem;
		void *pData=(void*) oi->m_readValue.parray->pvData;
		if(DBG_READ & dbg_level)
		{
			sprintf(szDbgMessage,"opcGetArray: %s: aitRec=%d, aitVar=%d, vt=0x%X",
				pOpc2epics->pRecord->name,aitRec,aitVar,(oi->m_readValue.vt & ~VT_ARRAY) );
			dbgPrintf(DBG_READ, pOpc2epics->recType);
			szDbgMessage[0] = NULL;
		}
		if (hr = SafeArrayLock(oi->m_readValue.parray) )
			return hr;
		hr = SafeArrayGetLBound(oi->m_readValue.parray, 1, &lBound);
		hr = SafeArrayGetUBound(oi->m_readValue.parray, 1, &uBound);
		if( hr )
			return hr;
		nrOfElem = uBound - lBound + 1;
		if( nrOfElem > pOpc2epics->nelm)   // just read what can be buffered from the record
			nrOfElem = pOpc2epics->nelm;
		*(pOpc2epics->nord) = nrOfElem;
		if(DBG_READ & dbg_level)
		{
			sprintf(szDbgMessage,"\tconvert %d elems, d[%d]..[%d]aitVar\n",nrOfElem,lBound,uBound);
			dbgPrintf(DBG_READ, pOpc2epics->recType);
			szDbgMessage[0] = NULL;
		}
		if((oi->m_readValue.vt & ~VT_ARRAY) < 32)	//the numeric values, see vt2aitTable
		{
			if( ! aitConvert(aitRec, pOpc2epics->pRecVal, aitVar, pData, nrOfElem) )
			{
				errlogPrintf("opcGetArray: %s: aitRec=%d, aitVar=%d, vt=0x%X \tconvert %d elems, d[%d]..[%d]aitVar failed!\n",
						pOpc2epics->pRecord->name,
						aitRec,aitVar,
						(oi->m_readValue.vt & ~VT_ARRAY),
						nrOfElem,
						lBound,
						uBound
						);
				hr=1;
			}
		}
		SafeArrayUnlock(oi->m_readValue.parray);
		return hr;
	}
	errlogPrintf("opcGetArray: Warning! Invalid adress ");
	if(pOpc2epics && pOpc2epics->pRecord)
		errlogPrintf("(%s)\n",pOpc2epics->pRecord->name);
	else if(pOpc2epics && pOpc2epics->pOpcItem)
		errlogPrintf("(%s)\n",((CItem*)pOpc2epics->pOpcItem)->m_sPvName.c_str());
	else
		errlogPrintf("(unknown PV)\n");
	return 1;
}

long opcGetScalar(OpcToEpics * pOpc2epics)
{
	if(pOpc2epics && pOpc2epics->pRecord && pOpc2epics->pOpcItem)
	{
		dbCommon *prec = pOpc2epics->pRecord;
		CItem *oi = (CItem*) pOpc2epics->pOpcItem;
		if(!oi)
			return 1;
		RecPropStruct *pRecProp = &(recProp[ pOpc2epics->recType ]);
		aitEnum aitRec = pRecProp->valAitType;
		aitEnum aitVar = vt2aitTable[(oi->m_readValue.vt & ~VT_ARRAY)];
		if(DBG_READ & dbg_level)
		{
			sprintf(szDbgMessage,"%s (%s) GetScalar aiT=%d vt=%d val=%s",pOpc2epics->pRecord->name,pRecProp->record,aitRec,oi->m_readValue.vt,oi->m_readValue.toString(&strDbg));
			dbgPrintf(DBG_READ, pOpc2epics->recType);
			szDbgMessage[0] = NULL;
		}
		if( setSecondaryAttributes(oi, prec, menuAlarmStatREAD) ) 
			return 1;
		FILETIME ft;					// keep epics time stamp if opc is BAD
		oi->getReadTimeStamp(&ft);

	//  SYSTEMTIME st;
	//  FileTimeToSystemTime( &ft,&st);
	//  printf("READ: %s\t%2i:%02i:%02i.%03i\n",prec->name,st.wHour+1,st.wMinute,st.wSecond,st.wMilliseconds);

		if(prec->tse == epicsTimeEventDeviceTime )
			ft2epics(&ft, &(prec->time));
		if((oi->m_readValue.vt & VT_ARRAY))
			return opcGetArray(pOpc2epics);
		if( oi->m_readValue.vt < 32)		//the numeric values, see vt2aitTable
		{
			if( aitVar )
			{
				void *pVariantData = &(oi->m_readValue.bVal);
				if( aitConvert(aitRec, pOpc2epics->pRecVal, aitVar, pVariantData,1) )
				{
					if(DBG_READ & dbg_level)
					{
						sprintf(szDbgMessage,"\taitRec=%d VAL=%d, aitVar=%d uiVal=%d\n",aitRec, *(aitUint16*)(pOpc2epics->pRecVal),aitVar,*(aitUint16*)pVariantData);
						dbgPrintf(DBG_READ, pOpc2epics->recType);
						szDbgMessage[0] = NULL;
					}
					return 0;
				}  
			}
		}  
		prec->pact = FALSE;
		switch( oi->m_readValue.vt)
		{ 
			case VT_BSTR:
			case VT_LPSTR:
			case VT_LPWSTR:
			{
				LPCTSTR  pStr=oi->m_readValue.toString(&strDbg);
				int cnt = pRecProp->cnt;
				if( strncpy((char*)(pOpc2epics->pRecVal), pStr,cnt) )
				{
					((char*)(pOpc2epics->pRecVal))[cnt-1]='\0';
					if(DBG_READ & dbg_level)
					{
						sprintf(szDbgMessage,"\tcnt=%d str= \"%s\",  VAL= \"%s\"",cnt,pStr,(aitString*)(pOpc2epics->pRecVal));
						dbgPrintf(DBG_READ, pOpc2epics->recType);
						szDbgMessage[0] = NULL;
					}
					return 0;
				}  
				break;
			}    
			default :
			{
				errlogPrintf("opcGetScalar: Invalid opc-type: \n",prec->name,aitVar);
				prec->nsta = menuAlarmStatREAD;	
				prec->nsev = menuAlarmSevrINVALID;
				prec->pact = TRUE;
			}
		}
	}
	errlogPrintf("opcGetScalar: Warning! Invalid adress ");
	if(pOpc2epics && pOpc2epics->pRecord)
		errlogPrintf("(%s)\n",pOpc2epics->pRecord->name);
	else if(pOpc2epics && pOpc2epics->pOpcItem)
		errlogPrintf("(%s)\n",((CItem*)pOpc2epics->pOpcItem)->m_sPvName.c_str());
	else
		errlogPrintf("(unknown PV)\n");
	return 1;  /* the error case */
}

long opcSetScalar(OpcToEpics * pOpc2epics)
{
	if(pOpc2epics && pOpc2epics->pRecord && pOpc2epics->pOpcItem)
	{
		dbCommon *prec = pOpc2epics->pRecord;
		CItem *oi = (CItem*) pOpc2epics->pOpcItem;
		RecPropStruct *pRecProp = &(recProp[ pOpc2epics->recType ]);
		aitEnum aitRec = pRecProp->valAitType;
		SOCmnVariant v;
		prec->pact = FALSE;
		if(DBG_WRITE & dbg_level)
		{
			sprintf(szDbgMessage,"%s SetScalar %d", prec->name,*(int*)(pOpc2epics->pRecVal) );
			dbgPrintf(DBG_WRITE, pOpc2epics->recType);
			szDbgMessage[0] = NULL;
		}
		if( pOpc2epics->noOut )
		{
			pOpc2epics->noOut=0;
			if(DBG_WRITE & dbg_level)
			{
				sprintf(szDbgMessage,"noOut");
				dbgPrintf(DBG_WRITE, pOpc2epics->recType);
				szDbgMessage[0] = NULL;
			}
			return 0;
		}

		v.vt = ait2vtTable[aitRec];
		if( v.vt )
		{
			void *pVariantData = &(v.bVal);
			if( ! aitConvert(aitRec, pVariantData, aitRec, pOpc2epics->pRecVal ,1) )
				return 1;
		}
		else if( aitRec = aitEnumString )
		{
			SOCmnVariant sVar( (LPCTSTR)(pOpc2epics->pRecVal) );
			v = sVar;
		}    
		else
		{
			errlogPrintf("opcSetScalar: %s unsupported ait type: %d\n",prec->name,aitRec);
			prec->nsta = menuAlarmStatREAD;	
			prec->nsev = menuAlarmSevrINVALID;
			prec->pact = TRUE;
			return 1;
		}
		if(DBG_WRITE & dbg_level)
		{
			sprintf(szDbgMessage,"%s (%s) SetScalar ait=%d vt=%d val=%s", prec->name,pRecProp->record,aitRec,v.vt,v.toString(&strDbg));
			dbgPrintf(DBG_WRITE, pOpc2epics->recType);
			szDbgMessage[0] = NULL;
		}
		oi->setWriteValue(v);
		oi->write();
		return setSecondaryAttributes(oi, pOpc2epics->pRecord, menuAlarmStatWRITE);
	}
	errlogPrintf("opcSetScalar: Warning! Invalid adress ");
	if(pOpc2epics && pOpc2epics->pRecord)
		errlogPrintf("(%s)\n",pOpc2epics->pRecord->name);
	else if(pOpc2epics && pOpc2epics->pOpcItem)
		errlogPrintf("(%s)\n",((CItem*)pOpc2epics->pOpcItem)->m_sPvName.c_str());
	else
		errlogPrintf("(unknown PV)\n");
	return 1;
}

static const LONGLONG epicsEpochInFileTime    = 0x1B41E2A18D64000;
static const LONGLONG FILE_TIME_TICKS_PER_SEC = 10000000;
long ft2epics(FILETIME *ft, epicsTimeStamp *et)
{ LARGE_INTEGER tmp;

  tmp.LowPart = ft->dwLowDateTime;
  tmp.HighPart = ft->dwHighDateTime;

  LONGLONG fileTimeTicksSinceEpochEPICS = tmp.QuadPart - epicsEpochInFileTime;
  et->secPastEpoch = fileTimeTicksSinceEpochEPICS / FILE_TIME_TICKS_PER_SEC;
  et->nsec = (fileTimeTicksSinceEpochEPICS % FILE_TIME_TICKS_PER_SEC)*100;
  return epicsTimeOK;
}

// disconnect opc-Server when CTRL-C, INThandler is set in iocShelMain.cpp
void  INThandler(int sig)
{   
	printf("abnormal termination!!!\nterminate me with exit, please\n\n");
	myOpc.Terminate();
}

void CItem::onSetReadValue()
{
	if(bInitialized && iIocInitReady)
	{
		FILETIME ft;
		pOpcInterface->getReadTimeStamp(&ft);
		if(DBG_READ & dbg_level)
		{
			sprintf(szDbgMessage,"%s: onSetReadValue",pOpc2Epics->pRecord->name);
			dbgPrintf(DBG_READ, pOpc2Epics->recType);
			szDbgMessage[0] = NULL;
		}
		if(pEpicsInterface->tse == epicsTimeEventDeviceTime ){ft2epics(&ft, &(pEpicsInterface->time));}
		if( pOpcInterface->isBad() )
		{	
			pEpicsInterface->nsta = menuAlarmStatREAD;
			pEpicsInterface->nsev = menuAlarmSevrINVALID;
		}
		else
		{
			pEpicsInterface->pact = FALSE;
		}
		if( pOpc2Epics->isCallback )
		{ 
			opcGetScalar(pOpc2Epics);	   // read value for out-records, in- and SCAN="I/O Intr"
			if( pOpc2Epics->isOutRecord )  // out-records are SCAN="passive" so scanIoRequest doesn't work
			{ 
				pOpc2Epics->noOut=1;
				if(DBG_READ & dbg_level)
				{
					sprintf(szDbgMessage,"%s: onSetReadValue callb %d",pOpc2Epics->pRecord->name,*(int*)(pOpc2Epics->pRecVal));
					dbgPrintf(DBG_READ, pOpc2Epics->recType);
					szDbgMessage[0] = NULL;
				}
				callbackRequest(&(pOpc2Epics->callback) );
			} 
			else
			{ 
				if(DBG_READ & dbg_level)
				{
					sprintf(szDbgMessage,"%s onSetReadValue scan",pOpc2Epics->pRecord->name);
					dbgPrintf(DBG_READ, pOpc2Epics->recType);
					szDbgMessage[0] = NULL;
				}
				scanIoRequest( pOpc2Epics->ioscanpvt );
			}
		}
	}
}
