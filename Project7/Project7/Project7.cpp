/* Project7.cpp : This file contains the 'main' function. Program execution begins and ends there.
Author: Michael Liguori
Title: Project 7
Purpose: To modify project 6 such that struct is used to retain the information entered by the user.
*/

#include <iostream>
#include <string>
using namespace std;

const int HISTORY_COLUMN_SIZE = 2;

struct weatherRecord {
    double temperature;
    double windSpeed;
    string windDirection;
};

void input(weatherRecord* historyArray,  int goodData)
{
    double input;
    string stringInput;
    cout << "Option 1:" << endl;
    cout << "Please enter the current temperature: ";
    cin >> input;
    historyArray[goodData].temperature = input;
    cout << endl;
    cout << "Please enter the current wind speed: ";
    cin >> input;
    historyArray[goodData].windSpeed = input;
    cout << endl;
    cout << "Please enter the current wind direction: ";
    cin.ignore(1000, '\n');
    cin.clear();
    getline(cin, stringInput);
    cout << endl;
    historyArray[goodData].windDirection = stringInput;
}

void printCurrent(string weatherStationName, weatherRecord* historyArray, int goodData)
{
    cout << "Option 2:" << endl;
    cout << "Weather Station Name: " << weatherStationName << endl;
    cout << endl;
    cout << "Current Temperature: " << historyArray[goodData - 1].temperature << endl;
    cout << "Current Wind Speed and Direction: " << historyArray[goodData - 1].windSpeed << ", " << historyArray[goodData - 1].windDirection << endl;
    cout << endl;
}

void printHistory(string weatherStationName, weatherRecord* historyArray, int goodData)
{
    cout << "Option 3:" << endl;
    cout << "Weather Station Name: " << weatherStationName << endl;
    cout << endl;
    if (goodData > 1)
        cout << "Last " << goodData << " weather readings from the station: " << endl;
    for (int i = (goodData - 1); i >= 0; i--)
    {
        if (i == 0 && goodData == 1)
        {
            cout << "Only Reading Recorded : " << endl;
        }
        else if (i == (goodData - 1))
        {
            cout << "Record " << (i + 1) << ": (most recent)" << endl;
        }
        else if (i == 0)
        {
            cout << "Record " << (i + 1) << ": (oldest)" << endl;
        }
        else
        {
            cout << "Record " << (i + 1) << ": " << endl;
        }

        cout << "Temperature: " << historyArray[i].temperature << " Wind Speed:  " << historyArray[i].windSpeed << " Direction: " << historyArray[i].windDirection << endl;
        cout << endl;
    }
}


int main()
{
    string weatherStationName;

    cout << "Please enter the name of the weather station: ";
    getline(cin, weatherStationName);
    cout << "Please enter the amount records of past readings inputted to keep in history: ";
    int historySize;
    cin >> historySize;
    weatherRecord* historyArray;
    historyArray = new weatherRecord[historySize] ;
    int goodData = 0;
    bool isDone = false;
    bool hasInputedData = false;
    cout << endl;
    cout << "There are four options within this program you can choose from. \n";
    cout << endl;
    while (isDone == false)
    {
        cout << "Option 1: Input values for the current temperature, wind speed, and wind direction." << endl;
        cout << "Option 2: Print out to the console the weather station name along with the current temperature, wind speed, and wind direction." << endl;
        cout << "Option 3: Print out to the console the five most recent values inputed for temperature, wind speed, and wind direction." << endl;
        cout << "Option 4: Quit the program." << endl;
        int option;
        cout << endl;
        cout << "Please enter either 1, 2, 3, or 4 to select the corresponding option. ";
        cin >> option;
        cout << endl;
        if (option == 1)
        {
            if (goodData == historySize)
            {
                goodData--;
                for (int i = 0; i < goodData; i++)
                {
                    double temp = historyArray[i + 1].temperature;
                    historyArray[i].temperature = temp;
                    temp = historyArray[i + 1].windSpeed;
                    historyArray[i].windSpeed = temp;
                    string tempString = historyArray[i + 1].windDirection;
                    historyArray[i].windDirection = tempString;
                }
            }
            input(historyArray, goodData);
            goodData++;
            hasInputedData = true;
        }
        else if (option == 2)
        {
            if (hasInputedData)
            {
                printCurrent(weatherStationName, historyArray, goodData);
            }
            else
            {
                cout << "No data to print. Please use option 1 to input data, then option 2 to print the current weather readings. \n";
                cout << endl;
            }
        }
        else if (option == 3)
        {
            if (hasInputedData)
            {
                printHistory(weatherStationName, historyArray, goodData);
            }
            else
            {
                cout << "No data to print. Please use option 1 to input data, then option 3 to print up to the last five weather readings. \n";
                cout << endl;
            }
        }
        else if (option == 4)
        {
            cout << "Thank you and have a good day!";
            isDone = true;
            cout << endl;
        }
        else
        {
            cout << "Please enter a valid option value, such as 1, 2, or 3. \n";
            cout << endl;
        }


    }
    delete[] historyArray;
    historyArray = NULL;

    return 0;
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