import requests
import string
import pandas as pd
import numpy as np
import ast
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import random


if __name__ == '__main__':
    #INICJALIZACJA DLA STRONY - NIE RUSZAC!
    id_p = 0
    id_web = 0
    HEADERS = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate',
            'authority': 'whoscored.com',
            'Accept-Language':'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'DNT':'1',
            'Host': 'www.google.com',
            'Pragma':'no-cache',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'cookie': 'IDE=AHWqTUkj1_W8zwb-1dcpYEWmPifNcsWNRR3N61Db8ZQRVboRo505eKWhP5d41ZPGWlI; DSID=NO_DATA',
    }
    PROXIES = {
        'http': 'none',
        'https': 'none',
    }
    prox=['51.158.123.35:9999','159.8.114.34:8123']
    # prox=['167.172.184.166:38318','167.172.191.249:34327','157.230.103.189:36366','168.119.137.56:3128','165.22.81.30:37344']
    USER_AGENT_LIST = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
        'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
    ]
    ##########################################

    #linki do lig z ktorych chcemy brac statystyki graczy (zmieńcie linki z https na http plus podajcie konkretny link do player statistics)
    linki_player_statistics = ['http://www.whoscored.com/Regions/252/Tournaments/2/Seasons/8228/Stages/18685/PlayerStatistics/England-Premier-League-2020-2021',
              'http://www.whoscored.com/Regions/81/Tournaments/3/Seasons/8279/Stages/18762/PlayerStatistics/Germany-Bundesliga-2020-2021',
              'http://www.whoscored.com/Regions/250/Tournaments/12/Seasons/8177/Stages/19130/PlayerStatistics/Europe-Champions-League-2020-2021',
              'http://www.whoscored.com/Regions/250/Tournaments/30/Seasons/8178/Stages/19164/PlayerStatistics/Europe-Europa-League-2020-2021']

    #Jezeli dodajecie / odejmujecie ligi wyzej to tutaj trzeba je dodac/ usunac jako samą nazwę
    allowed_leagues = ['Premier League', 'Bundesliga', 'Champions League', 'Europa League']


    player_match = []
    player_covered = []
    for x in linki_player_statistics:
        choice = random.choice(prox)
        PROXIES['https'] = choice
        PROXIES['http'] = choice


        ######## Przygotowanie strony
        time.sleep(5)
        options = webdriver.ChromeOptions()
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chrome_driver_binary = r"D:\SEMESTR_5\Inż\Poler-Bijaj\chromedriver.exe"
        browser = webdriver.Chrome(chrome_driver_binary, options=options)
        browser.switch_to.window(browser.window_handles[-1])

        browser.get(x)
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
        time.sleep(1)
        browser.execute_script('document.querySelector("#apps > dd:nth-child(2) > a").click()')
        time.sleep(2)

        #Wyliczanie stron
        #jesli potrzebne odkomentować
        pages = browser.find_element_by_xpath('//*[@id="statistics-paging-summary"]/div/dl[2]/dt/b').text
        pages = str(pages).split('|')[0]
        pages = str(pages).replace('Page ','')
        pages = int(pages.split('/')[1])

        # jesli wiecej wszystkie rekordy odkomentowac i zakomentowac na dole
        for page in range(pages-1):
        # for i in range(1):

            #pobieranie graczy
            players_xpath = '//*[@id="player-table-statistics-body"]/tr/td[1]/a[1]'
            #pobieranie ligi
            leaguename = browser.find_element_by_xpath('//*[@id="stage-top-player-stats"]/div[1]/h2')
            leaguename = str(leaguename.text).replace(' Player Statistics','')
            if leaguename == '1. Bundesliga':
                leaguename = leaguename.replace('1. ','')
            if leaguename == '2. Bundesliga':
                leaguename = leaguename.replace('2. ', '')

            #pobieranie graczy z xpatha
            players = browser.find_elements_by_xpath(players_xpath)
            #for po graczach
            for p in range(len(players)):
                #pobieranie linku z jego imienia
                # player-table-statistics-body > tr:nth-child(1) > td.col12-lg-2.col12-m-3.col12-s-4.col12-xs-5.grid-abs.overflow-text > a.player-link > span
                # player-table-statistics-body > tr:nth-child(1) > td.col12-lg-2.col12-m-3.col12-s-4.col12-xs-5.grid-abs.overflow-text > a.player-link > span
                name = browser.execute_script('return document.querySelector("#player-table-statistics-body > tr:nth-child({}) > td.col12-lg-2.col12-m-3.col12-s-4.col12-xs-5.grid-abs.overflow-text > a.player-link > span").outerText'.format(str(p+1)))
                if name not in player_covered:
                    players = browser.find_elements_by_xpath(players_xpath)
                    link = players[p].get_property('href')
                    link = link.replace('https:', 'http:')

                    #otwieranie nowej karty i przełączanie na nia
                    browser.execute_script("window.open('"+link+"');")
                    browser.switch_to.window(browser.window_handles[-1])

                    #pobieranie zakładek
                    player_match_stats_xpath = '//*[@id="sub-navigation"]/ul/li[2]/a'
                    player_match_stats = browser.find_element_by_xpath(player_match_stats_xpath).get_property('href')
                    country_xpath = '//*[@id="layout-wrapper"]/div[3]/div[1]/div[1]/div[2]/div[2]/div[6]/span[2]/text()'
                    deffensive_xpath = '//*[@id="player-matches-stats-options"]/li[2]/a'
                    offensive_xpath = '//*[@id="player-matches-stats-options"]/li[3]/a'
                    tournaments_xpath = '//*[@id="tournamentOptions"]/dd/a'


                    #przejscie do match statistic
                    browser.get(player_match_stats)
                    #pobieranie lig gracza
                    leagues = browser.find_elements_by_xpath(tournaments_xpath)
                    leagues = [item.text for item in leagues]



                    #zmienne pod dane gracza
                    player_name = ""
                    team = ""
                    age = ""
                    country = ""
                    #pobieranie wszystkich danych gracza
                    infos = browser.find_elements_by_css_selector('#layout-wrapper > div.sticky-unit-wrapper > div.main-content-column > div.header > div.col12-lg-12.col12-m-12.col12-s-12.col12-xs-12 > div.col12-lg-10.col12-m-10.col12-s-9.col12-xs-8 > div')

                    #wybieranie konkretnych danych
                    for i in infos:
                        #print(i.text)
                        #print("___________")
                        if(i.text[0:5] == "Name:"):

                            player_name = i.text
                        elif(i.text[0:5] == "Curre"):
                            team = i.text
                        elif(i.text[0:5] == "Age: "):
                            age = i.text
                        elif(i.text[0:5] == "Natio"):
                            country = i.text

                    #przygotowanie danych gracza
                    player_name = player_name.replace("Name: ","")
                    team = team.replace('Current Team: ',"")
                    age = age.split('(')[0].replace("Age: ","")
                    age = age.replace(" years old","")
                    country = country.replace('Nationality: ','')

                    #jezeli gracz juz mial pobierane dane
                    if(player_name not in player_covered):

                        print(player_name,team,age,country)

                        # usuwanie diva bo przez niego wywalało błąd
                        browser.execute_script('if(document.getElementById("qc-cmp2-container") != null){document.getElementById("qc-cmp2-container").remove()}')
                        #pobieranie lig i zamiana na tekst
                        leagues = browser.find_elements_by_xpath('/html/body/div[5]/div[4]/div[1]/div[1]/div[2]/dl[1]/dd/a')
                        leagues = [item.text for item in leagues]

                        for l in range(len(leagues)):
                            #jezeli liga to ta ktora szukamy
                            if leagues[l] in allowed_leagues:
                                browser.refresh()
                                time.sleep(1)

                                #zmiana zakladki i wybor ligi
                                browser.execute_script('document.querySelector("#player-matches-stats-options > li:nth-child(1) > a").click()')
                                time.sleep(2)
                                #usuwanie diva bo przez niego wywalało błąd
                                browser.execute_script('if(document.getElementById("qc-cmp2-container") != null ){document.getElementById("qc-cmp2-container").remove()}')
                                tmp = browser.find_elements_by_xpath('/html/body/div[5]/div[4]/div[1]/div[1]/div[2]/dl[1]/dd/a')
                                tmp[l].click()
                                time.sleep(1)

                                # summary
                                Opponent_xpath = browser.find_elements_by_xpath('//*[@id="player-table-statistics-body"]/tr/td[1]/a')
                                wynik_druzyny_g = browser.find_elements_by_xpath('//*[@id="player-table-statistics-body"]/tr/td[1]/a/span/span[1]')
                                wynik_druzyny_p = browser.find_elements_by_xpath('//*[@id="player-table-statistics-body"]/tr/td[1]/a/span/span[3]')
                                data = browser.find_elements_by_class_name('date')
                                mins_xpath = browser.find_elements_by_class_name('minsPlayed')
                                goals_xpath = browser.find_elements_by_class_name('goalTotal')
                                assists_xpath = browser.find_elements_by_class_name('assist')
                                yellow_xpath = browser.find_elements_by_class_name('yellowCard')
                                red_xpath = browser.find_elements_by_class_name('redCard')
                                shots_xpath = browser.find_elements_by_class_name('shotsTotal')
                                pass_xpath = browser.find_elements_by_class_name('passSuccess')
                                duel_xpath = browser.find_elements_by_class_name('duelAerialWon')
                                rating_xpath = browser.find_elements_by_class_name('rating')

                                #zamiana obiektow na tekst
                                Opponent_xpath2 = [item.text.split('(')[1] for item in Opponent_xpath]
                                Opponent_xpath = [item.text.split('(')[0] for item in Opponent_xpath]
                                wynik_druzyny_g = [item.text for item in wynik_druzyny_g]
                                wynik_druzyny_p = [item.text for item in wynik_druzyny_p]
                                for o in range(len(Opponent_xpath2)):
                                    if(Opponent_xpath2[o][0] == "A"):
                                        tmp = wynik_druzyny_g[o]
                                        wynik_druzyny_g[o] = wynik_druzyny_p[o]
                                        wynik_druzyny_p[o] = tmp

                                data = [item.text for item in data]
                                mins_xpath = [item.text for item in mins_xpath]
                                goals_xpath = [item.text for item in goals_xpath]
                                assists_xpath = [item.text for item in assists_xpath]
                                yellow_xpath = [item.text for item in yellow_xpath]
                                red_xpath = [item.text for item in red_xpath]
                                shots_xpath = [item.text for item in shots_xpath]
                                pass_xpath = [item.text for item in pass_xpath]
                                duel_xpath = [item.text for item in duel_xpath]
                                rating_xpath = [item.text for item in rating_xpath]

                                # zamiana zakładki i wybór ligi
                                browser.execute_script(
                                    'document.querySelector("#player-matches-stats-options > li:nth-child(2) > a").click()')
                                time.sleep(2)
                                tmp = browser.find_elements_by_xpath('/ html / body / div[5] / div[4] / div[2] / div[1] / div[2] / dl[1] / dd / a')
                                tmp[l].click()
                                time.sleep(1)

                                #deffensive
                                tackles_xpath = browser.find_elements_by_class_name('tackleWon')
                                inter_xpath = browser.find_elements_by_class_name('interceptionAll')
                                fouls_xpath = browser.find_elements_by_class_name('foulCommitted')
                                offsides_xpath = browser.find_elements_by_class_name('offsideProvoked')
                                clear_xpath = browser.find_elements_by_class_name('clearanceTotal')
                                deff_drb_xpath = browser.find_elements_by_class_name('challengeLost')
                                blocks_xpath = browser.find_elements_by_class_name('outfielderBlock')
                                owng_xpath = browser.find_elements_by_class_name('goalOwn')

                                #zamiana z obiektow na tekst
                                tackles_xpath = [item.text for item in tackles_xpath]
                                inter_xpath = [item.text for item in inter_xpath]
                                fouls_xpath = [item.text for item in fouls_xpath]
                                offsides_xpath = [item.text for item in offsides_xpath]
                                clear_xpath = [item.text for item in clear_xpath]
                                deff_drb_xpath = [item.text for item in deff_drb_xpath]
                                blocks_xpath = [item.text for item in blocks_xpath]
                                owng_xpath = [item.text for item in owng_xpath]

                                #zamiana zakładki i wybór ligi
                                browser.execute_script(
                                    'document.querySelector("#player-matches-stats-options > li:nth-child(3) > a").click()')
                                time.sleep(2)
                                tmp = browser.find_elements_by_xpath('/ html / body / div[5] / div[4] / div[3] / div[1] / div[2] / dl[1] / dd / a')
                                tmp[l].click()
                                time.sleep(1)

                                #offensive
                                off_drb_xpath = browser.find_elements_by_class_name('dribbleWon')
                                off_xpath = browser.find_elements_by_class_name('offsideGiven')

                                # zamiana z obiektow na tekst
                                off_drb_xpath = [item.text for item in off_drb_xpath]
                                off_xpath = [item.text for item in off_xpath]

                                time.sleep(1)

                                for line in range(0,len(data)):
                                    #dodawanie danych do globalnej tablicy
                                    player_match.append([player_name,
                                                         age,
                                                         team,
                                                         country,
                                                         leagues[l],
                                                        Opponent_xpath[line],
                                                         wynik_druzyny_g[line],
                                                         wynik_druzyny_p[line],
                                                         data[line],
                                                         0 if (mins_xpath[line+1] == '-') else mins_xpath[line+1],
                                                         0 if (goals_xpath[line+1] == '-') else goals_xpath[line+1],
                                                         0 if (assists_xpath[line+1] == '-') else assists_xpath[line+1],
                                                         0 if (yellow_xpath[line+1] == '-') else yellow_xpath[line+1],
                                                         0 if (red_xpath[line+1] == '-') else red_xpath[line+1],
                                                         0 if (shots_xpath[line+1] == '-') else shots_xpath[line+1],
                                                         0 if (pass_xpath[line+1] == '-') else pass_xpath[line+1],
                                                         0 if (duel_xpath[line+1] == '-') else duel_xpath[line+1],
                                                         0 if (rating_xpath[line+1] == '-') else rating_xpath[line+1],
                                                         0 if (tackles_xpath[line+1] == '-') else tackles_xpath[line+1],
                                                         0 if (inter_xpath[line+1] == '-') else inter_xpath[line+1],
                                                         0 if (fouls_xpath[line+1] == '-') else fouls_xpath[line+1],
                                                         0 if (offsides_xpath[line+1] == '-') else offsides_xpath[line+1],
                                                         0 if (clear_xpath[line+1] == '-') else clear_xpath[line+1],
                                                         0 if (deff_drb_xpath[line+1] == '-') else deff_drb_xpath[line+1],
                                                         0 if (blocks_xpath[line+1] == '-') else blocks_xpath[line+1],
                                                         0 if (owng_xpath[line+1] == '-') else owng_xpath[line+1],
                                                         0 if (off_drb_xpath[line+1] == '-') else off_drb_xpath[line+1],
                                                         0 if (off_xpath[line+1] == '-') else off_xpath[line+1],
                                                         ])
                                #Wypychanie danych do csv (w razie bledu mamy chociaz jakas czesc danych)

                                #print(player_match)
                    #zamykanie karty i przejscie do odpowiedniej zakladki
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])
                    #dodawanie gracza do listy pobranych
                    if(player_name not in player_covered):
                        player_covered.append(player_name)
                    print("odwiedzeni: ", player_covered, " (",len(player_covered),")")

        #ile stron z listami graczy chcemy pobierać (i+1) * 10 - dla 0 pobieramy 10 graczy
        # if i == 0:
        #         break
        #przycisk od zmiany strony na kolejną
            browser.switch_to.window(browser.window_handles[-1])
            browser.execute_script("document.getElementById('next').click()")
            time.sleep(1)
            browser.switch_to.window(browser.window_handles[-1])
            pand = pd.DataFrame(player_match,
                                columns=['player_name', 'age', 'team', 'country', 'league', 'opponent',
                                         'wynik druzyny gracza', 'wynik druzyny przeciwnika', 'data', 'mins', 'goals',
                                         'assists', 'yel',
                                         'red', 'shots', 'pass', 'duel', 'rating', 'tackles', 'inter',
                                         'fouls', 'offsides', 'clear', 'deff', 'blocks', 'owng', 'off_drb',
                                         'off'])
            pand.to_csv('csv_statystyki.csv')
            time.sleep(3)


    browser.close()




