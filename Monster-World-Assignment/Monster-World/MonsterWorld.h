#ifndef __WORLD_H__
#define __WORLD_H__

#include "Canvas.h"
#include "VariousMonsters.h"
#include "Human.h"
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

#include <algorithm> // STL의 알고리즘 사용
inline bool compare(Monster *first, Monster *second)
{
  return first->nItem > second->nItem;
}

class MonsterWorld
{
  vector<vector<int> > world;
  int xMax, yMax, nMove;
  vector<Monster *> pMon;
  Canvas canvas;

  int &Map(int x, int y) { return world[y][x]; }
  bool isDone() { return countItems() == 0; }
  int countItems()
  {
    int nItems = 0;
    for (int y = 0; y < yMax; y++)
      nItems += count(world[y].begin(), world[y].end(), 1);
    return nItems;
  }
  void print()
  {
    canvas.clear();
    for (int y = 0; y < yMax; y++)
      for (int x = 0; x < xMax; x++)
        if (Map(x, y) > 0)
          canvas.draw(x, y, ".");
    for (int i = 0; i < pMon.size(); i++)
      pMon[i]->draw(canvas);
    canvas.print("[ Monster World ]");

    cerr << " Total Move Count = " << nMove << endl;
    cerr << " Rest Items Count = " << countItems() << endl
         << endl;

    // 몬스터들은 아이템 획득 숫자에 따라 정렬 된다.
    sort(pMon.begin(), pMon.end(), compare);
    for (int i = 0; i < pMon.size(); i++)
    {
      cout << "  Rank " << i + 1;
      pMon[i]->print();
    }
  }

public:
  // 게임을 초기화 한다. 지도의 모든 칸에 아이템을 놓습니다.
  // 지도의 값이 1이면 아이템이 있고 0 이면 아이템이 없다는 뜻 이다.
  MonsterWorld(int w, int h) : world(h), canvas(w, h), xMax(w), yMax(h)
  {
    nMove = 0;
    for (int y = 0; y < yMax; y++)
    {
      world[y] = vector<int>(w, 1);
    }
  }
  // 추가 된 모든 몬스터 (인간 포함)의 메모리를 해제한다.
  ~MonsterWorld()
  {
    for (int i = 0; i < pMon.size(); i++)
      delete pMon[i];
  }
  void add(Monster *m)
  {
    pMon.push_back(m);
  }

  // 게임을 플레이 한다. 지도상의 모든 아이템이 없어지거나, 최대 이동 횟수가 끝나고 나면 게임이 종료 된다.
  void play(int maxwalk, int wait)
  {
    print();
    cerr << endl
         << " Press [ENTER] key...";
    getchar();
    // 몬스터들은 매 이동턴마다 이동을 수행한다.
    // 저장 된 순서대로 이동을 하고 이동 할 때마다 아이템을 획득한다.
    // 아이템 획득 수에 따라 결국 한 위치에 여러 몬스터가 도착 하더라도 순위가 높은 몬스터가 아이템을 획득하게 된다.
    for (int i = 0; i < maxwalk; i++)
    {
      for (int k = 0; k < pMon.size(); k++)
        pMon[k]->move(world, xMax, yMax);

      nMove++;
      print();
      if (isDone())
        break;

// 사용자의 프로그램 환경에 따라 적절한 sleep 명령을 호출합니다.
// 일정 주기로 매 이동 턴을 카운트 하기 위한 로직이다.
#ifdef _WIN32
      Sleep(wait);
#else
      usleep(wait);
#endif
    }
  }
};

#endif