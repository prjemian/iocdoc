/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Opc.cpp

Project:        parent OPC client class

Description:    supports    - several OPC servers
                            - several OPC groups
							- several OPC items
							- iocshell.cmd files for configuration
                how to use  - make an instance of this COpc class
				            - run ReadCmd("iocshell.cmd") function
							- run Connect() and/or Start() function
							- stop it with Disconnect() and/or
							  Terminate() function

Author:         Winkler

Version:        $Revision: 1.01 $

History:

  $Log: Opc.cpp,v $
  Revision 1.0  2003/12/12 15:00:00  winkler
  modified for working with iocshell

  Revision 1.01  2004/05/19 12:00:00  winkler
  skip if opc-server or opc-group are not set

  

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

// Opc.cpp: Implementation of COpc class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "Creator.h"
#include "Server.h"
#include "Group.h"
#include "Item.h"
#include "Opc.h"
extern int dbg_level;
extern char szDbgMessage[256];
char * OpcId =
"Opc.cpp: $Revision: 1.01 $\n";

COpc::COpc()
{
	GetCurrentDirectory(MAX_PATH,m_szPath);
	strcat(m_szPath,"\\");
	char szTmp[MAX_PATH]; strcpy(szTmp, m_szPath);
	_fullpath( m_szPath, szTmp, MAX_PATH);
	m_ServerCount	=		0;
	m_ServerArray	=		NULL;
	m_Creator		=		new CCreator;			// create creator-object
	m_Entry = ::getSODaCEntry();					// get root-pointer of toolkit-session
    m_Entry->initialize(COINIT_MULTITHREADED);		// intialize SODAC library
    m_Entry->setCreator(m_Creator);
	m_CLSID = NULL;
	m_ClassIdList.destroy();
}

COpc::~COpc()
{
	m_ClassIdList.destroy();							// clean up the class-id-list
	m_Entry->terminate();
	if(m_ServerArray)
	{
		for(unsigned long ul = 0;ul < m_ServerCount;ul++)
		{
			m_ServerArray[ul]->release();
			m_ServerArray[ul] = NULL;
		}
		delete m_ServerArray;
		m_ServerArray = NULL;
	}
}

