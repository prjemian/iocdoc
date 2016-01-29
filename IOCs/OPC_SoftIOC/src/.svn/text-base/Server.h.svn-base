/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Server.h

Project:        OPC group class

Description:    Contents one OPC server and creates several OPC groups

Author:         Winkler

Version:        $Revision: 0.9 $

History:

  $Log: Server.h,v $


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

// Server.h: interface for CServer class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_SERVER_H__0375C68A_14B5_4056_B29E_CE6C93B5CF99__INCLUDED_)
#define AFX_SERVER_H__0375C68A_14B5_4056_B29E_CE6C93B5CF99__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CGroup;

class CServer : public SODaCServerDefault 
{
public:
	string m_sServerName;
	string m_sNode;
	BOOL AddGroup(LPCTSTR szGroup, unsigned long ulTime);
	CGroup* GetLastGroup(){return m_pLastGroup;};
	CServer(IN SODaCEntry *parent);
	virtual	~CServer();
	CGroup**			m_GroupArray;		// pointer to last added group
	unsigned long		m_GroupCount;

protected:
	SODaCEntry *		m_Parent;
	void onSetObjectState(void);
private:
	CGroup* m_pLastGroup;
};

#endif // !defined(AFX_SERVER_H__0375C68A_14B5_4056_B29E_CE6C93B5CF99__INCLUDED_)
