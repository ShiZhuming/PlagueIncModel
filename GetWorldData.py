from bs4 import BeautifulSoup
import requests
import time

def sync():
    save_dir = r'D:\MyData\Python\2019-nCoV\data'
    url = 'https://www.worldometers.info/coronavirus/country/'
    countries = ['italy', 'germany', 'us', 'south-korea', 'iran', 'france', 'spain', 'uk', 'turkey', 'switzerland']
    curr_datas = []
    for country in countries:
        print("\n{}".format(country))
        r = requests.get(url+country+'/')
        demo = r.text  # 服务器返回响应
        soup = BeautifulSoup(demo, "html.parser")
        soup_text = soup.find_all('script', type='text/javascript')
        find_curr = False
        find_case = False
        find_death = False
        for _ in soup_text:
            if 'Currently Infected' in str(_) and not find_curr:
                curr = eval(str(_).split('#00DDDD')[-1].split('data:')[-1].split('responsive')[0].split('}')[0].strip())
                find_curr = True
                print('Currently Infected', curr)  # 输出响应的html对象
            elif 'Cases' in str(_) and not find_case:
                case = eval(str(_).split("'Cases'")[-1].split('data:')[-1].split('responsive')[0].split('}')[0].strip())
                find_case = True
                print('Cases', case)  # 输出响应的html对象
            elif 'Deaths' in str(_) and not find_death:
                death = eval(str(_).split('Deaths')[-1].split('data:')[-1].split('responsive')[0].split('}')[0].strip())
                find_death = True
                print('Deaths', death)  # 输出响应的html对象
        curr_datas.append(curr)
        with open("{}\{}.txt".format(save_dir, country), 'w') as country_file:
            country_file.write('Day\tCurrent\tTotal\tDeath\n')
            for _ in range(len(curr)):
                country_file.write('{}\t{}\t{}\t{}\n'.format(_ + 1, curr[_], case[_], death[_]))
        for _ in range(30):
            print('\rwaiting for {}s'.format(30 - _), flush=True, end='')
            time.sleep(1)
    with open("{}\\total_data.txt".format(save_dir), 'w') as data_f:
        for _ in range(len(countries)):
            if countries[_] == 'south-korea':
                country_name = 'south_korea'
            else:
                country_name = countries[_]
            data_f.write('I_{}={}\n'.format(country_name, curr_datas[_]))
    print('\nsync complete')


if __name__ == "__main__":
    sync()