BOOL COpc::ReadCmd(IN LPCTSTR szPathName)
{
	BOOL bResult = FALSE;
	if(szPathName)
	{
		char *pszFile = NULL;					// stringpointer to copy of cmd-file (cmd-string)
		char *pszFileTerminator = NULL;			// last valid position in cmd-string
		char *pszStringWalker = NULL;			// actual position in cmd-string
		char szParameter1[MAX_PATH];
		char szParameter2[MAX_PATH];			// given parameters to iocshell command
		char *pszStop = NULL;
		BOOL bOpcServerDefined = FALSE;
		BOOL bOpcGroupDefinded = FALSE;
		if(ReadFile(szPathName, &pszFile))
		{
			// set marker to end of file string before it will be chopped
			pszFileTerminator = pszFile+strlen(pszFile);
			// chop string at CR
			ChopFile(&pszFile, strlen(pszFile), "\x0A");
			pszStringWalker = pszFile;
			while(pszStringWalker < pszFileTerminator)
			{	// skip if empty or comment line
				if(SkipWhiteSpaces(&pszStringWalker) && pszStringWalker[0] != '#') 
				{
					GetParameter(&pszStringWalker, szParameter1, szParameter2);
					if(strstr(pszStringWalker,"iocInit()"))
					{
						if(DBG_OPC_INIT & dbg_level)
						{						
							sprintf(szDbgMessage,"iocInit()");
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						if(!Start())
							errlogPrintf("WARNING: iocInit() failed\n");
					}
					if(strstr(pszStringWalker,"opcSetNames"))
					{
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"opcSetNames(\"%s\")", szParameter1);
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						if(!OpcSetNames(szParameter1))
							errlogPrintf("WARNING: opcSetNames(\"%s\") failed\n", szParameter1);
					}
					if(strstr(pszStringWalker,"opcSetServer"))
					{
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"opcSetServer(\"%s\",\"%s\")", szParameter1, szParameter2);
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						if(!OpcSetServer(szParameter1, szParameter2))
							errlogPrintf("WARNING: opcSetServer(\"%s\",\"%s\") failed\n", szParameter1, szParameter2);
						else
							bOpcServerDefined = TRUE;
					}
					if(bOpcServerDefined && strstr(pszStringWalker,"opcSetGroup("))
					{
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"opcSetGroup(\"%s\",\"%s\")", szParameter1, szParameter2);
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						if(!OpcSetGroup(szParameter1, atol(szParameter2)))
							errlogPrintf("WARNING: opcSetGroup(\"%s\",\"%s\") failed\n", szParameter1, szParameter2);
						else
							bOpcGroupDefinded = TRUE;
					}
					if(strstr(pszStringWalker,"opcSetGroupRefresh"))
					{
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"opcSetGroupRefresh(\"%s\")", szParameter1);
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						if(!SetGroupRefresh(atol(szParameter1)))
							errlogPrintf("WARNING: opcSetGroupRefresh(\"%s\") failed\n", szParameter1);
					}
					if(bOpcGroupDefinded && strstr(pszStringWalker,"dbLoadRecords"))
					{
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"dbLoadRecords(\"%s\")", szParameter1);
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						DbLoadRecords(szParameter1);
					}
					if(bOpcGroupDefinded && strstr(pszStringWalker,"dbLoadTemplate"))
					{
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"dbLoadTemplate(\"%s\")", szParameter1);
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						if(!DbLoadTemplate(szParameter1))
							errlogPrintf("WARNING: dbLoadTemplate(\"%s\") failed\n", szParameter1);
					}
					if(strstr(pszStringWalker,"opcDbg"))
					{
						int iTmp = 0;
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"opcDbg(\"%s\")", szParameter1);
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
						if(szParameter1[0] == '0' && (szParameter1[1] == 'x' || szParameter1[1] == 'X'))
							iTmp = strtol(szParameter1,&pszStop,16);
						else
							iTmp = strtol(szParameter1,&pszStop,10);
						if(iTmp >= 0)
							dbg_level = iTmp;
						else
							errlogPrintf("WARNING: opcDbg(\"%s\" failed\n", szParameter1);
						if(DBG_OPC_INIT & dbg_level)
						{
							sprintf(szDbgMessage,"\n**************************\n OPC \"cmd-parser\" started \n**************************\n\n");
							dbgPrintf(DBG_OPC_INIT);
							szDbgMessage[0] = NULL;
						}
					}
				}
				if(pszStringWalker < pszFileTerminator)
					pszStringWalker += strlen(pszStringWalker)+1;
			}
			if(DBG_OPC_INIT & dbg_level)
			{
				sprintf(szDbgMessage,"\n\n***************************\n OPC \"cmd-parser\" finished \n***************************\n\n");
				dbgPrintf(DBG_OPC_INIT);
				szDbgMessage[0] = NULL;
			}
		}
		bResult = TRUE;
		if(pszFile)
		{
			delete [] pszFile;
			pszFile = NULL;
		}
	}
	printf("\n");
	return bResult;
}

void COpc::GetFullCurrentPathName(IN char *szFileName[MAX_PATH])
{
	char *pszFileName = *szFileName;
	char szMyPathName[MAX_PATH];
	int iLen = 0;
	if(pszFileName[1] == '/')
		pszFileName+=2;
	strcpy(szMyPathName, m_szPath);
	strcat(szMyPathName, pszFileName);
	while(szMyPathName[iLen])
	{
		if(szMyPathName[iLen] == '/')
			szMyPathName[iLen] = '\\';
		iLen++;
	}
	strcpy(*szFileName, szMyPathName);
}

BOOL COpc::ReadFile(LPCTSTR szPathName, char **pszFile)
{
	BOOL bResult = FALSE;
	// clean up string array
	if(*pszFile)
	{
		delete [] *pszFile;
		*pszFile = NULL;
	}
	// got file location?
	if(szPathName)
	{
		// read file
		FILE *fhFile;
		if(!(fhFile=fopen(szPathName,"r")))
		{
			errlogPrintf("ERROR: \"%s\" not found or no access!\n", szPathName);
		}
		else
		{
			fseek(fhFile, 0L, SEEK_END);
			unsigned long ulFileSize = ftell(fhFile);
			*pszFile = new char[ulFileSize+1];
			rewind(fhFile);
			ulFileSize = fread(*pszFile, 1, ulFileSize, fhFile);
			(*pszFile)[ulFileSize]=NULL;
			fclose(fhFile);
			ulFileSize = strlen(*pszFile);
			*pszFile = (char*) realloc (*pszFile, (ulFileSize+1)*sizeof(char));
			bResult = TRUE;
		}
	}
	return bResult;
}

