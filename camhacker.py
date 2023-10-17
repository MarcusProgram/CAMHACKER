#!/usr/bin/env python3 #
# -*- coding: utf-8 -*-

#Выше говорю на каком языке и с какой кодировкой буду писать




#      Данный код был написан программистом
#███╗░░░███╗░█████╗░██████╗░░█████╗░██╗░░░██╗░██████╗
#████╗░████║██╔══██╗██╔══██╗██╔══██╗██║░░░██║██╔════╝
#██╔████╔██║███████║██████╔╝██║░░╚═╝██║░░░██║╚█████╗░
#██║╚██╔╝██║██╔══██║██╔══██╗██║░░██╗██║░░░██║░╚═══██╗
#██║░╚═╝░██║██║░░██║██║░░██║╚█████╔╝╚██████╔╝██████╔╝
#╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░░╚═════╝░╚═════╝░







#Все импорты
import requests, re
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
from colorama import Fore,init

init() #Иницилизация Colorama

url = "http://www.insecam.org/en/jsoncountries/" #юрл сайта где хранятся все камеры отрытые

headers = CaseInsensitiveDict() #Создается словарь заголовков HTTP
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36" # И ставится user-agent

r = requests.get(url, headers=headers)# переходим на url

toJson = r.json() # получаем список стран в формате json
countries = toJson['countries']


print(Fore.RED + """
░█████╗░░█████╗░███╗░░░███╗    ██╗░░██╗░█████╗░░█████╗░██╗░░██╗███████╗██████╗░
██╔══██╗██╔══██╗████╗░████║    ██║░░██║██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██║░░╚═╝███████║██╔████╔██║    ███████║███████║██║░░╚═╝█████═╝░█████╗░░██████╔╝
██║░░██╗██╔══██║██║╚██╔╝██║    ██╔══██║██╔══██║██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
╚█████╔╝██║░░██║██║░╚═╝░██║    ██║░░██║██║░░██║╚█████╔╝██║░╚██╗███████╗██║░░██║
░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝    ╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝

""" + Fore.RESET)
a = input("Please press Enter: ")


for key, value in countries.items(): # проходимся по всем странам и выводим
    print(f'Code: ({Fore.GREEN + key + Fore.RESET}) - {Fore.RED + value["country"] + Fore.RESET};')
    print("")

try:
    i = 1
    country = input("Code: ") # после ввода номера страны
    res = requests.get(f"http://www.insecam.org/en/bycountry/{country}", headers=headers) # получаем юрл с этой страной
    last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)[0] #из хтмл-кода страницы извлекается номер последней страницы с камерами.
    for page in range(int(last_page)): #выполняется цикл по всем страницам с камерами в указанной стране. И вывод ip камер на экран
        res = requests.get(f"http://www.insecam.org/en/bycountry/{country}/?page={page}",
                                 headers=headers)
        find_ip = re.findall(r"http://\d+.\d+.\d+.\d+:\d+", res.text)

        for ip in find_ip:
            print(f"{Fore.RED}[{i}]{Fore.RESET}", ip)
            print("")
            i+=1

except Exception as ex:
    print(Fore.RED + "Something ERROR :(")
    print(ex)
finally:
    exit()