#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <ctime>
#include <chrono>

#define max(a, b) ((a < b) ? b : a)

using namespace std;
using namespace std::chrono;

void MakeString(FILE* file, vector<char>& string) {
	char ch;
	while ((ch = fgetc(file)) != EOF) {
		string.push_back(ch);
	}
	rewind(file);
}

void LoadFile(vector<char*>& fileNameVec, vector< vector<char>* >& stringVec) {
	char* fileName;
	int len;
	int fileNum = 0;
	FILE* fp;
	bool finishCheck = false;
	vector<char>* _string;

	cout << "프로그램 이름을 입력하시오. 입력이 완료되면 'q'를 입력하시오 :" << endl;

	while (true) {
		fileName = (char*)malloc(sizeof(char) * 128);
		fileNum++;
		while (true) {
			cout << "프로그램" << fileNum << " :";
			fgets(fileName, 128, stdin);
			len = strlen(fileName);
			fileName[len - 1] = '\0';

			if (strcmp(fileName, "q") == 0) {
				if (fileNameVec.size() < 15) {
					cout << "15개 이상의 프로그램이 필요합니다. 다시 입력하시오." << endl;
					continue;
				}
				free(fileName);
				finishCheck = true;
				break;
			}
			fp = fopen(fileName, "rt");
			if (fp == NULL) {
				cout << "프로그램 이름이 올바른지 확인하시오. 다시 입력하시오." << endl;
				continue;
			}
			_string = new vector<char>();
			MakeString(fp, *_string);
			if (_string->size() < 27) {
				cout << "각 프로그램은 27글자 이상의 문자가 필요합니다. 다시 입력하시오." << endl;
				free(_string);
				continue;
			}
			fclose(fp);
			fileNameVec.push_back(fileName);
			stringVec.push_back(_string);
			break;
		}
		if (finishCheck == true) break;
	}
}

void GetMalCode(vector<char>& malCode, int& len) {
	while (true) {
		char ch;
		cout << "악성코드를 입력하시오 : ";
		while ((ch = getchar()) != '\n') {
			malCode.push_back(ch);
		}
		if (malCode.size() < 12) {
			cout << "악성코드에는 12글자 이상의 문자를 입력하시오. 다시 입력하시오." << endl;
			malCode.clear();
			continue;
		}
		break;
	}
	while (true) {
		cout << "악성코드 패턴의 길이를 입력하시오 : ";
		cin >> len;
		if (cin.fail()) {
			cout << "정수를 입력해야 합니다. 다시 입력하시오." << endl;
			cin.clear();
			cin.ignore(1000, '\n');
			continue;
		}
		if (len < 1 || len > malCode.size()) {
			cout << "악성코드 패턴의 길이는 0보다 크고 프로그램 텍스트의 전체 길이 이하입니다. 다시 입력하시오." << endl;
			continue;
		}
		break;
	}
}

void MakeMalPattern(vector<char> malCode, int patternLen, vector< vector<char>* >& patternVec) {
	vector<char>* _pattern;
	for (int i = 0; i <= (malCode.size() - 1) - patternLen + 1; i++) {
		_pattern = new vector<char>();
		for (int j = 0; j < patternLen; j++) {
			_pattern->push_back(malCode[i + j]);
		}
		patternVec.push_back(_pattern);
	}
}

// KMP Algorithm
void PRE_KMP(vector<char> x, vector<int>& kmp_next) {
	int m = x.size();
	int i, j;
	i = 0;
	j = kmp_next[0] = -1;
	while (i < m) {
		while (j > -1 && x[i] != x[j]) j = kmp_next[j];
		kmp_next[++i] = ++j;
	}
}

bool KMP(vector<char> y, vector<char> x) {
	int n = y.size();
	int m = x.size();
	int i, j;
	vector<int> kmp_next(m + 1);
	PRE_KMP(x, kmp_next);

	i = j = 0;
	while (i < n) {
		while (j > -1 && x[j] != y[i]) j = kmp_next[j];
		i++;
		j++;
		if (j >= m) {
			return true;
		}
	}
	return false;
}

//Boyer_moore Algorithm
bool is_prefix(vector<char>& word, int pos) {
	int wordlen = word.size();
	int suffixlen = wordlen - pos;
	for (int i = 0; i < suffixlen - 1 - (pos - 1); i++) {
		if (word[i] != word[pos + i]) {
			return false;
		}
	}
	return true;
}

int suffix_length(vector<char>& word, int pos) {
	int wordlen = word.size();
	int i;
	for (i = 0; (word[pos - i] == word[wordlen - 1 - i]) && (i <= pos); i++);
	return i;
}