BOOL COpc::ChopFile(char **pszFile, unsigned long lFileSize, char *pszTerminators)
{
	BOOL bResult = FALSE;
	if(pszFile && pszTerminators)
	{
		char *pszFileTerminator = *pszFile+lFileSize;	// last valid character
		char *pszStringWalker = NULL;					// character sniffer
		// change all terminator characters to NULL == chop string into array
		while(*pszTerminators)
		{
			pszStringWalker = *pszFile;
			while(pszStringWalker < pszFileTerminator)
			{
				if(pszStringWalker[0] == pszTerminators[0])
					pszStringWalker[0] = NULL;
				pszStringWalker++;
			}
			pszTerminators++;
		}
		bResult = TRUE;
	}
	return bResult;
}


BOOL COpc::SkipWhiteSpaces(char **psz)
{
	BOOL bResult = FALSE;
	while((*psz)[0] == ' ' || (*psz)[0] == '\t')
		(*psz)++;
	if((*psz)[0])
		bResult = TRUE;
	return bResult;
}

void COpc::GetParameter(char **pszLine, char pszParameter1[MAX_PATH], char pszParameter2[MAX_PATH])
{
	pszParameter1[0] = NULL;
	pszParameter2[0] = NULL;
	if(strlen(*pszLine) >= MAX_PATH)
		return;
	char *psz;
	psz = strchr(*pszLine, '"');
	if(psz)
	{
		strcpy(pszParameter1, ++psz);
		pszParameter1[strchr(pszParameter1,'"')-pszParameter1]=NULL;
	}
	psz = strchr(*pszLine, '"');
	if(psz)
	{
		psz = strchr(++psz, '"');
		if(psz)
		{
			psz = strchr(++psz, '"');
			if(psz)
			{
				strcpy(pszParameter2, ++psz);
				pszParameter2[strchr(pszParameter2,'"')-pszParameter2]=NULL;
			}
		}
	}
}

BOOL COpc::GetClassId(IN SOCmnString soNode, IN SOCmnString soServerName)
{
	BOOL bResult = FALSE;
	SOCmnPointer<SOCltServerBrowser>	ServerBrowser = NULL;// pointer to server browser
	ServerBrowser  =	new SOCltServerBrowser();	// create OPC server browser
	ServerBrowser->setNodeName(soNode);
	ServerBrowser->browseServer( SOCLT_BROWSE_SERVER_CAT_ALL , m_ClassIdList);
	SOCmnListPosition pos = m_ClassIdList.getStartPosition();
	while(pos)
	{ 
		m_CLSID = m_ClassIdList.getNext(pos);
		ServerBrowser->getServerDescription(*m_CLSID, m_soServerDescription);
		ServerBrowser->getServerProgId(*m_CLSID, m_soServerProgId);
		if( m_soServerProgId == soServerName || m_soServerDescription == soServerName)
		{
			bResult = TRUE;
			break;
		}
		else
		{
			m_CLSID->Data1=NULL;	
			m_CLSID->Data2=NULL;	
			m_CLSID->Data3=NULL;	
			m_CLSID->Data4[0]=NULL;	
			m_CLSID->Data4[1]=NULL;
			m_CLSID->Data4[2]=NULL;
			m_CLSID->Data4[3]=NULL;
			m_CLSID->Data4[4]=NULL;
			m_CLSID->Data4[5]=NULL;
			m_CLSID->Data4[6]=NULL;
			m_CLSID->Data4[7]=NULL;
		}
	}
	ServerBrowser.release();						// have to be released before terminate toolkit session
	ServerBrowser = NULL;
	return bResult;
}

BOOL COpc::OpcSetNames(IN char szFileName[MAX_PATH])
{
	BOOL bResult = FALSE;
	char *pszFileTerminator = NULL;
	char *pszFile = NULL;
	char *pszStringWalker = NULL;
	unsigned long ulFileLen = 0;
	GetFullCurrentPathName(&szFileName);
	if(ReadFile(szFileName, &pszFile))
	{
		pszFileTerminator = pszFile + strlen(pszFile);
		pszStringWalker = pszFile;
		ChopFile(&pszFile, strlen(pszFile),"\x0A");
		while(pszStringWalker < pszFileTerminator)
		{
			*(strchr(pszStringWalker, '=')-1) = NULL;
			ulFileLen = strlen(pszStringWalker)+3;
			m_NameMap[pszStringWalker] = (pszStringWalker+ulFileLen);
			if(DBG_OPC_MAP & dbg_level)
			{
				sprintf(szDbgMessage,"   %s<=>%s (%d)",pszStringWalker,pszStringWalker+ulFileLen, m_NameMap.size() );
				dbgPrintf(DBG_OPC_MAP);
				szDbgMessage[0] = NULL;
			}
			pszStringWalker += (ulFileLen + strlen(pszStringWalker+ulFileLen)+1);
		}
		bResult = TRUE;
	}
	if(pszFile)
	{
		delete [] pszFile;
		pszFile = NULL;
	}
	return bResult;
}

