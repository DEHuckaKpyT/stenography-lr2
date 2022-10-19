import copy

import numpy as np
from matplotlib.pyplot import imread
from matplotlib.pyplot import imsave

start_image = imread('image.bmp')
# image = copy.deepcopy(imread('image.bmp'))  # начальная картинка
with open('message.txt') as file:
    message = file.read()  # сообщение для шифрования
colors = [0, 1, 2]  # цвета rgb: 0 - r, 1 - g, 2 - b

width = start_image.shape[0]
height = start_image.shape[1]


def print_header():
    print(f"Высота = {width} пикселей")
    print(f"Ширина = {height} пикселей")
    print(f"Максимальный встраиваемый объём информации и максимальное встраиваемое число символов:")
    print(f"Если используются последний бит и все три компоненты цвета: "
          f"{(width * height * 3)} бит информации, "
          f"{(width * height * 3) // 8} символов")
    print(f"Если используются два последних бита и все три компоненты цвета: "
          f"{(width * height * 2 * 3)} бит информации, "
          f"{(width * height * 2 * 3) // 8} символов")
    print(f"Если используются три последних младших бита и все три компоненты цвета: "
          f"{(width * height * 3 * 3)} бит информации, "
          f"{(width * height * 3 * 3) // 8} символов")
    print()
    print(f"Последний бит, три компоненты цвета, 10% от макс объёма: "
          f"{((width * height * 3) // 8) * 10 // 100} символов")
    print(f"Два последних бита, три компоненты цвета, 10% от макс объёма: "
          f"{((width * height * 2 * 3) // 8) * 10 // 100} символов")
    print(f"Три последних бита, три компоненты цвета, 10% от макс объёма: "
          f"{((width * height * 3 * 3) // 8) * 10 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 20% от макс объёма: "
          f"{((width * height * 3) // 8) * 20 // 100} символов")
    print(f"Два последних бита, три компоненты цвета, 20% от макс объёма: "
          f"{((width * height * 2 * 3) // 8) * 20 // 100} символов")
    print(f"Три последних бита, три компоненты цвета, 20% от макс объёма: "
          f"{((width * height * 3 * 3) // 8) * 20 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 30% от макс объёма: "
          f"{((width * height * 3) // 8) * 30 // 100} символов")
    print(f"Два последних бита, три компоненты цвета, 30% от макс объёма: "
          f"{((width * height * 2 * 3) // 8) * 30 // 100} символов")
    print(f"Три последних бита, три компоненты цвета, 30% от макс объёма: "
          f"{((width * height * 3 * 3) // 8) * 30 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 50% от макс объёма: "
          f"{((width * height * 3) // 8) * 50 // 100} символов")
    print(f"Два последних бита, три компоненты цвета, 50% от макс объёма: "
          f"{((width * height * 2 * 3) // 8) * 50 // 100} символов")
    print(f"Три последних бита, три компоненты цвета, 50% от макс объёма: "
          f"{((width * height * 3 * 3) // 8) * 50 // 100} символов")

    print(f"Последний бит, три компоненты цвета, 75% от макс объёма: "
          f"{((width * height * 3) // 8) * 75 // 100} символов")
    print(f"Два последних бита, три компоненты цвета, 75% от макс объёма: "
          f"{((width * height * 2 * 3) // 8) * 75 // 100} символов")
    print(f"Три последних бита, три компоненты цвета, 75% от макс объёма: "
          f"{((width * height * 3 * 3) // 8) * 75 // 100} символов")


def pixel(rgb):
    return 0.299 * int(rgb[0]) + 0.587 * int(rgb[1]) + 0.114 * int(rgb[2])


def get_MD(images):
    maxx = 0
    for image in images:
        for i in range(width):
            for j in range(height):
                current = np.abs(pixel(start_image[i][j]) - pixel(image[i][j]))
                if current > maxx:
                    maxx = current
    return maxx


def get_CQ(images):
    sum_CS = 0
    sum_CC = 0
    for image in images:
        for i in range(width):
            for j in range(height):
                sum_CS += pixel(start_image[i][j]) * pixel(image[i][j])
                sum_CC += pixel(start_image[i][j]) * pixel(start_image[i][j])
    return sum_CS / sum_CC


def get_GSSNR(images):
    n = np.gcd(width, height)

    for image in images:
        sum1 = 0
        sum2 = 0

        for w in range(0, width, n):
            for h in range(0, height, n):
                c = 0
                s = 0

                for x in range(n):
                    for y in range(n):
                        width_x = w + x
                        height_y = h + y

                        c += pixel(start_image[width_x][height_y])
                        s += pixel(image[width_x][height_y])

                sigma1 = np.sqrt(((1 / n) * (c ** 2)) - (((1 / n) * c) ** 2))
                sigma2 = np.sqrt(((1 / n) * (s ** 2)) - (((1 / n) * s) ** 2))

                sum1 += sigma1 ** 2
                sum2 += (sigma1 - sigma2) ** 2

        gssnr = sum1 / sum2
        print(f"gssnr = {gssnr}")


def print_footer(images):
    print(f"MD = {get_MD(images)}")
    print(f"CQ = {get_CQ(images)}")
    get_GSSNR(images)


def get_sequence():
    symbols = ['{:08b}'.format(symbol) for symbol in bytearray(message, 'utf-8')]
    return ''.join(symbols)


def insert_into(s, index, ch):
    return s[:index] + ch + s[index + 1:]


def set_pixel_bit(pixel, rgb, bit, value):
    color = '{:08b}'.format(pixel[rgb])
    color = color[:bit] + value + color[bit + 1:]
    pixel[rgb] = int(color, 2)


def embed_text_to_image(bits, percent, image):
    number = 0
    sequence = get_sequence()
    sequence_length = len(sequence)

    count_of_embeding_bits = (width * height * len(bits) * 3) * percent // 100

    for row in image:
        for pixel in row:
            for color in colors:
                for bit in bits:
                    set_pixel_bit(pixel, color, bit, sequence[number % sequence_length])

                    number += 1

                    if number == count_of_embeding_bits:
                        return


def main():
    print_header()
    bits = [[7], [6, 7], [5, 6, 7]]  # номера битов для замены; отсчёт от нуля
    percents = [10, 20, 30, 50, 75]

    images = [copy.deepcopy(imread('image.bmp')) for _ in range(15)]

    image_number = 0
    for percent in percents:
        for bitsList in bits:
            image = images[image_number]
            image_number += 1
            print(f"Обрабатывается картинка {image_number}")

            embed_text_to_image(bitsList, percent, image)
            imsave(f'image{image_number}.bmp', image)

    print_footer(images)


if __name__ == '__main__':
    main()
    print()
    print("end")