void makeDelta1(vector<int>& delta1, vector<char>& pat) {
	int patlen = pat.size();
	int len = 256;
	for (int i = 0; i < len; i++) {
		delta1[i] = patlen;
	}

	for (int i = 0; i < patlen - 1; i++) {
		delta1[pat[i]] = patlen - 1 - i;
	}
}

void makeDelta2(vector<int>& delta2, vector<char>& pat) {
	int patlen = pat.size();
	delta2[patlen - 1] = 1;

	int p;
	int last_prefix_index = patlen;

	for (p = patlen - 2; p >= 0; p--) {
		if (is_prefix(pat, p + 1)) {
			last_prefix_index = p + 1;
		}
		delta2[p] = patlen - (patlen - 1 - (last_prefix_index - 1)) + (patlen - 1 - p);
	}

	for (p = 0; p < patlen - 1; p++) {
		int slen = suffix_length(pat, p);
		if (pat[p - slen] != pat[patlen - 1 - slen]) {
			delta2[patlen - 1 - slen] = patlen - 1 - p + slen;
		}
	}
}

bool Boyer_moore(vector<char> string, vector<char> pattern) {
	int stringlen = string.size();
	int patlen = pattern.size();
	int len = 256;
	vector<int> delta1(len);
	vector<int> delta2(patlen);
	makeDelta1(delta1, pattern);
	makeDelta2(delta2, pattern);

	int t, initial_jump;
	for (t = 1; t < patlen; t++) {
		if (is_prefix(pattern, t))break;
	}
	initial_jump = t;

	if (patlen == 0) return false;

	int i = patlen - 1;
	while (i < stringlen) {
		int j = patlen - 1;
		while (j >= 0 && (string[i] == pattern[j])) {
			--i;
			--j;
		}
		if (j < 0) {
			return true;
			i++;
			i += patlen - 1;
			i += initial_jump;
			continue;
		}
		int shift = max(delta1[string[i]], delta2[j]);
		i += shift;
	}
	return false;
}

void Detect(
	bool (*Algorithm)(vector<char>, vector<char>),
	vector<char*>& fileNameVec,
	vector< vector<char>* >& stringVec,
	vector< vector<char>* >& patVec,
	vector<char*>& normalCodeVec,
	vector<char*>& malCodeVec
) {
	bool flag;

	for (int i = 0; i < stringVec.size(); i++) {
		flag = false;
		for (int j = 0; j < patVec.size(); j++) {
			if (Algorithm(*(stringVec[i]), *(patVec[j]))) {
				flag = true;
				break;
			}
		}
		if (flag == true) malCodeVec.push_back(fileNameVec[i]);
		else normalCodeVec.push_back(fileNameVec[i]);
	}
}

void PrintResult(vector<char*> normalCodeVec, vector<char*> malCodeVec) {
	cout << endl;
	cout << "정상 프로그램 리스트: " << endl;
	for (int i = 0; i < normalCodeVec.size(); i++) {
		cout << normalCodeVec[i] << endl;
	}
	cout << "정상 프로그램의 수: " << normalCodeVec.size() << endl;
	cout << "바이러스 패턴을 가진 프로그램 리스트: " << endl;
	for (int i = 0; i < malCodeVec.size(); i++) {
		cout << malCodeVec[i] << endl;
	}
	cout << "바이러스 패턴을 가진 프로그램의 수: " << malCodeVec.size() << endl;
	cout << endl;
}

int main(void) {
	int patternLen;
	vector<char*> fileNameVec;
	vector< vector<char>* > stringVec;	
	vector<char> malCode;
	vector< vector<char>* > patternVec;
	vector<char*> normalCodeVec;
	vector<char*> malCodeVec;
	LoadFile(fileNameVec, stringVec);
	GetMalCode(malCode, patternLen);
	MakeMalPattern(malCode, patternLen, patternVec);

	cout << endl << "<KMP Algorithm>" << endl;
	high_resolution_clock::time_point start = high_resolution_clock::now();
	Detect(KMP, fileNameVec, stringVec, patternVec, normalCodeVec, malCodeVec);
	high_resolution_clock::time_point end = high_resolution_clock::now();
	auto time = duration_cast<nanoseconds>(end - start).count();

	PrintResult(normalCodeVec, malCodeVec);
	cout << "실행시간(seconds): " << time / 1000000000.0 << endl;

	normalCodeVec.clear();
	malCodeVec.clear();

	cout << endl << "<Boyer-Moore Algorithm>" << endl;
	start = high_resolution_clock::now();
	Detect(Boyer_moore, fileNameVec, stringVec, patternVec, normalCodeVec, malCodeVec);
	end = high_resolution_clock::now();
	time = duration_cast<nanoseconds>(end - start).count();

	PrintResult(normalCodeVec, malCodeVec);
	cout << "실행시간(seconds): " << time / 1000000000.0 << endl;

	return 0;
}
