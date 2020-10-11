#ifndef __POINT_H__
#define __POINT_H__

#include <iostream>
#include <cmath>
using namespace std;

class Point
{
	int x, y;			  //  점의 x와 y 좌표 값
	friend class Monster; //  Monster를 친구 클래스로 등록
	friend class Canvas;  //  Canvas를 친구 클래스로 등록
public:
	Point(int xx = 0, int yy = 0) : x(xx), y(yy) {}
	int &operator[](int id)
	{ // 인덱스 연산자
		if (id == 0)
			return x;
		else if (id == 1)
			return y;
		else
			exit(0);
	}

	// sqrt는 제곱근을 뜻한다. 거리를 구할때 사용하면 좋을 것 같다.
	operator double() { return sqrt((double)x * x + y * y); }

	// Point 의 값이 0보다 작거나 최대값을 넘지 않도록 해주는 () 연산자
	void operator()(int maxx, int maxy)
	{
		if (x < 0)
			x = 0;
		if (x >= maxx)
			x = maxx - 1;
		if (y < 0)
			y = 0;
		if (y >= maxy)
			y = maxy - 1;
	}
	Point operator-() { return Point(-x, -y); }
	bool operator==(const Point &p) { return x == p.x && y == p.y; }
	bool operator!=(const Point &p) { return x != p.x || y != p.y; }
	Point operator-(const Point &p) { return Point(x - p.x, y - p.y); }
	Point operator+(const Point &p) { return Point(x + p.x, y + p.y); }
	void operator+=(const Point &p) { x += p.x, y += p.y; }
	void operator-=(const Point &p) { x -= p.x, y -= p.y; }
};

#endif
