#include<iostream>
#include<climits>
using namespace std;
int main() {
	int t,ind,sum;
	cin>>t;
	int arr1[t]={0};
	int maxsum=INT_MIN;
	for(int i=0;i<t;i++)
	{
		int n;
		cin>>n;
		int arr[n]={0};
		for(int j=0;j<n;j++)
		{
			cin>>arr[j];
		}
		maxsum=0;
	
	for(int m=2;m<=n;m++)
	{

	ind=0;
	while(ind<n)
	{
		sum=0;
		for(int i=0;i<m;i++)
		{
			sum+=arr[(i+ind)%n];
						
		}
		cout<<sum<<endl;
		if(sum>maxsum)
			{
				maxsum=sum;
			}
		ind++;
	}

	}
	arr1[i]=maxsum;	
	}
	for(int i=0;i<t;i++)
	{
		cout<<arr1[i]<<endl;
	}
	return 0;
}
