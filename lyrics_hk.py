"""lyrics classifier
This script scrapes mojim.com using beautifulsoup or scrapy, uses the information 
for a naive bayes classifier to predict the artist given the lyrics.
"""
import requests
import re
import numpy as py
import jieba
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from IPython.display import clear_output
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from fuzzywuzzy import fuzz
import plotly.express as px
from os import system, name
import argparse
from time import sleep

FEATURED_ARTIST = [
    "王光良",
    "朱頭皮",
    "老爹",
    "王建傑",
    "文揚",
    "阮小弟",
    "方力申",
    "方大同",
    "王識賢",
    "王中平",
    "老蕭",
    "伍思凱",
    "老孫",
    "任賢齊",
    "王力宏",
    "伊麵",
    "伍佰",
    "古巨基",
    "王傑",
]


def myscrape():
    """
    Scrapes Mojim.com using BeautifulSoup. Separate function using scrapy is available,
    see /hklyricsscrapper for more details. Returns None
    """
    s = requests.Session()
    response = s.get("https://mojim.com/twh100183.htm")
    response = BeautifulSoup(response.text, "html.parser")
    # scraping
    website_artist_list = [
        "https://mojim.com/twzlha_02.htm",
        "https://mojim.com/twzlha_03.htm",
        "https://mojim.com/twzlha_04.htm",
        "https://mojim.com/twzlha_05.htm",
        "https://mojim.com/twzlha_06.htm",
        "https://mojim.com/twzlha_07.htm",
        "https://mojim.com/twzlhb_02.htm",
        "https://mojim.com/twzlhb_03.htm",
        "https://mojim.com/twzlhb_04.htm",
        "https://mojim.com/twzlhb_05.htm",
        "https://mojim.com/twzlhb_06.htm",
        "https://mojim.com/twzlhb_07.htm",
        "http://mojim.com/twzlhc_28.htm",
        "http://mojim.com/twzlhc_29.htm",
        "http://mojim.com/twzlhc_30.htm",
        "http://mojim.com/twzlhc_31.htm",
        "http://mojim.com/twzlhc_32.htm",
        "http://mojim.com/twzlhc_33.htm",
    ]
    df_name_list = [
        "df_M2.csv",
        "df_M3.csv",
        "df_M4.csv",
        "df_M5.csv",
        "df_M6.csv",
        "df_M7.csv",
        "df_F2.csv",
        "df_F3.csv",
        "df_F4.csv",
        "df_F5.csv",
        "df_F6.csv",
        "df_F7.csv",
        "df_G28.csv",
        "df_G29.csv",
        "df_G30.csv",
        "df_G31.csv",
        "df_G32.csv",
        "df_G33.csv",
    ]
    for artist_list_i, current_artist_list in enumerate(website_artist_list):
        response = s.get(current_artist_list)
        response = BeautifulSoup(response.text, "html.parser")
        dd_class_name_list = ["hb2", "hb3"]
        span_class_name_list = ["hc3", "hc4"]
        song_artist = []
        song_name = []
        song_lyrics = []
        problem_artist = []
        home_url = "https://mojim.com"
        artist_list = response.find_all("ul", attrs={"class": "s_listA"})[0].find_all(
            "a"
        )
        for i1, current_artist in enumerate(artist_list):
            clear_output()
            print(df_name_list[artist_list_i])
            artist_url = current_artist["href"]
            artist_name = current_artist.text
            current_url = home_url + artist_url
            response = s.get(current_url)
            response = BeautifulSoup(response.text, "html.parser")
            album_url_list = []
            try:
                if (
                    len(
                        response.find_all("div", id="inS")[0]
                        .find_all("span", attrs={"class": "hd4"})[0]
                        .find_all("a")
                    )
                    != 0
                ):
                    for album_url in (
                        response.find_all("div", id="inS")[0]
                        .find_all("span", attrs={"class": "hd4"})[0]
                        .find_all("a")
                    ):
                        album_url_list.append(album_url["href"])
                else:
                    album_url_list = [artist_url]
            except:
                problem_artist.append(current_artist)
            for album_url in album_url_list:
                for dd_class_name in dd_class_name_list:
                    current_url = home_url + album_url
                    response = s.get(current_url)
                    response = BeautifulSoup(response.text, "html.parser")
                    dd_list = response.find_all("dd", attrs={"class": dd_class_name})
                    for current_dd in dd_list:
                        for span_class_name in span_class_name_list:
                            span_list = current_dd.find_all(
                                "span", attrs={"class": span_class_name}
                            )
                            for current_span in span_list:
                                a_list = current_span.find_all("a")
                                i = 0
                                while i <= len(a_list) - 1:
                                    if i + 1 <= len(a_list) - 1:
                                        if a_list[i + 1].text != "(提供)":
                                            print(
                                                "artist ",
                                                i1 + 1,
                                                " of ",
                                                len(artist_list) + 1,
                                            )
                                            song_url = a_list[i]["href"]
                                            current_url = home_url + song_url
                                            response = s.get(current_url)
                                            response = BeautifulSoup(
                                                response.text, "html.parser"
                                            )
                                            song_name.append(a_list[i].text)
                                            song_artist.append(artist_name)
                                            song_lyrics.append(
                                                response.find_all(
                                                    "dd", attrs={"id": "fsZx3"}
                                                )[0]
                                            )
                                            i += 1
                                        elif i + 2 <= len(a_list) - 1:
                                            i += 2
                                        else:
                                            break
                                    else:
                                        print(
                                            "artist ",
                                            i1 + 1,
                                            " of ",
                                            len(artist_list) + 1,
                                        )
                                        song_url = a_list[i]["href"]
                                        current_url = home_url + song_url
                                        response = s.get(current_url)
                                        response = BeautifulSoup(
                                            response.text, "html.parser"
                                        )
                                        song_name.append(a_list[i].text)
                                        song_artist.append(artist_name)
                                        song_lyrics.append(
                                            response.find_all(
                                                "dd", attrs={"id": "fsZx3"}
                                            )[0]
                                        )
                                        i += 1
        df_temp = pd.DataFrame(
            {"Artist": song_artist, "Song name": song_name, "Lyrics": song_lyrics}
        )
        df_temp.to_csv(df_name_list[artist_list_i])
    return None