BOOL COpc::OpcSetServer(IN LPCTSTR szNode, IN LPCTSTR szName)
{
	BOOL bResult = FALSE;
	if(m_Entry.isNotNull())				// Softing Toolbox ok
	{
		if(GetClassId(szNode,szName))	// found class id of server
		{
			if(m_CLSID->Data1)			// valid class id
			{
				if(m_ServerArray = (CServer**)realloc(m_ServerArray,(1+m_ServerCount)*sizeof(CServer**)))
				{						// created new instance of server object
					if((m_ServerArray[m_ServerCount] = (CServer*)m_Entry->addServer(szName, szNode, *m_CLSID)))
					{
						m_ServerArray[m_ServerCount]->m_sServerName = szName;
						m_ServerArray[m_ServerCount]->m_sNode = szNode;
						m_ServerCount++;
						bResult = TRUE;
					}
				}
			}
		}
	}
	return bResult;
}

BOOL COpc::OpcSetGroup(IN LPCTSTR szName, IN unsigned long ulTime)
{
	BOOL bResult = FALSE;
	if(m_ServerCount > 0)
		if(m_ServerArray[m_ServerCount-1]->AddGroup(szName, ulTime))
			bResult = TRUE;
	return bResult;
}

BOOL COpc::SetGroupRefresh(IN int iRefreshTime)
{
	BOOL bResult = FALSE;
	if(m_ServerCount > 0)
	{
		m_ServerArray[m_ServerCount-1]->GetLastGroup()->SetRefreshTimer(iRefreshTime);
		bResult = TRUE;
	}
	return bResult;
}

BOOL COpc::OpcSetItem(IN LPCTSTR szItemID, IN LPCTSTR szPvName)
{
	if(!m_ServerArray)	// no opc defined
		return TRUE;
	BOOL bResult = FALSE;
	if(m_ServerArray[m_ServerCount-1]->m_GroupCount > 0)
		if(m_ServerArray[m_ServerCount-1]->m_GroupArray[m_ServerArray[m_ServerCount-1]->m_GroupCount-1]->AddItem(szItemID, szPvName))
			bResult = TRUE;
	CItem *pNewItem = m_ServerArray[m_ServerCount-1]->m_GroupArray[m_ServerArray[m_ServerCount-1]->m_GroupCount-1]
		->m_ItemArray[m_ServerArray[m_ServerCount-1]->m_GroupArray[m_ServerArray[m_ServerCount-1]->m_GroupCount-1]->m_ItemCount-1];
	m_PointerMap[szPvName] = pNewItem;
	return bResult;
}

BOOL COpc::DbLoadRecords(char *szFileName)
{
	BOOL bResult = FALSE;
	char *pszFile = NULL;
	GetFullCurrentPathName(&szFileName);
	if(ReadFile(szFileName, &pszFile))
	{
		bResult = ScanStringAndAddOpcItems(&pszFile);
		if(pszFile)
		{
			delete [] pszFile;
			pszFile = NULL;
		}
	}
	return bResult;
}

