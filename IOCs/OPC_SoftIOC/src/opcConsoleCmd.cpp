/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/drvOpc.cpp

Project:        Device support for OPC

Description:    All opc access and conversion of data type is done here.
                Epics related stuff is implemented in devOpc.c

Author:         Bernhard Kuner, Carsten Winkler

Version:        $Revision: 1.1 $

History:

  $Log: opcConsoleCmd.cpp,v $
  Revision 1.1  2003/12/11 12:49:04  kuner
  Array Access added, outsource console functions to opcConsoleCmd.cpp


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
char * opcConsoleCmdId =
"opcConsoleCmd: $Revision: 1.1 $\n";

#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <winsock2.h>	//need definition of: FILETIME

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
#include "errlog.h"
#include "iocsh.h"
#include "devOpc.h"
#include "drvOpc.h"
#include "opcConsoleCmd.h"

#include "errDbg.h"

#ifdef __cplusplus
extern "C" { 
#endif
extern int iIocInitReady;
extern char * devOpcId;
#ifdef __cplusplus
}
#endif

extern char * iocShellMainId;
extern char * drvOpcId;
extern char * OpcId;
extern char * CreatorId;
extern char * ServerId;
extern char * GroupId;
extern char * ItemId;
extern char szDbgMessage[256];

static const iocshArg opcArg = {">>Use in 'cmd-file' only!<<",iocshArgString};

int opcNameTranslationFlag = 0;
static const iocshArg opcSetServerArg0	= {"[OPC-Server Name]", iocshArgString};
static const iocshArg opcSetServerArg1	= {"[Host]", iocshArgString};
static const iocshArg * const  opcSetServerArg[3]= {&opcSetServerArg0, &opcSetServerArg1, &opcArg};
iocshFuncDef opcSetServerFuncDef = {"opcSetServer", 3, opcSetServerArg};
void opcSetServer(const iocshArgBuf *args )
{
	if(iIocInitReady)
		printf("\t%s\n",opcArg);
	return;
}

//add group and set use it for all createion of items until there is an other group set
static const iocshArg opcSetGroupArg0	= {"add and set Group name", iocshArgString};
static const iocshArg opcSetGroupArg1	= {"scan rate > 0 ms", iocshArgInt};
static const iocshArg * const  opcSetGroupArg[3]= {&opcSetGroupArg0, &opcSetGroupArg1, &opcArg};
iocshFuncDef opcSetGroupFuncDef = {"opcSetGroup", 3, opcSetGroupArg};
void opcSetGroup( const iocshArgBuf *args )
{
	if(iIocInitReady)
	{
		printf("\t%s\n",opcArg);
	}
	return;
}
//add refresh-cycle for last defined group
static const iocshArg opcSetGroupRefreshArg0	= {"set refresh-cycle in ms for last defined Group", iocshArgString};
static const iocshArg * const  opcSetGroupRefreshArg[2]= {&opcSetGroupRefreshArg0, &opcArg};
iocshFuncDef opcSetGroupRefreshFuncDef = {"opcSetGroupRefresh", 2, opcSetGroupRefreshArg};
void opcSetGroupRefresh( const iocshArgBuf *args )
{
	if(iIocInitReady==1)
	{
		iIocInitReady=2;
		printf("Disabled all automatical opc group refreshes!\n");
	}
	else if(iIocInitReady==2)
	{
		iIocInitReady=1;
		printf("Enabled all automatical opc group refreshes!\n");
	}
	return;
}
// iocSh command line tool to browse items of connected server
void opcPrintItemList(SOCltBrowseObject* pObj, int tabs, int maxLayer)
{
   static int cnt;
   if(tabs==0) cnt=0;

   SOCmnList<SOCltBrowseObject> obj;

     printf("level: %d\n",tabs);
   if ( pObj->expand( SOCMNOBJECT_TYPE_ALL, obj) )
   { 
     SOCmnListPosition pos = obj.getStartPosition();
     while(pos)
     { 
       printf("%d ",cnt++);
       for ( int i=0 ; i < tabs ; i++ )  printf(" ");

       SOCltBrowseObject* pNext = obj.getNext(pos);
       if( ! pNext ) continue;
       SOCmnString path = (LPCTSTR)pNext->getPath();
       SOCmnString display = (LPCTSTR)pNext->getDisplayName();

       if ( !path.isEmpty() ) printf("%s : \"",(LPCTSTR)pNext->getPath());
       if ( !display.isEmpty() ) printf("%s",(LPCTSTR)pNext->getDisplayName());
       //if ( pNext->isExpandable() ) printf 
       printf("%s",(pNext->isExpandable() ? "\" ->\n": "\"\n"));//std::cout << (pNext->isExpandable() ? "\" ->\n": "\"\n");

       if ( pNext->isExpandable() && tabs<maxLayer)
         opcPrintItemList(pNext, tabs + 1, maxLayer);
     }
   }
}

static const iocshArg opcSetNamesArg0	= {"name translation file", iocshArgString};
static const iocshArg * const  opcSetNamesArg[1]= {&opcSetNamesArg0};
iocshFuncDef opcSetNamesFuncDef = {"opcSetNames", 1, opcSetNamesArg};
void opcSetNames( const iocshArgBuf *args )
{
	if(iIocInitReady)
		printf("\t%s\n",opcArg);
	return;
}

