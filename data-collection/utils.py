from bs4 import BeautifulSoup
import re
# constant denoting unknown / absent / missing values
EMPTY_VALUE = "null"


def extract_memory(mem):
    mem = mem.upper()
    gb_idx = mem.find("GB")
    mb_idx = mem.find("MB")

    actual_mem = mem

    if gb_idx != -1:
        
        actual_mem = mem[:gb_idx]
        actual_mem = re.sub("[^0-9]","",actual_mem)
        actual_mem += " GB"

    elif mb_idx != -1:
        actual_mem = mem[:mb_idx]
        actual_mem = re.sub("[^0-9]","",actual_mem)
        actual_mem += " MB"

    return actual_mem

def parse__requirements_html(html):
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    lis = list(soup.children)[0].find_all_next('li')

    # os, processor , memory , graphics , directX , storage
    requirements = {
        "os": "",
        "processor": "",
        "memory": "",
        "graphics": "",
        "directx": "",
        "storage": ""
    }

    for li in lis:
        req = li.get_text(strip=True).split(":")

        if len(req) < 1 or len(req) > 2:
            continue
        elif len(req) == 1:
            for requirement in requirements.keys():
                if requirement in req[0].lower():
                    requirements[requirement] += f"{req[0]} "
            continue
        
        # len(req) = 2
        key,value = req
        for requirement in requirements.keys():
            if requirement in key.lower():
                requirements[requirement] += f"{value} "

    # os, processor , memory , graphics , directX , storage
    parsed_requirements = [
        requirements["os"].strip() if requirements["os"] else EMPTY_VALUE,
        requirements["processor"].strip() if requirements["processor"] else EMPTY_VALUE,
        extract_memory(requirements["memory"].strip()) if requirements["memory"] else EMPTY_VALUE,
        requirements["graphics"].strip() if requirements["graphics"] else EMPTY_VALUE,
        requirements["directx"].strip() if requirements["directx"] else EMPTY_VALUE,
        extract_memory(requirements["storage"].strip()) if requirements["storage"] else EMPTY_VALUE
    ]

    return parsed_requirements