BOOL COpc::DbLoadTemplate(char *szFileName)
{
	BOOL bResult = FALSE;
	BOOL bReplace = FALSE;
	char *pszFileTerminator = NULL;
	char *pszStringWalker = NULL;
	char *pszFile = NULL;
	char *pszFormular = NULL;
	char **pTmp = NULL;
	char szSubstitutionFileName[MAX_PATH];
	int iLayer = 0;
	string sFormular, sSubstitution, sSearch, sFind, sReplace;
	string::size_type sPos = 0;
	size_t sSize = 0;
	GetFullCurrentPathName(&szFileName);
	if(ReadFile(szFileName, &pszFile))
	{
		// set marker to end of file string before it will be chopped
		pszFileTerminator = pszFile+strlen(pszFile);
		// chop string at CR
		ChopFile(&pszFile, strlen(pszFile), "\x0A");
		pszStringWalker = pszFile;
		while(pszStringWalker < pszFileTerminator)
		{	// skip if empty or comment line
			if(SkipWhiteSpaces(&pszStringWalker) && pszStringWalker[0] != '#') 
			{
				if(strstr(pszStringWalker, "file "))
				{
					pszStringWalker = strstr(pszStringWalker, "file ") +5;
					while(pszStringWalker[0] >= '0' && pszStringWalker[0] && sReplace[sPos] <= 'z')
						pszStringWalker++;
					strcpy(szSubstitutionFileName, pszStringWalker);
					sPos = 0;
					while(szSubstitutionFileName[sPos] > ' ' && szSubstitutionFileName[sPos]  <= 'z')
						sPos++;
					szSubstitutionFileName[sPos] = NULL;
					pTmp = new char*;
					*pTmp = szSubstitutionFileName;
					GetFullCurrentPathName(pTmp);
					if(DBG_TEMPLATE & dbg_level)
					{
						sprintf(szDbgMessage,"%s",szSubstitutionFileName);
						dbgPrintf(DBG_TEMPLATE);
						szDbgMessage[0] = NULL;
					}
					if(ReadFile(szSubstitutionFileName, &pszFormular))
					{
						sFormular = pszFormular;
						sSubstitution = pszFormular;
						if(pszFormular)
						{
							delete[] pszFormular;
							pszFormular = NULL;
						}
					}
					delete pTmp;
					pTmp = NULL;
					while(pszStringWalker < pszFileTerminator && iLayer == 0)
					{
						while(strchr(pszStringWalker, '{'))
						{
							pszStringWalker = strchr(pszStringWalker, '{') +1;
							iLayer++;
						}
						if(iLayer == 0)
						{
							if(pszStringWalker < pszFileTerminator)
								pszStringWalker += strlen(pszStringWalker)+1;
							else
								break;
						}
					}
					while(pszStringWalker < pszFileTerminator && iLayer != 0)
					{
						do
						{
							while(strchr(pszStringWalker, '{'))
							{
								pszStringWalker = strchr(pszStringWalker, '{') +1;
								iLayer++;
							}
							sSearch = pszStringWalker;
							sPos = sSearch.find("=",0);
							if(sPos != string::npos)
							{
								while(sSearch[sPos-1] < '-' || sSearch[sPos-1] > 'z')
									sPos--;
								sSearch[sPos] = NULL;
								while(sSearch[sPos-1] >= '-' && sSearch[sPos-1] <= 'z')
									sPos--;
								sFind = (char*)&(sSearch.at(sPos));
							}
							sSearch = pszStringWalker;
							sPos = sSearch.find("=",0);
							if(sPos != string::npos)
							{
								while(sSearch[sPos+1] < '-' || sSearch[sPos-1] > 'z')
									sPos++;
								sReplace = (char*)&(sSearch.at(sPos+1));
								sPos = 0;
								while(sReplace[sPos] >= '-' && sReplace[sPos] <= 'z')
									sPos++;
								sReplace[sPos] = NULL;
							}
							if(strstr(pszStringWalker,sReplace.c_str()))
								pszStringWalker = strstr(pszStringWalker,sReplace.c_str()) + strlen(sReplace.c_str());
							if(!sFind.empty())
							{
								if(DBG_TEMPLATE & dbg_level)
								{
									sprintf(szDbgMessage,"Find: %-8s and replace it with: %s",sFind.c_str(), sReplace.c_str());
									dbgPrintf(DBG_TEMPLATE);
									szDbgMessage[0] = NULL;
								}
								sFind.insert(0,"$(");
								sFind += ")";
								sSize = sFind.length();
								while((sPos = sSubstitution.find(sFind,0)) != string::npos)
								{
									sSubstitution.replace(sPos, sSize, sReplace.c_str());
								}
								sFind.erase();
								sReplace.erase();
								bReplace = TRUE;
								bResult = TRUE;
							}
						}
						while(strchr(pszStringWalker,',') && (++pszStringWalker)[0]);
						if(bReplace)
							if(pszFormular = new char[strlen(sSubstitution.c_str())+1])
							{
								strcpy(pszFormular,sSubstitution.c_str());
								ScanStringAndAddOpcItems(&pszFormular);
								sSubstitution.erase();
								delete [] pszFormular;
								pszFormular = NULL;
								sSubstitution = sFormular;
								bReplace = FALSE;
							}
						while(strchr(pszStringWalker, '}'))
						{
							pszStringWalker = strchr(pszStringWalker, '}')+1;
							iLayer--;
						}
						
						if(pszStringWalker < pszFileTerminator)
							pszStringWalker += strlen(pszStringWalker)+1;
					}
				}
			}
			if(pszStringWalker < pszFileTerminator)
				pszStringWalker += strlen(pszStringWalker)+1;
		}
		if(pszFile)
		{
			delete [] pszFile;
			pszFile = NULL;
		}	
	}
	return bResult;
}

