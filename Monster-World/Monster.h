#ifndef __MONSTER_H__
#define __MONSTER_H__

#include "Canvas.h"
#include "Point.h"

class Monster
{
public:
	string name, icon; // 몬스터 이름과 화면 출력용 아이콘
	int nItem;         // 먹은 아이템 수
	Point q, p;        // 이전 위치(q)와 현재 위치(p)
	int nSleep;        // 쉬어야 하는 횟수
	double dist;       // 쉬고 난 다음 움직인 거리
	double total;      // 총 움직인 거리

	// 이동이 화면을 벗어나는 경우 이동 처리를 막아준다
	// hint : Point에 () 연산자가 존재한다
	void clip(int maxx, int maxy)
	{
		p(maxx, maxy);
	}

	// 자신의 위치에 아이템이 있는경우 습득을 할 수 있음.
	// 지도의 좌표에 있는 값이 1인경우 아이템 있음, 0 인경우 없음이다.
	// 이곳에서 아이템 획득 여부와 거리 계산, 휴식 여부를 수행한다.
	// 플레이어의 경우 휴식을 하지 않는다.
	void eat(vector<vector<int> >& map, bool isMonster = true)
	{
		if (dist > 20)
		{
			dist = 0;

			if (isMonster)
			{
				nSleep = 10;
			}
		}

		int x = p.x;
		int y = p.y;

		if (map[y][x] == 1)
		{
			map[y][x] = 0;
			nItem++;
			
			if (isMonster)
			{
				nSleep++;
			}
		}
	}

public:
	Monster(string n = "Monster", string i = "M", int x = 0, int y = 0)
		: name(n), icon(i), nItem(0),
		p(x, y), q(x, y), nSleep(0), dist(0.0), total(0.0) {}
	virtual ~Monster() {
		cout << " " << icon << "\t"
			<< "Item:" << nItem << "\t\t"
			<< "Distance:" << total << endl;
	}

	void draw(Canvas& canvas) { canvas.draw(p, icon); }

	// 몬스터의 경우는 거리를 20 이상 이동하고 나면 10번의 이동턴 동안 쉬어야 한다.
	// 몬스터는 매 이동 턴 마다 대각선, 가로, 세로, 제자리 이렇게 총 9가지 이동중 한가지 이동을 하는 것을 기본 동작으로 한다.
	// 기본 몬스터의 이동 거리는 매턴당 최대 1칸이다.
	virtual void move(vector<vector<int> >& map, int maxx, int maxy)
	{
		if (nSleep > 0)
		{
			nSleep--;
			return;
		}

		int dir = rand() % 9;
		int dx = 0;
		int dy = 0;

		switch (dir)
		{
		case 0: dx = -1; dy = -1; break;
		case 1: dy = -1; break;
		case 2: dx = 1; dy = -1; break;
		case 3: dx = -1; break;
		case 4: break;
		case 5: dx = 1; break;
		case 6: dx = -1; dy = 1; break;
		case 7: dy = 1; break;
		case 8: dx = 1; dy = 1; break;
		}

		Point vector(dx, dy);
		q = p;
		p = p + vector;

		clip(maxx, maxy);

		dist++;
		total++;

		eat(map, true);
	}
	void print() { cout << "\t" << name << " " << icon << "\t" << nItem << "\t" << nSleep << endl; }
};

#endif