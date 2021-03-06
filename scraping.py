# import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import datetime
from assets.database import db_session
from assets.models import Data
import time

# Indeedのリンク（国別）
japan = {
    'python': 'https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q=python&l=',
    'javascript': 'https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q=javascript&l=',
    'php': 'https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q=php&l=',
    'ruby': 'https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q=ruby&l=',
    'c': 'https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q=C%2B%2B&l=',
    'java': 'https://jp.indeed.com/jobs?q=java&l='
}
canada = {
    'python': 'https://ca.indeed.com/jobs?q=python&l=',
    'javascript': 'https://ca.indeed.com/jobs?q=javascript&l=',
    'php': 'https://ca.indeed.com/jobs?q=php&l=',
    'ruby': 'https://ca.indeed.com/jobs?q=ruby&l=',
    'c': 'https://ca.indeed.com/jobs?q=c%2B%2B&l=',
    'java': 'https://ca.indeed.com/jobs?q=java&l='
}
usa = {
    'python': 'https://www.indeed.com/jobs?q=python&l=',
    'javascript': 'https://www.indeed.com/jobs?q=javascript&l=',
    'php': 'https://www.indeed.com/jobs?q=php&l&vjk=e183fb63ca24c7b7',
    'ruby': 'https://www.indeed.com/jobs?q=ruby&l&vjk=9db28d28c8660a25',
    'c': 'https://www.indeed.com/jobs?q=c%2B%2B&l&vjk=f0a6715db8bd92b7',
    'java': 'https://www.indeed.com/jobs?q=java&l&vjk=cb10955439ed26fb'
}
australia = {
    'python': 'https://au.indeed.com/jobs?q=python&l=',
    'javascript': 'https://au.indeed.com/jobs?q=javascript&l=',
    'php': 'https://au.indeed.com/jobs?q=php&l=',
    'ruby': 'https://au.indeed.com/jobs?q=ruby&l=',
    'c': 'https://au.indeed.com/jobs?q=c%2B%2B&l=',
    'java': 'https://au.indeed.com/jobs?q=java&l='
}
singapore = {
    'python': 'https://sg.indeed.com/jobs?q=python&l=',
    'javascript': 'https://sg.indeed.com/jobs?q=javascript&l=',
    'php': 'https://sg.indeed.com/jobs?q=php&l=',
    'ruby': 'https://sg.indeed.com/jobs?q=ruby&l=',
    'c': 'https://sg.indeed.com/jobs?q=c%2B%2B&l=',
    'java': 'https://sg.indeed.com/jobs?q=java&l='
}
newzealand = {
    'python': 'https://nz.indeed.com/jobs?q=python&l=',
    'javascript': 'https://nz.indeed.com/jobs?q=javascript&l=',
    'php': 'https://nz.indeed.com/jobs?q=php&l=',
    'ruby': 'https://nz.indeed.com/jobs?q=ruby&l=',
    'c': 'https://nz.indeed.com/jobs?q=c%2B%2B&l=',
    'java': 'https://nz.indeed.com/jobs?q=java&l='
}

# Write_data()にあげる
Countries_LanguagesLinks = {'japan': japan, 'canada': canada, 'usa': usa,
                            'australia': australia, 'singapore': singapore, 'newzealand': newzealand}


def get_number(Country_LanguagesLinks):

    results = {}
    country = Country_LanguagesLinks[0]
    LanguagesLinks = Country_LanguagesLinks[1]

    for language, link in LanguagesLinks.items():
        # 日本と英語圏だと抽出方法が変わるのでif文追加
        if country == 'japan':
            url = link
            r_url = requests.get(url)
            time.sleep(1)
            soup = BeautifulSoup(r_url.text, 'html.parser')
            offer = soup.select('#searchCountPages')[0].string.split('果')[1]
            offer = int(offer.split('件')[0].replace(",", ""))
            results[language] = offer

        elif country == 'canada' or 'usa' or 'australia' or 'singapore' or 'newzealand':
            url = link
            r_url = requests.get(url)
            time.sleep(1)
            soup = BeautifulSoup(r_url.text, 'html.parser')
            offer = soup.select('#searchCountPages')[0].string.split('of')[1]
            offer = int(offer.split('jobs')[0].replace(",", ""))
            results[language] = offer

    return results


def write_data():
    # 世界項目用のtotal
    total_python = 0
    total_javascript = 0
    total_php = 0
    total_ruby = 0
    total_c = 0
    total_java = 0

    # for文で国別・言語別にデータを抽出しデータベースに保存。世界項目用にtotalに足していく
    for Country_LanguagesLinks in Countries_LanguagesLinks.items():
        country = Country_LanguagesLinks[0]
        _results = get_number(Country_LanguagesLinks)
        row = Data(date=datetime.datetime.today(), country=country, python=_results["python"], javascript=_results[
                   "javascript"], php=_results["php"], ruby=_results["ruby"], c=_results["c"], java=_results["java"])
        db_session.add(row)
        total_python += _results["python"]
        total_javascript += _results["javascript"]
        total_php += _results["php"]
        total_ruby += _results["ruby"]
        total_c += _results["c"]
        total_java += _results["java"]

    # 世界用のデータ
    row = Data(date=datetime.datetime.today(), country='world', python=total_python,
               javascript=total_javascript, php=total_php, ruby=total_ruby, c=total_c, java=total_java)
    db_session.add(row)
    db_session.commit()


if __name__ == "__main__":
    write_data()
