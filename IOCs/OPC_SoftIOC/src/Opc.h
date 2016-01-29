/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Opc.h

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

Version:        $Revision: 1.0 $

History:

  $Log: Opc.h,v $
  Revision 1.0  2003/12/12 15:00:00  winkler
  modified for working with iocshell

  

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

// Opc.h: interface for COpx class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_OPC_H__C070B5D5_E1E0_49E6_8088_61EF2307AB2F__INCLUDED_)
#define AFX_OPC_H__C070B5D5_E1E0_49E6_8088_61EF2307AB2F__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CItem;
class CServer;
class CCreator;

class COpc  
{
public:
	BOOL Terminate();
	BOOL Disconnect();
	BOOL Start();
	BOOL Connect();
	BOOL ReadCmd(LPCTSTR szPathName);
	COpc();
	virtual ~COpc();
	map<string, CItem*> m_PointerMap;
	std::map<string, CItem*>::iterator m_PointerMapPos;
protected:
	BOOL ScanStringAndAddOpcItems(char **pszFile);
	void GetFullCurrentPathName(IN char *szFileName[MAX_PATH]);
	BOOL OpcSetServer(IN LPCTSTR szNode, IN LPCTSTR szName);
	BOOL OpcSetGroup(IN LPCTSTR szName, IN unsigned long ulTime);
	BOOL OpcSetItem(IN LPCTSTR szItemID, IN LPCTSTR szPvName);
	BOOL SetGroupRefresh(IN int iRefreshTime);
	BOOL DbLoadTemplate(IN char *szFileName);
	BOOL DbLoadRecords(IN char *szFileName);
	BOOL GetClassId(IN SOCmnString soNode, IN SOCmnString soServerName);
	BOOL OpcSetNames(IN char szFileName[MAX_PATH]);
	BOOL SkipWhiteSpaces(char **psz);
	BOOL ChopFile(char **pszFile, unsigned long lFileSize, char *pszTerminators);
	BOOL ReadFile(IN LPCTSTR szPathName, char **pszFile);
	void GetParameter(char **pszLine, char pszParameter1[256], char pszParameter2[256]);
	map<string, string> m_NameMap;
	std::map<string, string>::iterator m_NamePos;
	char m_szPath[MAX_PATH];
	unsigned long m_ServerCount;
	SOCmnPointer<SODaCEntry>			m_Entry;
	CServer**							m_ServerArray;	// pointer to server array of actually session
	SOCmnList<CLSID>					m_ClassIdList;	// pointer to Class ID list (List of opc servers)
	SOCmnPointer<CCreator>				m_Creator;		// class to create OPCItems
	CLSID* m_CLSID;
    SOCmnString m_soServerDescription;
    SOCmnString m_soServerProgId;
};

#endif // !defined(AFX_OPC_H__C070B5D5_E1E0_49E6_8088_61EF2307AB2F__INCLUDED_)
