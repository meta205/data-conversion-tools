# -*- coding: utf-8 -*-

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='target file path')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
