/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Group.h

Project:        OPC group class

Description:    Contents one OPC group and creates several OPC items

Author:         Winkler

Version:        $Revision: 0.9 $

History:

  $Log: Group.h,v $


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

// Group.h: interface for CGroup class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_GROUP_H__B30CA9CB_ED1D_4EA1_975A_200871F97AC3__INCLUDED_)
#define AFX_GROUP_H__B30CA9CB_ED1D_4EA1_975A_200871F97AC3__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

class CServer;
class CItem;

class CGroup : public SODaCGroupDefault  
{
public:
	void SetRefreshTimer(int iRefreshTime);
	unsigned long m_ulTime;
	BOOL AddItem(LPCTSTR szItemID, LPCTSTR szPvName);
	CGroup(IN CServer* parent);
	virtual ~CGroup();
	CItem**	m_ItemArray;			// pointer to item array of this group
	unsigned long m_ItemCount;
	string m_sGroupName;

private:
	static void RefreshTimer(void* param);
	unsigned long m_hRefreshTimer;
	int m_iRefreshTime;
	CServer *m_Parent;
};

#endif // !defined(AFX_GROUP_H__B30CA9CB_ED1D_4EA1_975A_200871F97AC3__INCLUDED_)
