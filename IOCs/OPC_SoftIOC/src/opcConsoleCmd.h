/*****************************************************************************
File:   $CVSROOT/support/opcApp/src/opcConsoleCmd.h

Project:        Device support for OPC

Description:    opc related console commands for the iocShell

Author:         Bernhard Kuner

Version:        $Revision: 1.1 $

History:

  $Log: opcConsoleCmd.h,v $
  Revision 1.1  2003/12/11 12:49:04  kuner
  Array Access added, outsource console functions to opcConsoleCmd.cpp


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
#ifndef INCopcConsoleCmdH
#define INCopcConsoleCmdH

extern int opcNameTranslationFlag;
struct IorItem	// public class with information to an opcItem used for report function opcIor
{ 
	std::string epicsName;
	std::string opcName;
	std::string opcFullName;
	IorItem(char *enam, char *onam) {	epicsName=enam;	opcName=onam; };
	void dumpItem(void);
};

typedef std::vector<IorItem *> IorItemVec;	// store item information for opcIor routine
extern IorItemVec iorItems;

#endif /*INCopcConsoleCmdH*/
