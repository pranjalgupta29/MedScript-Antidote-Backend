#include<iostream>
using namespace std;
int sum(int arr[],int i,int n)
{
	if(i==(n-1))
		return arr[n-1];
	else
		return arr[i]+sum(arr,i+1,n);
}
int main()
{
	int n;
	cout<<"Enter the number of elements in an array: ";
	cin>>n;
	int a[n];
	cout<<"Enter the array : ";
	for(int i=0;i<n;i++)
	{
		cin>>a[i];
	}
	cout<<"Sum of array elements is : "<<sum(a,0,n);
	return 0;
}