def feature_engineering(df_in):
    """Feature engineering for the chinese lyrics to be processed by TFIDF"""
    df_temp = df_in.copy()
    # cleaning the lyrics
    bin = []
    for string in df_temp["Lyrics"]:
        if "作曲" in string:
            string = string.split("作曲")[1].split("<br/>", 1)[1]
        if "編曲" in string:
            string = string.split("編曲")[1].split("<br/>", 1)[1]
        if "監製" in string:
            string = string.split("監製")[1].split("<br/>", 1)[1]
        if "演唱" in string and not ("演唱會" in string):
            string = string.split("演唱")[1].split("<br/>", 1)[1]
        if "原唱" in string:
            string = string.split("原唱")[1].split("<br/>", 1)[1]
        if "[" in string:
            string = string.split("[")[0]
        string = re.sub("<br/>", " ", string)
        string = re.sub(
            '更多更詳盡歌詞 在 <a href="http://mojim.com">※ Mojim.com　魔鏡歌詞網 </a>', "", string,
        )
        string = re.sub(" \n</dd>", "", string)
        string = re.sub('<dd class="fsZx3" id="fsZx3">', "", string)
        string = re.sub(r"[^\u4e00-\u9fff]+", " ", string)
        string = re.sub("感謝 提供歌詞 友站連結", "", string)
        string = re.sub("感謝 修正歌詞", "", string)
        string = re.sub("純音樂", "", string)
        string = string.lstrip().rstrip()
        bin.append(string)
    df_temp["Lyrics"] = bin
    # segmentize the lyrics
    bin = []
    for string in df_temp["Lyrics"]:
        clear_output()
        seg_list = list(jieba.cut(string, cut_all=False))
        string = " ".join([i.strip() for i in seg_list])
        bin.append(string)
    df_temp["Lyrics"] = bin
    # add a space to every word
    df_temp["Lyrics"] = df_temp["Lyrics"].str.strip()
    df_temp["Lyrics"] = df_temp["Lyrics"].str.join(" ")
    df_temp.dropna(inplace=True)
    df_temp.drop(df_temp[df_temp["Lyrics"].str.len() < 20].index, inplace=True)

    i = 0

    while i + 1 <= df_temp.shape[0] - 1:
        if fuzz.ratio(df_temp.iloc[i]["Lyrics"], df_temp.iloc[i + 1]["Lyrics"]) > 80:
            df_temp.drop(df_temp.iloc[i].name, inplace=True)
            continue
        i += 1
    return df_temp


