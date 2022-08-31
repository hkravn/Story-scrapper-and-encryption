import os
import pandas as pd
import encode_decode
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import story_scrapper2
from tqdm import tqdm

file_lis = []
url_lis = []
csvfile = "urllist.csv"
basepath = os.path.abspath(os.getcwd()) + "\\stories\\"

'''
test = [['', '', '', '', '', '', '', '', '']]
df = pd.DataFrame(data=test, columns=['URL', 'Story-Name', 'Author-Name', 'Description', 'Def-Rating',
                                      'Pers-Rating', 'Saved', 'Encrypted'])
'''

df = pd.read_csv(csvfile, index_col='Sl No', encoding='utf-8', dtype='object')

'''req_proxy = RequestProxy()
proxies = req_proxy.get_proxy_list()
PROXY = proxies[0].get_address()
print(PROXY)'''
PROXY = "46.216.255.225:8118"

with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.name.find('txt') != -1:
            file_lis.append(entry.name)


while True:
    user_choice = input("Do you want to:\n 1)Encode Stories\n 2)Decode Stories\n 3)"
                        "Add URL\n 4)Check for Duplicates\n 5)Update Stories\n 6)Update Basic Information\n 7)Exit\n :")
    if user_choice == '7':
        df.to_csv(csvfile, index=True, index_label='Sl No', encoding='utf-8')
        break
    if user_choice == '1':
        for file in tqdm(file_lis):
            encode_decode.encryption(basepath + file)
    if user_choice == '2':
        for file in tqdm(file_lis):
            encode_decode.decryption(basepath + file)
    if user_choice == '3':
        print("Enter URL:")
        df = df.append({'URL': input()}, ignore_index=True)
    if user_choice == '4':
        duplicaterows = df[df.duplicated(['URL', 'Story-Name', 'Author-Name'])]
        print(f"Total duplicates in url's: {duplicaterows.count()}")
        df.drop_duplicates(subset='URL', keep='last', inplace=True)
        df.reset_index(drop=True, inplace=True)
    if user_choice == '5':
        df1 = pd.isna(df['Saved'])
        df2 = df[df1]['URL']
        print(f"To Update links: {df2.count()}")
        for d in df2:
            s = story_scrapper2.update_story_file(d, PROXY)
            if s:
                loc = df[df['URL'] == d].index.values
                df.at[loc[0], 'Saved'] = 'Y'
                df.to_csv(csvfile, index=True, index_label='Sl No', encoding='utf-8')
            else:
                loc = df[df['URL'] == d].index.values
                df.at[loc[0], 'Saved'] = 'N'
                df.to_csv(csvfile, index=True, index_label='Sl No', encoding='utf-8')
    if user_choice == '6':
        df1 = pd.isna(df['Story-Name'])
        df2 = df[df1]['URL']
        print(f"To Update links: {df2.count()}")
        for d in tqdm(df2):
            s = story_scrapper2.update_info(d)
            if s:
                loc = df[df['URL'] == d].index.values
                df.at[loc[0], 'Author-Name'] = s[0]
                df.at[loc[0], 'Story-Name'] = s[1]
                df.to_csv(csvfile, index=True, index_label='Sl No', encoding='utf-8')