IorItemVec iorItems;
void IorItem::dumpItem(void)
{	// get the values of record.DTYP field and record type by epics database access
	std::string dtype(epicsName); 
	std::string recType;
	dtype += ".DTYP";
    DBENTRY	dbentry;
    DBENTRY	*pdbentry = &dbentry;
    dbInitEntry(pdbbase,pdbentry);
	if( ! dbFindRecord(pdbentry,dtype.c_str() ) )
	{   dtype = dbGetString(pdbentry);
  	}
	if( ! dbGetRecordAttribute(pdbentry,"RTYP" ) )
	{   recType = dbGetString(pdbentry);
  	}
  	dbFinishEntry(pdbentry);
	printf("%27s | %12s | %6s | %27s | %s\n",epicsName.c_str(), recType.c_str(), dtype.c_str(), opcName.c_str(), opcFullName.c_str() ); 
} 



static const iocshArg opcIorFuncArg0	= {">>shows opc-epics map<<", iocshArgString};
static const iocshArg * const  opcIorArg[1]= {&opcIorFuncArg0};
iocshFuncDef opcIorFuncDef = {"opcIor", 1, opcIorArg};
void opcIor( const iocshArgBuf *args )
{ 
	printf ("\n%27s | %12s | %6s | %27s | %s\n"
	"----------------------------+--------------+--------+-----------------------------+------------------------------\n",
	"epicsName","Record Type", "Dtype", "opcName", "opcFullName");
	for(IorItemVec::iterator p = iorItems.begin(); p != iorItems.end(); p++) (*p)->dumpItem();
}

static const iocshArg opcDbgArg0	= {"<n>\n", iocshArgInt};
static const iocshArg opcDbgArg1	= {"\n  It shows more informations about opc device driver.\n"\
	"  Argument n may be hexadecimal OR decimal value\n"\
	"\t0x00000001\tShow version of opc device driver\n"\
	"\t0x00000002\tShow read values\n"\
	"\t0x00000004\tShow write values\n"\
	"\t0x00000008\tShow bad values\n"\
	"\t0x00000010\tShow OPC init\n"\
	"\t0x00000020\tShow all OPC variables\n"\
	"\t0x00000040\tShow OPC-EPICS-MAPPING\n"\
	"\t0x00000080\tShow template processing\n"\
	"\t0x00000100\tShow OPC-group refreshing\n"\
	"\t0x00000200\tundefined\n"\
	"\t0x00000400\tundefined\n"\
	"\t0x00000800\tundefined\n"\
	"\t0x00001000\tundefined\n"\
	"\t0x00002000\tShow only ai(r) variables\n"\
	"\t0x00004000\tShow only aai variables\n"\
	"\t0x00008000\tShow only bi(r) variables\n"\
	"\t0x00010000\tShow only longin variables\n"\
	"\t0x00020000\tShow only mbbi(r) variables\n"\
	"\t0x00040000\tShow only mbbiDirect(r) variables\n"\
	"\t0x00080000\tShow only stringin variables\n"\
	"\t0x00100000\tShow only eventval variables\n"\
	"\t0x00200000\tShow only histogramval variables\n"\
	"\t0x00300000\tShow only ao(r) variables\n"\
	"\t0x00800000\tShow only aao variables\n"\
	"\t0x01000000\tShow only bo(r) variables\n"\
	"\t0x02000000\tShow only longout variables\n"\
	"\t0x04000000\tShow only mbbo(r) variables\n"\
	"\t0x08000000\tShow only mbboDirect(r) variables\n"\
	"\t0x10000000\tShow only stringout variables\n"\
	"\t0x20000000\tShow only waveformval variables\n"\
	"\t0x40000000\tColored output\n"\
	"\t0x80000000\tundefined\n"\
	"You can add these values to get several outputs.\n"
	, iocshArgInt};
static const iocshArg * const  opcDbgArg[2]= {&opcDbgArg0,&opcDbgArg1};
iocshFuncDef opcDbgFuncDef = {"opcDbg", 2, opcDbgArg};
void opcDbg( const iocshArgBuf *args )
{
	dbg_level = args[0].ival;
//	sprintf(szDbgMessage,"Version 1.1\n\n\t- %s\t- %s\t- %s\t- %s\t- %s\t- %s\t- %s\t- %s\n\n",
//		iocShellMainId, devOpcId, drvOpcId, OpcId, CreatorId, ServerId, GroupId, ItemId);
//	dbgPrintf(DBG_VERSION);
//	szDbgMessage[0] = NULL;
	printf("Version 2.0.1\n\n\t- %s\t- %s\t- %s\t- %s\t- %s\t- %s\t- %s\t- %s\n\n",
		iocShellMainId, devOpcId, drvOpcId, OpcId, CreatorId, ServerId, GroupId, ItemId);
}


//create a static object to make shure that opcRegisterToIocShell is called on beginning of
class OpcRegisterToIocShell
{
public :
	OpcRegisterToIocShell(void);
};

OpcRegisterToIocShell::OpcRegisterToIocShell(void)
{ iocshRegister(&opcSetGroupRefreshFuncDef, opcSetGroupRefresh);
  iocshRegister(&opcSetGroupFuncDef, opcSetGroup);
  iocshRegister(&opcSetServerFuncDef, opcSetServer);
  iocshRegister(&opcSetNamesFuncDef, opcSetNames);
  iocshRegister(&opcIorFuncDef, opcIor);
  iocshRegister(&opcDbgFuncDef, opcDbg);
}
static OpcRegisterToIocShell opcRegisterToIocShell;

