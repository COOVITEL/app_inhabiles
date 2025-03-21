def setValue(value):
    reverseValue = list(value[::-1])
    formatted_list = []
    for i, char in enumerate(reverseValue):
        if i > 0 and i % 3 == 0:
            formatted_list.append(".")
        formatted_list.append(char)
    
    return "".join(formatted_list[::-1])

if __name__ == '__main__':
    print(setValue("25000000"))