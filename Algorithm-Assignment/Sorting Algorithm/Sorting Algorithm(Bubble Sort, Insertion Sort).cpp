#include <iostream>
#include <vector>
#include <chrono>
#include <map>
#include <string>

using namespace std;
using namespace chrono;

//정렬할 때 사용되는 Swap
void Swap(map<int, vector<string>>& map, int a, int b) {
	map[1000] = map[a];
	map[a] = map[b];
	map[b] = map[1000];
}

//Bubble Sort
void BubbleSort(int input, map<int, vector<string>>&map) {
	for (int i = 0; i < map.size()-1; i++) {
		for (int j = 0; j < map.size() - i - 2; j++) {
			if (map[j][input].compare(map[j + 1][input]) > 0) {
				Swap(map, j, j + 1);
			}				
		}
	}
}

//Insertion Sort
void InsertionSort(int input, map<int, vector<string>>& map) {
	int j = 0;
	for (int i = 1; i < map.size()-2; i++) {
		j = i;
		while (j >= 0 && map[j][input].compare(map[j + 1][input]) > 0) {
			Swap(map, j, j + 1);
			j--;
		}
	}
}

//정렬
void Sort(map<int, vector<string>>& map) {
	int choice;
	int input;
	cout << "정렬 항목을 선택하시오" << endl;
	cout << "1. 노래 2. 가수 3. 앨범" << endl;
	while (true) {
		cout << "->";
		cin >> input;
		if (input >= 1 && input <= 3) {
			break;
		}
		cout << "잘못 입력하셨습니다. 재입력 해주세요" << endl;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(1000, '\n');
		}
	}
	input -= 1;
	cout << "정렬 알고리즘을 선택하시오" << endl;
	cout << "1. Bubble Sort 2. InsertionSort" << endl;
	while (true) {
		cout << "->";
		cin >> choice;
		if (choice >= 1 && choice <= 2) {
			break;
		}
		cout << "잘못 입력하셨습니다. 재입력 해주세요" << endl;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(1000, '\n');
		}
	}
	high_resolution_clock::time_point start = high_resolution_clock::now();
	if (choice == 1) BubbleSort(input, map);
	if (choice == 2) InsertionSort(input, map);
	high_resolution_clock::time_point end = high_resolution_clock::now();
	auto time = duration_cast<nanoseconds>(end - start).count();
	cout << "정렬이 완료되었습니다." << endl;
	cout << "실행시간(seconds):" << time / 1000000000.0 << endl;
}

//입력
void Insert(map<int, vector<string>>& map) {
	int n = map.size()-1;
	string name;
	string singer;
	string album;
	cout << "팝송의 제목을 입력하시오 :" << endl;
	cout << "->";
	cin.ignore();
	getline(cin, name);
	cout << name <<"을 부른 가수를 입력하시오 :" << endl;
	cout << "->";
	getline(cin, singer);
	cout << name <<"의 앨범 이름을 입력하시오 :" << endl;
	cout << "->";

	getline(cin, album);
	high_resolution_clock::time_point start = high_resolution_clock::now();
	map.insert(pair<int, vector<string>>(n, { name, singer, album }));
	high_resolution_clock::time_point end = high_resolution_clock::now();
	auto time = duration_cast<nanoseconds>(end - start).count();
	cout << "입력이 완료되었습니다." << endl;
	cout << "실행시간(seconds):" << time / 1000000000.0 << endl;
}

//삭제 
void Delete(map<int, vector<string>>& map) {
	int delete_num =0;
	cout << "삭제할 음악의 번호를 입력하시오 :" << endl;
	while (true) {
		cout << "->";
		cin >> delete_num;
		if (delete_num >= 0 && delete_num <= map.size()-2) {
			break;
		}
		cout << "잘못 입력하셨습니다. 재입력 해주세요" << endl;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(1000, '\n');
		}
	}
	high_resolution_clock::time_point start = high_resolution_clock::now();
	if (delete_num != map.size() - 3) map.erase(delete_num);
	for (int i = delete_num; i < map.size() - 2; i++) {
		map[i] = map[i + 1];
	}
	if(delete_num !=map.size()-1) map.erase(map.size() - 2);
	high_resolution_clock::time_point end = high_resolution_clock::now();
	auto time = duration_cast<nanoseconds>(end - start).count();
	cout << "삭제가 완료되었습니다." << endl;
	cout << "실행시간(seconds):" << time / 1000000000.0 << endl;
}

