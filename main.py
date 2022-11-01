import copy

import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

start_image = plt.imread('image.bmp')
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
    maxx = [0 for i in range(len(images))]

    for image_number in range(len(images)):
        for i in range(width):
            for j in range(height):
                current = np.abs(pixel(start_image[i][j]) - pixel(images[image_number][i][j]))
                if current > maxx[image_number]:
                    maxx[image_number] = current

    return maxx


def get_CQ(images):
    sum_CS = [0 for i in range(len(images))]
    sum_CC = [0 for i in range(len(images))]

    for image_number in range(len(images)):
        for i in range(width):
            for j in range(height):
                sum_CS[image_number] += pixel(start_image[i][j]) * pixel(images[image_number][i][j])
                sum_CC[image_number] += pixel(start_image[i][j]) * pixel(start_image[i][j])

    return [sum_CS[i] / sum_CC[i] for i in range(len(images))]


def get_SNR(images):
    sum_CS = [0 for i in range(len(images))]
    sum_CC = [0 for i in range(len(images))]

    for image_number in range(len(images)):
        for i in range(width):
            for j in range(height):
                sum_CS[image_number] += (pixel(start_image[i][j]) - pixel(images[image_number][i][j])) ** 2
                sum_CC[image_number] += pixel(start_image[i][j]) ** 2

    return [sum_CS[i] / sum_CC[i] for i in range(len(images))]


def get_NAD(images):
    sum_CS = [0 for i in range(len(images))]
    sum_C = [0 for i in range(len(images))]

    for image_number in range(len(images)):
        for i in range(width):
            for j in range(height):
                sum_CS[image_number] += np.abs(pixel(start_image[i][j]) - pixel(images[image_number][i][j]))
                sum_C[image_number] += pixel(start_image[i][j])

    return [sum_CS[i] / sum_C[i] for i in range(len(images))]


def get_GSSNR(images):
    n = np.gcd(width, height)
    gssnr_list = []

    for image_number in range(len(images)):
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
                        s += pixel(images[image_number][width_x][height_y])

                sigma1 = np.sqrt(((1 / n) * (c ** 2)) - (((1 / n) * c) ** 2))
                sigma2 = np.sqrt(((1 / n) * (s ** 2)) - (((1 / n) * s) ** 2))

                sum1 += sigma1 ** 2
                sum2 += (sigma1 - sigma2) ** 2

        gssnr = sum1 / sum2
        gssnr_list.append(gssnr)

    return gssnr_list


def print_row(worksheet, row, values, name):
    worksheet.write(row, 0, name)

    for i in range(len(values)):
        worksheet.write(row, i + 1, values[i])


def print_footer(images):
    # snrs = get_SNR(images)
    # nads = get_NAD(images)
    mds = get_MD(images)
    cqs = get_CQ(images)
    gssnrs = get_GSSNR(images)

    print(f"MD = {mds}")
    print(f"CQ = {cqs}")
    print(f"GSSNR = {gssnrs}")

    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    print_row(worksheet, 0, mds, "MD")
    print_row(worksheet, 1, cqs, "CQ")
    print_row(worksheet, 2, gssnrs, "GSSNR")
    workbook.close()

    plt.rcParams["figure.autolayout"] = True
    x = np.array([10, 20, 30, 50, 75])
    fig, axs = plt.subplots(3, 3)

    axs[0, 0].plot(x, [mds[0], mds[3], mds[6], mds[9], mds[12]], marker='o', color='b')  # , markevery=x)
    axs[0, 0].set_title('MD при 1 bit')
    axs[0, 1].plot(x, [mds[1], mds[4], mds[7], mds[10], mds[13]], marker='o', color='b')  # , markevery=x)
    axs[0, 1].set_title('MD при 2 bit')
    axs[0, 2].plot(x, [mds[2], mds[5], mds[8], mds[11], mds[14]], marker='o', color='b')  # , markevery=x)
    axs[0, 2].set_title('MD при 3 bit')

    axs[1, 0].plot(x, [cqs[0], cqs[3], cqs[6], cqs[9], cqs[12]], marker='o', color='b')  # , markevery=x)
    axs[1, 0].set_title('CQ при 1 bit')
    axs[1, 1].plot(x, [cqs[1], cqs[4], cqs[7], cqs[10], cqs[13]], marker='o', color='b')  # , markevery=x)
    axs[1, 1].set_title('CQ при 2 bit')
    axs[1, 2].plot(x, [cqs[2], cqs[5], cqs[8], cqs[11], cqs[14]], marker='o', color='b')  # , markevery=x)
    axs[1, 2].set_title('CQ при 3 bit')

    axs[2, 0].plot(x, [gssnrs[0], gssnrs[3], gssnrs[6], gssnrs[9], gssnrs[12]], marker='o', color='b')  # , markevery=x)
    axs[2, 0].set_title('GSSNR при 1 bit')
    axs[2, 1].plot(x, [gssnrs[1], gssnrs[4], gssnrs[7], gssnrs[10], gssnrs[13]], marker='o', color='b')  # , markevery=x)
    axs[2, 1].set_title('GSSNR при 2 bit')
    axs[2, 2].plot(x, [gssnrs[2], gssnrs[5], gssnrs[8], gssnrs[11], gssnrs[14]], marker='o', color='b')  # , markevery=x)
    axs[2, 2].set_title('GSSNR при 3 bit')

    plt.show()
    # ax.annotate('local max', xy=(3, 1),  xycoords='data',
    # xytext=(0.8, 0.95), textcoords='axes fraction',
    # arrowprops=dict(facecolor='black', shrink=0.05),
    # horizontalalignment='right', verticalalignment='top',
    # )


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

    images = [copy.deepcopy(plt.imread('image.bmp')) for _ in range(15)]

    image_number = 0
    for percent in percents:
        for bitsList in bits:
            image = images[image_number]
            image_number += 1
            print(f"Обрабатывается картинка {image_number}")

            embed_text_to_image(bitsList, percent, image)
            plt.imsave(f'image{image_number}.bmp', image)

    print_footer(images)


if __name__ == '__main__':
    main()
    print()
    print("end")
