from typing import List


def includes(query: str, search_from: List[int]) -> bool:
    for test_case in search_from:
        if str(test_case) in str(query):
            return True
    return False
