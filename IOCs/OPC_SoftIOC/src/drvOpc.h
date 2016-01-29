/*****************************************************************************
File:	$CVSROOT/support/opcApp/src/drvOpc.h

Project:        Device support for OPC

Description:    

Author:         Bernhard Kuner

Version:        $Revision: 1.6 $

History:

  $Log: drvOpc.h,v $
  Revision 1.6  2003/12/12 07:09:45  kuner
  minor bugfix

  Revision 1.5  2003/12/11 12:49:05  kuner
  Array Access added, outsource console functions to opcConsoleCmd.cpp

  Revision 1.4  2003/07/16 17:09:53  kuner
  Adapted to base3.14.2, new io report function: opcIor, use iocLogClient for error logging

  Revision 1.3  2003/03/03 14:08:25  kuner
  no real changes


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
#ifndef INCdrvOpcH
#define INCdrvOpcH

#include "devOpc.h"
/* export functions for devOpc.c */
#ifdef __cplusplus
extern "C" {
#endif
extern long opcGetScalar(OpcToEpics *);
extern long opcSetScalar(OpcToEpics *);
extern long opcCreateItem(OpcToEpics *, char *opcName, dbCommon *prec);
extern long opcCreateServer( void );
extern long opcStartServer( void );
extern long ft2epics(FILETIME *ft, epicsTimeStamp *et);

#ifdef __cplusplus
}

/* Fast conversion of ait types to variant types */
#define AIT_MAX aitEnumContainer+1	/* ait types defined in <base>/include/aitTypes.h */

#include <map>
#include <string>
using std::string;
using std::map;
#include "Creator.h"
#include "Item.h"
/*
// classes needed by opcSonsoleCmd.cpp //
class COpcCreator : public SODaCCreator
{
public:
    COpcCreator(){};
	// Override item creation 
	virtual SODaCItem* createItem(IN SODaCGroup *parent);

protected:
    virtual ~COpcCreator(){};
};

class COpcItem : public SODaCItemDefault
{
public:
    friend long opcGetArray(OpcToEpics * );
    friend long opcGetScalar(OpcToEpics *);
    friend long opcSetScalar(OpcToEpics *);
	COpcItem(void){};
    int isBad() {
		int wegdamit = getReadQuality();
		return (getReadQuality() == 192)?0:1;}
	void setRec(OpcToEpics *opcEpics) { pOpc2Epics = opcEpics; }
    OpcToEpics *pOpc2Epics;
	
protected:
	virtual void onSetReadValue(void);
// Start of Test 03/09/2003
//	virtual void onSetReadQuality(void);
//	virtual void onSetReadTimeStamp(void);
// End of Test 03/09/2003

};
*/
typedef std::map<std::string, std::string> NameMap;

/* globals needed by opcSonsoleCmd.cpp */
extern enum VARENUM ait2vtTable[AIT_MAX];	/* variant types defined in <MSVC>/VC98/Include/KS.H */
extern SOCmnPointer<SODaCEntry>    pEntry;
extern SOCmnPointer<SODaCServer> m_pServer;
extern SOCmnPointer<SODaCGroup> m_pGroup;
extern SOCmnList<CLSID> clsidList;     // Class Id list: List of servers
extern opcStartServerFlag;
extern opcCreateGroupFlag;
extern opcCreateServerFlag;
extern NameMap nameMap;

#endif	/*__cplusplus*/

#endif /*INCdrvOpcH*/