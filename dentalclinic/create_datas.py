#include <iostream>
#include <string>
using namespace std;

// Задача 1
struct Person {
    string name;
    int age;
    string address;
};

void printPerson(const Person& person) {
    cout << "Name: " << person.name << ", Age: " << person.age << ", Address: " << person.address << endl;
}

// Задача 2
struct Address {
    string street;
    string city;
    string postalCode;
};

void printAddress(const Address& address) {
    cout << "Street: " << address.street << ", City: " << address.city << ", Postal Code: " << address.postalCode << endl;
}

// Задача 3
struct Date {
    int day;
    int month;
    int year;
};

int main() {
    // Задача 1
    cout << "Task 1:" << endl;
    Person person = {"John Doe", 30, "123 Main St, City, 12345"};
    printPerson(person);

    // Задача 2
    cout << "\nTask 2:" << endl;
    Address address = {"456 Elm St", "Town", "54321"};
    printAddress(address);

    // Задача 3
    cout << "\nTask 3:" << endl;
    Date date = {29, 2, 2024};

    return 0;
}
