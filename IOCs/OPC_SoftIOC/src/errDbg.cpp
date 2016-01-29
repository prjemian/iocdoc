#include "stdafx.h"
#include <sys/timeb.h>
#include "time.h"
#include "errDbg.h"

int dbg_level = 0;
char szDbgMessage[256] = {NULL};

int CheckType(int iActualType)
{
	if(((iActualType == airval) || (iActualType == aival)) && ((dbg_level & DBG_AI_AIR) == DBG_AI_AIR))
		return 1;
	if((iActualType == aaival) && ((dbg_level & DBG_AAI) == DBG_AAI))
		return 1;
	if(((iActualType == birval) || (iActualType == bival)) && ((dbg_level & DBG_BI_BIR) == DBG_BI_BIR))	
		return 1;
	if((iActualType == longinval) && ((dbg_level & DBG_LONGIN) == DBG_LONGIN))	
		return 1;
	if(((iActualType == mbbirval) || (iActualType == mbbival)) && ((dbg_level & DBG_MBBI_MBBIR) == DBG_MBBI_MBBIR))	
		return 1;
	if(((iActualType == mbbiDirectrval) || (iActualType == mbbiDirectval)) && ((dbg_level & DBG_MBBIDIRECT_MBBIDIRECTR) == DBG_MBBIDIRECT_MBBIDIRECTR))	
		return 1;
	if((iActualType == stringinval) && ((dbg_level & DBG_STRINGIN) == DBG_STRINGIN))	
		return 1;
	if((iActualType == eventval) && ((dbg_level & DBG_EVENTVAL) == DBG_EVENTVAL))	
		return 1;
	if((iActualType == histogramval) && ((dbg_level & DBG_HISTOGRAMVAL) == DBG_HISTOGRAMVAL))	
		return 1;
	if(((iActualType == aorval) || (iActualType == aoval)) && ((dbg_level & DBG_AO_AOR) == DBG_AO_AOR))	
		return 1;
	if((iActualType == aaoval) && ((dbg_level & DBG_AAO) == DBG_AAO))	
		return 1;
	if(((iActualType == borval) || (iActualType == boval)) && ((dbg_level & DBG_BO_BOR) == DBG_BO_BOR))	
		return 1;
	if((iActualType == longoutval) && ((dbg_level & DBG_LONGOUT) == DBG_LONGOUT))	
		return 1;
	if(((iActualType == mbborval) || (iActualType == mbboval)) && ((dbg_level & DBG_MBBO_MBBOR) == DBG_MBBO_MBBOR))	
		return 1;
	if(((iActualType == mbboDirectval) || (iActualType == mbboDirectrval)) && ((dbg_level & DBG_MBBODIRECT_MBBIDORECTR) == DBG_MBBODIRECT_MBBIDORECTR))	
		return 1;
	if((iActualType == stringoutval) && ((dbg_level & DBG_STRINGOUT) == DBG_STRINGOUT))	
		return 1;
	if((iActualType == waveformval) && ((dbg_level & DBG_WAVEFORMAL) == DBG_WAVEFORMAL))	
		return 1;
	return 0;
}

void dbgPrintf(int iLevel, int iActualType)
{
	if(iLevel & dbg_level)
	{
		HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
		if(dbg_level & DBG_COLORED)
			SetConsoleTextAttribute ( hOut, iLevel | 49 | FOREGROUND_INTENSITY);
		struct _timeb timebuffer;
		char *timeline;
		_ftime( &timebuffer );
		timeline = ctime( & ( timebuffer.time ) );
		if ( (dbg_level & (DBG_COLORED-1)) < DBG_AI_AIR)
		{
			printf( "%.19s.%hu\t# ", timeline, timebuffer.millitm);
			printf("%s\n",szDbgMessage);
		}
		else
		{															
			if(CheckType(iActualType))
			{
				printf( "%.19s.%hu\t# ", timeline, timebuffer.millitm);
				printf("%s\n",szDbgMessage);
			}
		}
		if(dbg_level & DBG_COLORED)
			SetConsoleTextAttribute ( hOut,FOREGROUND_RED | FOREGROUND_GREEN |
									FOREGROUND_BLUE | FOREGROUND_INTENSITY);
	}
}

