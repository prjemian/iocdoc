/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Item.cpp

Project:        OPC item class

Description:    Contents one OPC item and interface to epics PV

Author:         Winkler

Version:        $Revision: 1.0 $

History:

  $Log: Item.cpp,v $
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

// Item.cpp: Implementation of CItem class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "Item.h"
char * ItemId =
"Item.cpp: $Revision: 1.00 $\n";
extern int dbg_level;

CItem::CItem(IN CGroup* parent)
{
	static unsigned long ulCounter = 0;
	if(!(dbg_level & 32))
		printf("%5lu variables connected to OPC server\x0D",++ulCounter);
	m_Parent        = parent;
	pOpc2Epics      = NULL;
	pEpicsInterface = NULL;
	pOpcInterface   = NULL;
	bInitialized    = FALSE;
}

CItem::~CItem()
{
}

void CItem::setRec(OTE *opcEpics)
{
	pOpc2Epics = opcEpics;
	pOpc2Epics->pOpcItem = this;
	bInitialized = (opcEpics && opcEpics->pRecord && opcEpics->pOpcItem);
	if(bInitialized)	// avoid invalid pointers
	{
		pEpicsInterface = pOpc2Epics->pRecord;
		pOpcInterface = (CItem*) pOpc2Epics->pOpcItem;
	}
}

/*
void CItem::onSetReadValue()
{
   // look at drvOpc.cpp !!!
}
*/