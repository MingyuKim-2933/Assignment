#include "MonsterWorld.h"
#include "Human.h"
#include "RankingBoard.h"
#include <time.h>

// 랭킹 보드의 정보를 불러온다.
void initRankingBoard(RankingBoard &rank)
{
	try
	{
    cout << "Loading Ranking Board..." << endl;
		rank.load();
	}
	catch (FileException e)
	{
		string passwd, correct = "1234";
		cout << "Password: ";
    cin >> passwd;

		if (passwd != correct)
		{
			cout << "Incorrect password. Quit game.\n\n";
			exit(0);
		}
		// 비밀 번호가 맞으면 기본 랭킹으로 게임을 계속 진행함.
	}
	rank.print("[Game Ranking: START]");
}

// 지도의 임의 위치에 몬스터와 플레이어를 배치한다.
Human *initGame(MonsterWorld &game, int width, int height)
{
	srand((unsigned int)time(NULL));

	game.add(new Zombie("Zombie", "Z", rand() % width, rand() % height));
	game.add(new Vampire("Vampire", "V", rand() % width, rand() % height));
	game.add(new KGhost("KGhost", "G", rand() % width, rand() % height));
	game.add(new Jiangshi("Jiangshi1", "A", rand() % width, rand() % height, true));
	game.add(new Jiangshi("Jiangshi2", "B", rand() % width, rand() % height, false));

	Human *human = new Human("Player", "H", rand() % width, rand() % height);
	game.add(human);
	return human;
}

// 게임이 종료 한 후 랭킹 보드 갱신 및 저장을 수행 한다.
void handleScore(RankingBoard &rank, Human *human)
{
	rank.add(human->nItem, human->nItem / human->total);
	rank.print("[Game Ranking: FINISH]");
	rank.store();
}

int main()
{
	RankingBoard rank("MonsterWorld.rnk");
	initRankingBoard(rank);

	int width = 32, height = 10;
	MonsterWorld game(width, height);
	Human *human = initGame(game, width, height);

#ifndef _WIN32
  init_keyboard();
#endif
	game.play(500, 10);
#ifndef _WIN32
  close_keyboard();
#endif
	printf("\n------------------- Game Finish -------------------\n");

	handleScore(rank, human);

	return 0;
}