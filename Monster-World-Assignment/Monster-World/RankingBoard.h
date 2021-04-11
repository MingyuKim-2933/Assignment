#ifndef __RANKING_BOARD_H__
#define __RANKING_BOARD_H__

#include <iostream>
#include <fstream>
#include "FileException.h"
using namespace std;
#define NUM_MVP 5 // 최대 랭킹 기록 수

struct PlayInfo
{						// 게임 정보 클래스
	string name;		// 게이머의 이름
	int nItem;			// 획득한 아이템의 수
	double itemPerMove; // 이동 거리당 아이템 수
	PlayInfo(string na = "NewPlayer", int ni = 0, double ipm = 0.0) // 등록 기록이 없을 경우의 초기 값을 입력
		: name(na), nItem(ni), itemPerMove(ipm) {}
};

class RankingBoard
{ // 랭킹 관리 클래스
	string filename;
	PlayInfo MVP[NUM_MVP];
	int nMVP = NUM_MVP;

public:
	RankingBoard(string filename) : filename(filename) {}

	// 주어진 파일의 데이터를 읽어온다. 파일이 없는 경우 예외 처리를 한다.
	void load()
	{
		ifstream is;		
		int idx = 0;

		is.open(filename);
		
		if (is.is_open())
		{
			while (!is.eof())
			{
				string name;
				int nItem;
				double itemPerMove;

				is >> name >>  nItem >> itemPerMove;
				MVP[idx++] = PlayInfo(name, nItem, itemPerMove);
			}
		}
		else
		{
			throw FileException(filename, false);
		}
	}

	// 랭킹 리스트를 저장한다.
	void store()
	{
		ofstream os;
		os.open(filename);

		for (int i = 0; i < nMVP; i++)
		{
			PlayInfo playInfo = MVP[i];
			os << playInfo.name << " "
				<< playInfo.nItem << " "
				<< playInfo.itemPerMove;
		}

		os.close();
	}

	// 랭킹 리스트를 1위부터 순서대로 출력한다.
	void print(string title = "Game Ranking")
	{
		cout << endl << "" << title << endl << endl;

		sort(MVP, MVP + nMVP, [](PlayInfo l, PlayInfo r) -> bool{
			return l.nItem > r.nItem;
		});

		for (int i = 0; i < nMVP; i++)
		{
			PlayInfo playInfo = MVP[i];

			cout << "[Rank " << i + 1 << "]"
				<< playInfo.name << "\t"
				<< playInfo.nItem << "\t"
				<< playInfo.itemPerMove << endl;
		}

		cout << endl;

		cout << "Press [Enter] Key" << endl;
		getchar();
	}

	// 게임이 끝난 후 플레이어의 기록을 입력한다.
	// nItem : 아이템 획득 수, ipm : 이동거리당 아이템 획득 비율 (아이템 획득 수 / 총 이동 거리)
	// 입력시 현재 기록과 비교하여 5위 이내인 경우 기록을 위한 이름을 받는다.
	void add(int nItem, double ipm)
	{
		bool isRank = false;
		int idx = -1;

		for (int i = 0; i < nMVP; i++)
		{
			PlayInfo playInfo = MVP[i];

			if (nItem > playInfo.nItem)
			{
				isRank = true;
				idx = i;
				break;
			}
		}

		if (isRank)
		{
			string name;
			cout << "[Rank " << idx + 1 << "] Insert Name: ";
			cin >> name;

			for (int i = nMVP - 1; i > idx; i--)
			{
				MVP[i] = MVP[i - 1];
			}

			MVP[idx] = PlayInfo(name, nItem, ipm);
		}
	}
};

#endif