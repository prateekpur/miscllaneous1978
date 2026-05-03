from utils import check_input_num , check_input_float

def get_inputs():
    num1 = check_input_float("Enter number 1:")
    num2 = check_input_float("Enter number 2:")
    valid_ops = ("+", "-", "/", "*")
    while True:
        oper = input("Enter operator (+, -, *, /):")
        if oper not in valid_ops :
            print ("Wrong input")
        else :
            if oper == "/" and num2 == 0:
                print ("Wrong inputs. Divide by 0 is not an option")
                while num2 == 0.0:
                    num2 = check_input_float("Enter number 2:")
            break
    return (num1, num2, oper)

def calc() :
    num1, num2, oper = get_inputs()
    match oper:
        case "+": return( num1 + num2)
        case "-": return(num1 - num2)
        case "*": return(num1 * num2)
        case "/": return( num1 / num2)
        case _: print ("Invalid operation")

if __name__ == "__main__":
    print(calc())
