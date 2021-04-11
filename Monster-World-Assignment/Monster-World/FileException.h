#ifndef __EXCEPTION_H__
#define __EXCEPTION_H__

#include <string>
class FileException
{					 // 파일 예외 클래스
	string filename; // 파일 이름
	bool bRead;		 // 파일 모드

public:
	FileException(string name, bool b) : filename(name), bRead(b) {}
};

#endif