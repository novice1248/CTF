import os, re

FLAG = os.environ.get("FLAG", "Alpaca{REDACTED}")
assert re.fullmatch(r"Alpaca\{\w+\}", FLAG)

while pattern := input("regex> "):
    if re.match(pattern, FLAG):
        print("Hit!")
    else:
        print("Miss...")
