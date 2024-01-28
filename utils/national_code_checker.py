def verify_national_code(national_cole: str):
    try:
        int(national_cole)
    except:
        return False
    length = len(national_cole)
    if length > 10 or length < 8:
        return False
    if length < 10:
        while len(national_cole) == 10:
            national_cole = '0' + national_cole

    control_digit = int(national_cole[-1])
    nine_digit = national_cole[:9][::-1]
    sum_digit = 0
    for i in range(len(nine_digit)):
        factor = i + 2
        sum_digit += int(nine_digit[i]) * factor
    remainder = sum_digit % 11
    if remainder >= 2:
        return 11 - remainder == control_digit
    else:
        return remainder == control_digit