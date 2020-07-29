#ifndef __CANVAS_H__
#define __CANVAS_H__

#include <iostream>
#include <string>
#include "Point.h" // Point 사용을 위해 추가
#include <vector>
using namespace std;

#ifdef _WIN32
const char *COMMAND = "cls";
#else
const char *COMMAND = "clear";
#endif

// 화면을 출력 하기 전 메모리 Canvas
class Canvas
{
  vector<string> line; // 화면 출력을 위한 벡터 객체
  int xMax, yMax;

public:
  // 화면의 크기를 세팅하고 공백으로 초기화 한다.
  Canvas(int nx = 10, int ny = 10) : line(ny), xMax(nx), yMax(ny)
  {
    for (int y = 0; y < yMax; y++)
      line[y] = string(xMax, ' ');
  }

  // 주어진 x, y 좌표에 val 을 그려준다
  void draw(int x, int y, string val)
  {
    if (x >= 0 && y >= 0 && x < xMax && y < yMax)
      line[y].replace(x, 1, val);
  }

  // 주어진 Point 좌표에 val 을 그려준다
  void draw(Point &p, string val) { draw(p.x, p.y, val); }

  // Canvas 전체를 공백으로 초기화 해준다 (Canvas에 그려진 그림을 지운다)
  void clear(string val = " ")
  {
    for (int y = 0; y < yMax; y++)
      for (int x = 0; x < xMax; x++)
        draw(x, y, val);
  }

  // 현재 화면을 지우고 title 과 함께 현재 Canvas 를 화면에 출력한다
  void print(const char *title = "<My Canvas>")
  {
    system(COMMAND);
    cout << title << endl;
    for (int y = 0; y < yMax; y++)
      cout << line[y] << endl;
    cout << endl;
  }
};

#endif