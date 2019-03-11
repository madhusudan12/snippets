# -*- coding: utf-8 -*-

def main():
    x = u"रच-आउटसरसग-क-करण-बढ"
    n = x.rfind('-')
    print(x[:n])

    print(len(x))


if __name__ == '__main__':
    main()