def clear():
    """This function clears the command prompt"""
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def plotting(artist_to_be_plotted):
    """for plotting a plotly pie chart of word occurence for an artist"""
    word_count_group = (
        df_test.groupby(["Artist"])[["Lyrics"]]
        .sum()["Lyrics"]
        .str.split(expand=True)
        .stack()
    )

    df = pd.DataFrame(word_count_group)

    temp = list(zip(*list(df.index)))[0]
    df.reset_index(inplace=True)
    df["Artist"] = temp

    df.rename(columns={0: "Lyrics"}, inplace=True)
    df.drop(columns=["level_1"], inplace=True)
    # matplotlib.rcParams['font.family'] = ['SoukouMincho']
    df_toplot = pd.DataFrame(
        df.groupby(["Artist"]).get_group(artist_to_be_plotted)["Lyrics"].value_counts()
    )
    df_toplot.reset_index(inplace=True)

    fig = px.pie(
        df_toplot,
        values="Lyrics",
        names="index",
        title=f"Occurence of words for songs of {artist_to_be_plotted}",
        width=800,
        height=800,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.show()
    return None


if __name__ == "__main__":
    clear()
    print("Hello, fitting the model......")

    parser = argparse.ArgumentParser(
        description="This program is going to give you a guess of an artist given an input of lyrics"
    )

    df_M3 = pd.read_csv("df_M3.csv", index_col=0)
    df_M3.head(3)
    # df_M3["Artist"].value_counts().sort_values().tail(5).keys()
    df_test = df_M3[df_M3["Artist"].isin(FEATURED_ARTIST)].copy()
    df_test = feature_engineering(df_test)
    X = df_test[["Lyrics"]]
    y = df_test["Artist"]
    ros = RandomOverSampler(random_state=0)
    Tfidf = TfidfVectorizer(
        max_features=10000, min_df=1, token_pattern="(?u)\w+", ngram_range=(1, 4)
    )
    X_vec = Tfidf.fit_transform(X["Lyrics"])

    print("Almost there......")
    X_train_vec, X_test_vec, y_train, y_test = train_test_split(
        X_vec, y, train_size=0.8
    )
    X_train_vec, y_train = ros.fit_resample(X_train_vec, y_train)
    nb = MultinomialNB(alpha=1)
    nb.fit(X_train_vec, y_train)

    print("Train score:", nb.score(X_train_vec, y_train))
    print("Test score:", nb.score(X_test_vec, y_test))

    sleep(5)
    clear()
    while True:
        print("The list of featured artists are as below:")
        print(" ".join(FEATURED_ARTIST))
        lyrics_in = input("Please input your lyrics (enter q to quit): ")

        if lyrics_in == "q":
            break
        lyrics_in
        NEW_SONGS = [lyrics_in]
        NEW_SONGS
        df_temp2 = pd.DataFrame({"Lyrics": NEW_SONGS})
        df_temp2_fe = feature_engineering(df_temp2)
        new_vec = Tfidf.transform(df_temp2_fe["Lyrics"])

        print("The model's guess is: ".join(nb.predict(new_vec)))
        print("")
