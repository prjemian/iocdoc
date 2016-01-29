/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/Creator.cpp

Project:        OPC creator class

Description:    Object factory for toolkit objects
				Contents one toolkit session and creates several OPC servers

Author:         Winkler

Version:        $Revision: 0.9 $

History:

  $Log: Creator.cpp,v $


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

// Creator.cpp: Implementation of CCreator class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "Server.h"
#include "Group.h"
#include "Item.h"
#include "Creator.h"
char * CreatorId =
"Creator.cpp: $Revision: 0.9 $\n";

CCreator::CCreator()
{
}

CCreator::~CCreator()
{
}

SODaCServer* CCreator::createServer(SODaCEntry *parent)
{
	return new CServer(parent);
}

SODaCGroup* CCreator::createGroup(SODaCServer *parent)
{
	return new CGroup((CServer*)parent);
}

SODaCItem* CCreator::createItem(SODaCGroup *parent)
{
	return new CItem((CGroup*)parent);
}
