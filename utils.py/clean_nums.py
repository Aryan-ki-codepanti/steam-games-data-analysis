import re


def extract_number(num : str):
    return float(re.sub(',' , '' , num))

if __name__ == "__main__":
    print(extract_number('1,73,000'))
    print(extract_number('173,000'))


