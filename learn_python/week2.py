def filter_odd(nums):
    result = [x  for x in nums if x % 2 == 0]
    print(result)

def add_numbers(*args):
    sum_nums = 0
    for num in args:
        print(num)
        sum_nums += num
    print ("Sum : ", sum_nums)
    return sum_nums

def append_str(*args):
    res = " ".join(args)
    return res

def main():
    words = ["10", "2", "3", "4", "5"]
    print(append_str("10", "2", "3", "4", "5"))
    nums = (1,2,3,4,5,6)
    #add_numbers(1,2,3,4,5,6)

if __name__ == "__main__":
    main()