BOOL COpc::ScanStringAndAddOpcItems(char **pszFile)
{
	BOOL bResult = FALSE;
	char *pszFileTerminator = NULL;
	char *pszStringWalker = NULL;
	char *pszLookBack = NULL;
	// set marker to end of file string before it will be chopped
	pszFileTerminator = *pszFile+strlen(*pszFile);
	// chop string at CR
	ChopFile(pszFile, strlen(*pszFile), "\x0A");
	pszStringWalker = *pszFile;
	while(pszStringWalker < pszFileTerminator)
	{	// skip if empty or comment line
		if(SkipWhiteSpaces(&pszStringWalker) && pszStringWalker[0] != '#') 
		{
			while(pszStringWalker < pszFileTerminator)
			{
				if(strstr(pszStringWalker,"\"opc\""))
				{
					while(pszStringWalker < pszFileTerminator)
					{
						if(strstr(pszStringWalker,"\"@"))
						{
							pszStringWalker = strstr(pszStringWalker,"\"@")+2;
							if(strchr(pszStringWalker, '"'))
								*(strchr(pszStringWalker, '"')) = NULL;
							m_NamePos = m_NameMap.find(pszStringWalker);
							// search PV Name backwards
							pszLookBack = pszStringWalker;
							while(!strstr(pszLookBack,"record"))
								pszLookBack--;
							if(strstr(pszLookBack,"record"))
							{
								pszLookBack = strstr(pszLookBack,"\"")+1;
								*(strstr(pszLookBack,"\"")) = NULL;
							}
							else
								return FALSE;
							if(m_NamePos != m_NameMap.end())
								OpcSetItem((*m_NamePos).second.c_str(),pszLookBack);
							else
								OpcSetItem(pszStringWalker, pszLookBack);
						}
						if(pszStringWalker < pszFileTerminator)
							pszStringWalker += strlen(pszStringWalker)+1;
					}
					bResult = TRUE;
				}
				if(pszStringWalker < pszFileTerminator)
					pszStringWalker += strlen(pszStringWalker)+1;
			}
		}
		if(pszStringWalker < pszFileTerminator)
			pszStringWalker += strlen(pszStringWalker)+1;
	}
	return bResult;
}

BOOL COpc::Connect()
{
	if(!m_ServerArray)
		return TRUE;
	BOOL bResult = FALSE;
	if(m_Entry.isNotNull() && !m_Entry->isConnected())
	{
		m_Entry->connect();
		printf("OPC session connected\n");
	}
	if(m_Entry.isNotNull() && m_Entry->isConnected())
		bResult = TRUE;
	return bResult;
}

BOOL COpc::Start()
{
	if(!m_ServerArray)
		return TRUE;
	BOOL bResult = FALSE;
	if(m_Entry.isNotNull() && !m_Entry->isStarted())
	{
		m_Entry->start();
		printf("OPC session started\n");
	}
	if(m_Entry.isNotNull() && m_Entry->isStarted())
		bResult = TRUE;
	return bResult;
}

BOOL COpc::Disconnect()
{
	if(!m_ServerArray)
		return TRUE;
	BOOL bResult = FALSE;
	if(m_Entry.isNotNull() && m_Entry->isConnected())
	{
		m_Entry->disconnect();
		printf("OPC session disconnected\n");
	}
	if(m_Entry.isNotNull() && !m_Entry->isConnected())
		bResult = TRUE;
	return bResult;
}

BOOL COpc::Terminate()
{
	if(!m_ServerArray)
		return TRUE;
	BOOL bResult = FALSE;
	if(m_Entry.isNotNull() && m_Entry->isConnected())
	{
		m_Entry->terminate();
		printf("OPC session terminated\n");
	}
	if(m_Entry.isNotNull() && !m_Entry->isConnected())
		bResult = TRUE;
	return bResult;
}