//메뉴화면 출력
int PrintMenu() {
	cout << "================" << endl;
	cout << "PopSong Playlist" << endl;
	cout << "================" << "\n" << endl;
	cout << "수행할 기능을 선택하시오" << endl;
	cout << "1. 입력 2. 정렬 3. 삭제 4. 출력 5.종료" << endl;
	int choice;
	while (true) {
		cout << "->"; 
		cin >> choice;
		if (choice >= 1 && choice <= 5) {
			break;
		}
		cout << "잘못 입력하셨습니다. 재입력 해주세요" << endl;
		if (cin.fail()) {
			cin.clear();
			cin.ignore(1000, '\n');
		}
	}
	return choice;
}

//출력
void Print(map<int, vector<string>>& map) {
	high_resolution_clock::time_point start = high_resolution_clock::now();
	cout << "------------" << "노래 제목" << " / " << "가수" << " / " << "앨범 이름" << "------------" << endl;
	for (int i = 0; i < map.size() - 1; i++) {
		cout << i << "번 : " << map[i][0] << " / " << map[i][1] << " / " << map[i][2] << endl;
	}
	high_resolution_clock::time_point end = high_resolution_clock::now();
	auto time = duration_cast<nanoseconds>(end - start).count();
	cout << "출력이 완료되었습니다." << endl;
	cout << "실행시간(seconds):" << time / 1000000000.0 << endl;
}


int main() {
	//map 초기화 및 Default 팝송 차트 데이터 입력
	map<int, vector<string>> map;
	map[0] = vector<string>{ "dance monkey", "tones and i", "the kids are coming" };
	map[1] = vector<string>{ "memories", "maroon 5", "memories" };
	map[2] = vector<string>{ "2002", "anne marie", "speak your mind" };
	map[3] = vector<string>{ "maniac", "conan gray", "maniac" };
	map[4] = vector<string>{ "paris in the rain", "lauv", "i met you when i was 18" };
	map[5] = vector<string>{ "painkiller", "ruel", "painkiller" };
	map[6] = vector<string>{ "bad guy", "billie eilish", "when we all fall asleep, where do we go?" };
	map[7] = vector<string>{ "to die for", "sam smith", "to die for" };
	map[8] = vector<string>{ "santa tell me", "ariana grande", "santa tell me" };
	map[9] = vector<string>{ "all i want for christmas is you", "mariah carey", "merry christmas" };
	map[10] = vector<string>{ "snowman", "sia", "everyday is christmas" };
	map[11] = vector<string>{ "cheap sunglasses", "john k", "love + everything else" };
	map[12] = vector<string>{ "believer", "imagine dragons", "evolve" };
	map[13] = vector<string>{ "bad", "christopher", "under the surface" };
	map[14] = vector<string>{ "mad at disney", "salem ilese", "mad at disney" };
	map[15] = vector<string>{ "comethru", "jeremy zucker", "summer," };
	map[16] = vector<string>{ "watermelon sugar", "harry styles", "fine line" };
	map[17] = vector<string>{ "holy", "justin bieber", "holy" };
	map[18] = vector<string>{ "one call away", "charlie puth", "nine track mind" };
	map[19] = vector<string>{ "circles", "post malone", "hollywood's bleeding" };
	map[1000] = vector<string>{ "", "", "" }; // Swap()할 때 temp 역할을 한다.

	Print(map);
	cout << "\n" << endl;
	
	while (true) {
		switch (PrintMenu()) {
		case 1:		
			Insert(map);
			break;
		case 2:			
			Sort(map);
			break;
		case 3:		
			Delete(map);
			break;
		case 4:
			Print(map);
			break;
		case 5:
			exit(0);
		}
	}
	return 0;
}