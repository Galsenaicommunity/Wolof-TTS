units = {
    0: "nópp",
    1: "benn",
    2: "ñaar",
    3: "ñett",
    4: "ñeent",
    5: "juróom",
    6: "juróom benn",
    7: "juróom ñaar",
    8: "juróom ñett",
    9: "juróom ñeent"
}

tens = {
    1: "fukk",
    2: "ñaar fukk",
    3: "ñett fukk",
    4: "ñeent fukk",
    5: "juróom fukk",
    6: "juróom benn fukk",
    7: "juróom ñaar fukk",
    8: "juróom ñett fukk",
    9: "juróom ñeent fukk"
}
def process_block(n):
    if n == 0:
        return ""

    result = ""

    # Processing hundreds
    hundreds = n // 100
    if hundreds > 0:
        match hundreds:
            case 1:
                result += "téeméer "
            case _:
                result += units[hundreds] +"i" + " téeméer "


    # Processing tens
    remainder = n % 100
    ten = remainder // 10
    unit = remainder % 10

    if ten > 0:
        if result:  
            result += "ak "
        result += tens[ten] + " "
         
            

    # Processing units
    if unit > 0:
        if result:  
            result += "ak "
        result += units[unit]

    return result.strip()

def spell_number_in_wolof(number):
    """
    Function that takes an integer and returns its pronunciation in Wolof.
    Uses a block approach to handle numbers up to 999,999,999.
    """



    # Special case: zero
    if number == 0:
        return units[0]

    # For negative numbers
    if number < 0:
        return "minus " + spell_number_in_wolof(abs(number))

    # For numbers greater than 999,999,999
    if number > 999_999_999:
        return "Number too large to process"

    # Function to process blocks from 1 to 999

    # Decomposition of the number into blocks
    billions = number // 1_000_000_000
    millions = (number % 1_000_000_000) // 1_000_000
    thousands = (number % 1_000_000) // 1_000
    units_block = number % 1_000

    result = ""

    # Processing billions (just in case)
    if billions > 0:
        match billions:
            case 1:
                result += "milliar "
            case _:
                result += process_block(billions) +"i" + " milliar "

    # Processing millions
    if millions > 0:
        if result :
            result += "ak "
        match millions:
            case 1:
                result += "million "
            case _:
                result += process_block(millions) +"i" + " million "

    # Processing thousands
    if thousands > 0:
        if result :
            result += "ak "
        match thousands:
            case 1:
                result += "junni "
            case _:
                result += process_block(thousands) +"i" + " junni "

    # Processing units
    if units_block > 0 or (number == 0):
        if result :
            result += "ak "
        print(units_block   )
        result += process_block(units_block)

    return result.strip()


