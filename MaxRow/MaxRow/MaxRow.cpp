/* MaxRow.cpp : This file contains the 'main' function. Program execution begins and ends there.
Author: Michael Liguori and Nico C.
Purpose: to use two variables, maxRow and indexofRow, to find the row with the largest sum
*/

#include <iostream>
using namespace std;

const int ROW_SIZE = 10;
const int COLUMN_SIZE = 10;

void fillMatrix(int matrix[ROW_SIZE][COLUMN_SIZE]);

int sumOfRow(int matrix[ROW_SIZE][COLUMN_SIZE],  int& maxSum);

int sumOfRowAtRowIndex(int matrix[ROW_SIZE][COLUMN_SIZE], int index);

int main()
{
    int matrix[ROW_SIZE][COLUMN_SIZE];
    fillMatrix(matrix);
    int  maxSum = sumOfRowAtRowIndex(matrix,0);
    int largestRowSumIndex = sumOfRow(matrix, maxSum);
    cout << "The largest sum of a row in the matrix is " << maxSum << " which is the row indexed at " << largestRowSumIndex;
    return 0;
}

//Functions
void fillMatrix(int matrix[ROW_SIZE][COLUMN_SIZE]) 
{
    int number = 0;
    for (int i = 0; i < ROW_SIZE; i++) 
    {
        for (int j = 0; j < COLUMN_SIZE; j++) 
        {
            matrix[i][j] = number;
            number++;
        }
    }
}

int sumOfRow(int matrix[ROW_SIZE][COLUMN_SIZE],  int& maxSum)
{
    int largestRowSumIndex = 0;
    for (int i = 1; i < ROW_SIZE; i++) 
    {
        cout << "The sum of row " << i << " is " << sumOfRowAtRowIndex(matrix, i) << endl;
        if (sumOfRowAtRowIndex(matrix, i) > maxSum) 
        {
            maxSum = sumOfRowAtRowIndex(matrix, i);
            largestRowSumIndex = i;
        }
    }
    return largestRowSumIndex;
}

int sumOfRowAtRowIndex(int matrix[ROW_SIZE][COLUMN_SIZE], int index)
{
    int sum = 0;
    for (int i = 0; i < COLUMN_SIZE; i++) 
    {
        sum += matrix[index][i];
    }
    return sum;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
