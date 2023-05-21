def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return average

def main():
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    print("The average is:", avg)

if __name__ == '__main__':
    main()
