from math import pi, sin
from sys import argv


class WawFile:
    def __init__(self, duration_secs: float, frequency: int, amplitude: int, discretization_frequancy=44100):
        self.duration_secs = duration_secs
        self.frequency = frequency
        self.d_frequency = discretization_frequancy
        self.amplitude = amplitude
        self.file_size = int(44 + 88200 * duration_secs)

    def generate_representation(self) -> bytes:
        representation = b''  # Поле, хранящее в себе байтовое предств

        # Заголовок .wav файла
        representation += b'\x52\x49\x46\x46'  # Начало RIFF цепочки
        # Размер файла -8 байт
        representation += int.to_bytes(self.file_size - 8, 4, "little")
        representation += b'\x57\x41\x56\x45'  # format	        содержит символы «WAVE» 0x57415645
        representation += b'\x66\x6d\x74\x20'  # subchunk1Id	Содержит символы "fmt " 0x666d7420
        representation += b'\x10\x00\x00\x00'  # subchunk1Size	16 для формата PCM.
        representation += b'\x01\x00'          # audioFormat	Аудио формат, список допустипых форматов. Для PCM = 1
        representation += b'\x01\x00'          # numChannels	Количество каналов. Моно = 1, Стерео = 2 и т.д.
        # sampleRate	    Частота дискретизации. 44100 Гц
        representation += int.to_bytes(self.d_frequency, 4, 'little')
        # byteRate	    Количество байт, переданных за секунду воспроизведения.
        representation += int.to_bytes(self.d_frequency * 2, 4, 'little')
        representation += b'\x02\x00'          # blockAlign	    Количество байт для одного сэмпла, включая все каналы.
        representation += b'\x10\x00'          # bitsPerSample	Количество бит в сэмпле. Так называемая «глубина» 16 бит
        representation += b'\x64\x61\x74\x61'  # subchunk2Id	Содержит символы «data» 0x64617461
        # subchunk2Size	Количество байт в области данных.
        representation += int.to_bytes(self.file_size - 44, 4, "little")

        # Данные .waw файла
        for i in range(0, int(self.duration_secs * self.d_frequency)):
            # Рассчитываем синусойду
            representation += int.to_bytes(int(self.amplitude * sin(2 * pi * i / self.d_frequency * self.frequency)), 2, 'little', signed=True)

        # Возвращаем готовое представление
        return representation


if __name__ == "__main__":
    # Вход осуществляется в следующем порядке:
    # 1: Название выходного файла
    # 2: Частота
    # 3: Амплитуда
    # 4: Длительность сигнала
    try:
        file = open(argv[1], "wb")
        file.write(WawFile(float(argv[4]), int(argv[2]), int(argv[3])).generate_representation())
        file.close()
    except ValueError:
        print("Некорректный ввод. Попробуйте снова")