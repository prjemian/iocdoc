/*****************************************************************************
File:    $CVSROOT/support/opcApp/src/iocShellMain.cpp

Project:        Device support for OPC

Description:    The ioc shell

Author:         Kuner, Winkler

Version:        $Revision: 1.9 $

History:

  $Log: iocShellMain.cpp,v $
  Revision 1.9  2003/07/18 11:51:08  kuner
  iocShellMain.cpp

  Revision 1.8  2003/07/16 17:12:09  kuner
  *** empty log message ***

  Revision 1.7  2003/07/16 17:09:53  kuner
  Adapted to base3.14.2, new io report function: opcIor, use iocLogClient for error logging

  Revision 1.5  2003/03/18 12:08:00  kuner
  add cvs id variables and print it by showVersion()

  Revision 1.4  2003/03/18 11:53:38  kuner
  Logfiles added by Winkler

  

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
char *iocShellMainId=
"iocShellMain: $Revision: 1.9 $\n";
#include <stddef.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <signal.h>
#include <windows.h>
#include <winbase.h>
#include "epicsThread.h"
#include "iocsh.h"
#include "logClient.h"
#include "errDbg.h"

extern long opcInit( void );

void  INThandler(int sig);
int main(int argc,char *argv[])
{
    HANDLE hOut;
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    GetConsoleScreenBufferInfo(hOut, &csbi);
	csbi.dwSize.X = 120;
	csbi.dwSize.Y = 32767;
	SetConsoleScreenBufferSize(hOut, csbi.dwSize);
	SetConsoleTextAttribute ( hOut,
                      FOREGROUND_RED |
                        FOREGROUND_GREEN |
                        FOREGROUND_BLUE |
                        FOREGROUND_INTENSITY );
	char txt[]="************************* O P C - I O C - S H E L L ***********************";
	printf("\n%s\n\n",txt);
	iocLogInit();
	opcInit();

	signal(SIGINT,  INThandler);   // exit with disconnect via CTRL-C
	signal(SIGABRT, INThandler);
	signal(SIGTERM, INThandler);
	signal(SIGILL,  INThandler);
	signal(SIGFPE,  INThandler);
	signal(SIGSEGV ,INThandler);
	signal(SIGBREAK,INThandler);

	// start ioc-shell
	if(argc>=2)
	{   
		iocsh(argv[1]);
		epicsThreadSleep(.2);
	}

	iocsh(NULL);
	return(0);
}
