import re


def extract_number(num : str):
    return float(re.sub(',' , '' , num))

def extract_memory_or_storage(num : str):
    try:
        n,unit = num.split()

        if unit == 'GB':
            return int(n) * 1024
        elif unit == 'MB':
            return int(n)
        return 0
    except:
        print(num)

if __name__ == "__main__":
    print(extract_number('1,73,000'))
    print(extract_number('173,000'))


