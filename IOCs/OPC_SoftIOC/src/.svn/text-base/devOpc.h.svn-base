/*****************************************************************************
File:	$CVSROOT/support/opcApp/src/devOpc.h

Project:        Device support for OPC

Description:    

Author:         Bernhard Kuner

Version:        $Revision: 1.6 $

History:

  $Log: devOpc.h,v $
  Revision 1.6  2003/12/11 12:49:04  kuner
  Array Access added, outsource console functions to opcConsoleCmd.cpp

  Revision 1.5  2003/07/16 17:09:52  kuner
  Adapted to base3.14.2, new io report function: opcIor, use iocLogClient for error logging

  Revision 1.4  2003/03/03 14:05:59  kuner
  struct OpcToEpics: new member: shft, records shift value


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
#ifndef INCdevOpcH
#define INCdevOpcH

#include <ks.h>
#include "aitTypes.h"
#include "dbScan.h"
#include "callback.h"

/*This record type enums are used as index for every supported record in RecPropStruct*/
typedef enum {	aaival,	aaoval,aival,aoval,bival,boval,eventval,histogramval,
				longinval,longoutval,mbbival,mbboval,mbbiDirectval,mbboDirectval,  
				stringinval,stringoutval,waveformval,airval,aorval,birval,borval,
				mbbiDirectrval,mbboDirectrval,mbbirval,mbborval
  			 } RecTypeEnum;
    
typedef struct {	/* set relevant properties of a record type */
		aitEnum valAitType;	/* data type of records val/rval field */
				/* aitEnumInvalid type signals an array. Take type/len from record */ 	
		aitInt32 cnt;	/* Array length: 1=scalar value, 0=array - see nelm for length, fixed for strings according to the record */
		long ret;	/* return value for read_io functions 0=default, 2=don't convert */
		char *record;	/* Record type string */
		} RecPropStruct;
/* This global array contains record attributes, defined in devOpc.c */
    
#ifdef __cplusplus
extern "C" {
#endif
extern RecPropStruct recProp[];
#ifdef __cplusplus
}   
#endif

/* Records private struct rec->dpvt to connect epics device support devOpc.c 
	and opc in drvOpc.cpp */
typedef struct OTE 
{ void *pOpcItem;		/* point to the opc object */
  struct dbCommon *pRecord; /* give opc callback a chance to access the record */
  RecTypeEnum recType;	/* enum used as index to record relevant definitions */

/* Need this because it is record dependant and not defined in dbCommon */
  void *pRecVal;		/* point to records val field */
  /* used in mbb..Records */
  aitUint32 mask;   /* init_record can set here the shifted mask according to NOBT and SHFT */
  aitUint32 shft;   /* init_record can set here the shift according to SHFT */

  /* used in aa..Records */
  aitUint32 nelm;   /* init_record can set here the number of elements for an array according to NELM*/
  aitUint32 *nord;	/*Number elements read*/


/*	Problem: in-records (ai, bi...) use common scan mechanism. For SCAN=IOINTR
	the COpcItem::onSetReadValue() function puts the new value to the .VAL field 
	and	causes the record to be processed by scanIoRequest(). Also all other 
	possibilities of SCAN will work correct. 
	For out records this way doesn't work. Actually out records are now InOut-records!
	and SCAN is allways set to 'passive'. Here the only way is to cause processing by 
	the callback mechanism and prevent that new values read by the opc library are 
	written back to the opc server. Otherwise it would cause a infinite loop!
*/
  int isCallback;		/* is IN-record with SCAN=IOINTR or any type of OUT record*/
  int isOutRecord;
  int noOut;            /* flag for OUT-records: prevent write back of incomming values */
  IOSCANPVT ioscanpvt;	/* in-records scan request.*/
  CALLBACK callback;	/* out-records callback request.*/
} OpcToEpics;

#endif /*INCdevOpcH*/

