# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.

import asyncio
import sys
import aiohttp
import time
urls = ['https://gas-kvas.com/uploads/posts/2023-02/1675489747_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-24.png',
        'https://fikiwiki.com/uploads/posts/2022-02/1644865303_51-fikiwiki-com-p-skachat-kartinki-khoroshego-kachestva-59.jpg',
        'https://w.forfun.com/fetch/1f/1ff02e3ba9cecf53fa276611f21c6881.jpeg',
        'https://w.forfun.com/fetch/56/5656d35727009cabea6ce79973a9702c.jpeg',
        'https://img.desktopwallpapers.ru/rocks/pics/wide/1920x1200/465fe2b0f7394ff33b5adc2a12243cc4.jpg',
        ]

async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            chunk = await response.content.read()
            filename = 'asyncio_' + url.split("/")[-1]
            with open(filename, mode="wb") as f:
                f.write(chunk)
                print(f"Загружен файл {url} за {time.time() - start_time:.2f} секунд\n")

async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

start_time = time.time()

if __name__ == '__main__':
    if len (sys.argv) > 1:
        urls.append(sys.argv[1])
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
    print(f"Общее время выполнения {time.time() - start_time:.2f} секунд\n")