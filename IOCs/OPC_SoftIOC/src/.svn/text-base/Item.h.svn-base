/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Item.h

Project:        OPC item class

Description:    Contents one OPC item and interface to epics PV

Author:         Winkler

Version:        $Revision: 1.0 $

History:

  $Log: Item.h,v $
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

// Item.h: interface for CItem class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_ITEM_H__6480F798_5F26_445C_8742_0E35B09C7C01__INCLUDED_)
#define AFX_ITEM_H__6480F798_5F26_445C_8742_0E35B09C7C01__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

extern int dbg_level;
#include "errDbg.h"
#include "dbCommon.h"
#include "menuAlarmStat.h"
#include "menuAlarmSevr.h"
class CGroup;
#ifdef __cplusplus
extern "C" {
#endif
extern long ft2epics(FILETIME *ft, epicsTimeStamp *et);
#ifdef __cplusplus
}
#endif

class CItem : public SODaCItemDefault  
{
public:
    friend long opcGetArray(OpcToEpics *);
    friend long opcGetScalar(OpcToEpics *);
    friend long opcSetScalar(OpcToEpics *);
	CItem(IN CGroup* parent);
	virtual ~CItem();
    int isBad() {return (getReadQuality() == 192)?0:1;}
	void setRec(OTE *opcEpics);
	SOCmnString m_soItemID;
	string m_sPvName;
protected:
    OTE *pOpc2Epics;
	CItem* pOpcInterface;
	dbCommon* pEpicsInterface;
	BOOL bInitialized;
	virtual void onSetReadValue(void);
	CGroup *m_Parent;
};

#endif // !defined(AFX_ITEM_H__6480F798_5F26_445C_8742_0E35B09C7C01__INCLUDED_)
