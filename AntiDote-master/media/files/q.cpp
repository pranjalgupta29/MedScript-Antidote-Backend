using namespace std;
#include<iostream>


int factor_count_by_3(int x){
	if(x%3 != 0 || x == 0)
	return 0;
	
	else
	return factor_count_by_3(x/3) + 1;
}

int main(){
	using namespace std;
	cout<< factor_count_by_3(3) << endl;
	cout<< factor_count_by_3(0) << endl;
	cout<< factor_count_by_3(8) << endl;
	cout<< factor_count_by_3(27) << endl;
	cout<< factor_count_by_3(162) << endl;
	cout<< factor_count_by_3(59049) << endl;
}
