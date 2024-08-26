def format_for_read(json):
    json["phone"] = format_phone(json["phone"])
    return json

def format_phone(digits):
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"