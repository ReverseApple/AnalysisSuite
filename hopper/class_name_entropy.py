import re

import collections

from math import log2

document = Document.getCurrentDocument()


def shannon_entropy(X: bytes):
    result = 0.0

    items = collections.Counter(X).items()
    for b, count in items:
        pr = count / len(X)
        result -= pr * log2(pr)

    return result


def get_all_symbol_names():
    txt_seg = document.getSegmentByName('__TEXT')
    txt_seg.labelIterator()
    return txt_seg.getLabelsList()


def sift_objc_classes(symbols):
    pattern = r"__objc_class_(.*)_methods"
    result_buffer = []

    for symbol in symbols:
        match = re.match(pattern, symbol)
        if match:
            result_buffer.append(match.group(1))

    return result_buffer

def main():
    symbols = get_all_symbol_names()
    symbols = sift_objc_classes(symbols)
    symbols.sort(key=shannon_entropy)
    symbols.reverse()

    print("Top 50 entropic objc class names:")

    for symbol in symbols[:50]:
        print(f"* {symbol}")


if __name__ == '__main__':
    main()
