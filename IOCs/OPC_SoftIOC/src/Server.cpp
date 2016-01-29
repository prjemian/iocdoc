/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Server.cpp

Project:        OPC group class

Description:    Contents one OPC server and creates several OPC groups

Author:         Winkler

Version:        $Revision: 1.0 $

History:

  $Log: Server.cpp,v $

  Revision 1.0  2004/05/19 12:00:00  winkler
  onSetObjectState implemented


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

// Server.cpp: Implementation of CServer class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "Group.h"
#include "Server.h"
char * ServerId =
"Server.cpp: $Revision: 1.0 $\n";

CServer::CServer(IN SODaCEntry *parent)
{
	m_Parent = parent;
	m_GroupCount = 0;
	m_GroupArray = NULL;
	m_pLastGroup = NULL;
}

CServer::~CServer()
{
	if(m_GroupArray)
	{
		for(unsigned long ul = 0;ul < m_GroupCount;ul++)
		{
			m_GroupArray[ul]->release();
			m_GroupArray[ul] = NULL;
		}
		delete m_GroupArray;
		m_GroupArray = NULL;
	}
}

BOOL CServer::AddGroup(LPCTSTR szGroup, unsigned long ulTime)
{
	BOOL bResult = FALSE;
	
	if(m_GroupArray = (CGroup**)realloc(m_GroupArray,(1+m_GroupCount)*sizeof(CGroup**)))
	{
		if(m_GroupArray[m_GroupCount] = (CGroup*)addGroup(szGroup, ulTime))
		{
			m_GroupArray[m_GroupCount]->m_sGroupName = szGroup;
			m_GroupArray[m_GroupCount]->m_ulTime = ulTime;
			m_pLastGroup = m_GroupArray[m_GroupCount];
			m_GroupCount++;
			bResult = TRUE;
		}
	}
	return bResult;
}

void CServer::onSetObjectState(void)
{
	SOCmnString szServerState;
	BYTE state = getObjectState();
	switch (state)
	{
		case SOCltElement::disconnected:
			szServerState = _T("disconnected");	
		break;
		case SOCltElement::connected:
			szServerState = _T("connected");	
		break;
		case SOCltElement::started:
			szServerState = _T("active");	
		break;
	}
	_tprintf(_T("Server state : %s                             \n"), szServerState);	
}