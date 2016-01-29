/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Group.cpp

Project:        OPC group class

Description:    Contents one OPC group and creates several OPC items

Author:         Winkler

Version:        $Revision: 0.91 $

History:

  $Log: Group.cpp,v $


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

// Group.cpp: Implementation of CGroup class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "Item.h"
#include "Group.h"
extern int dbg_level;
extern char szDbgMessage[256];
extern "C" int iIocInitReady;
char * GroupId =
"Group.cpp: $Revision: 0.91 $\n";

CGroup::CGroup(IN CServer* parent)
{
	m_ItemCount = 0;
	m_Parent = parent;
	m_ItemArray = NULL;
	m_iRefreshTime = 0;
	m_hRefreshTimer = 0;
}

CGroup::~CGroup()
{
	if(m_ItemArray)
	{
		for(unsigned long ul = 0;ul < m_ItemCount;ul++)
		{
			m_ItemArray[ul]->release();
			m_ItemArray[ul] = NULL;
		}
		delete m_ItemArray;
		m_ItemArray = NULL;
	}
}

BOOL CGroup::AddItem(LPCTSTR szItemID, LPCTSTR szPvName)
{
	BOOL bResult = FALSE;
	if(m_ItemArray = (CItem**)realloc(m_ItemArray, (1+m_ItemCount)*sizeof(CItem**)))
	{
		if(m_ItemArray[m_ItemCount] = (CItem*)addItem(szItemID))
		{
			m_ItemArray[m_ItemCount]->m_soItemID = szItemID;
			m_ItemArray[m_ItemCount]->m_sPvName  = szPvName;
			m_ItemCount++;
			if(DBG_OPC_VARS & dbg_level)
			{
				sprintf(szDbgMessage,"   %s <==> %s (%d)",m_ItemArray[m_ItemCount-1]->m_soItemID,m_ItemArray[m_ItemCount-1]->m_sPvName.c_str(),m_ItemCount);
				dbgPrintf(DBG_OPC_VARS);
				szDbgMessage[0] = NULL;
			}
			bResult = TRUE;
		}
	}
	return bResult;
}

void CGroup::SetRefreshTimer(int iRefreshTime)
{
	if(DBG_OPC_REFRESH & dbg_level)
	{
		sprintf(szDbgMessage,"SetRefreshTimer: %s will be refreshed every %d ms ",m_sGroupName.c_str(),iRefreshTime);
		dbgPrintf(DBG_OPC_REFRESH);
		szDbgMessage[0] = NULL;
	}
	m_iRefreshTime = iRefreshTime;
	if(m_hRefreshTimer == 0)
		m_hRefreshTimer = _beginthread(RefreshTimer, 0, this);
//	printf("(%lu)\n",m_hRefreshTimer);
}

void CGroup::RefreshTimer(void *param)
{
	if(DBG_OPC_REFRESH & dbg_level)
	{
		sprintf(szDbgMessage,"\nRefresh-circle of Group %s started with %d ms refresh cycle.\n\tWaiting for \"iocInit()\" ...\n",((CGroup*)(param))->m_sGroupName.c_str(),((CGroup*)param)->m_iRefreshTime);
		dbgPrintf(DBG_OPC_REFRESH);
		szDbgMessage[0] = NULL;
	}
	while(((CGroup*)(param))->m_iRefreshTime > 0)
	{
		Sleep(((CGroup*)param)->m_iRefreshTime);
		if(iIocInitReady==1)
		{
			((CGroup*)param)->asyncRefresh(OPC_DS_DEVICE);//OPC_DS_CACHE);
			if(DBG_OPC_REFRESH & dbg_level)
			{
				sprintf(szDbgMessage,"Group %s refreshed.",((CGroup*)(param))->m_sGroupName.c_str());
				dbgPrintf(DBG_OPC_REFRESH);
				szDbgMessage[0] = NULL;
			}
		}
	}
	_endthread();
}
