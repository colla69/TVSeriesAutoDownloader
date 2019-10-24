# -*- coding: utf-8 -*-
from src.context import *
import mechanicalsoup
import time
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def download_videos_todo(todo_list, output):
    for s in todo_list:
        e_output = _enrich_output_path(s, output)
        done_output = output+"done/"
        if not os.path.exists(done_output):
            os.mkdir(done_output)
        done_files = os.listdir(done_output)
        for e in s.epis:
            no = e[0]
            link = e[1]
            file_name = "{} S{} E{}.mp4".format(s.name, s.s_no, no)
            if file_name not in done_files:
                _download_from_epi_page(link, e_output, file_name, done_output)


def _enrich_output_path(s, output):
    subdir = "{}/".format(s.name)
    output += subdir
    if not os.path.exists(output):
        os.mkdir(output)
    subdir = "s{}/".format(s.s_no)
    output += subdir
    if not os.path.exists(output):
        os.mkdir(output)
    return output


def __try_vidoza(soup, output, title, done_output):
    lines = soup.find_all("a", class_="watchlink")
    # lines.remove(lines[0])
    done = False
    for link in lines:
        sublink = link["href"]
        bs64 = sublink[sublink.find("r=") + 2:]
        try:
            link = base64.b64decode(bs64)
            if "vidoza.net" in str(link):
                # print(link)
                try:
                    d = requests.get(link).text
                    v = BeautifulSoup(d, 'html.parser')
                    d_link = v.find("source")["src"]
                    r = requests.head(d_link)
                    if r.status_code != 200:
                        continue
                except Exception as e:
                    # print(e)
                    continue
                print("Downloading {} from:\n\t{}".format(title, d_link))
                download_link(output, title, done_output, d_link)
                print("Done!\n")
                return "done"
        except Exception as e:
            # print(e)
            # print(link)
            continue
    print("\tnothing from vidoza")
    return None


def __try_vshare(soup, output, title, done_output):
    lines = soup.find_all("a", class_="watchlink")
    brow = mechanicalsoup.StatefulBrowser()
    for link in lines:
        sublink = link["href"]
        bs64 = sublink[sublink.find("r=")+2:]
        try:
            link = base64.b64decode(bs64)
            if "vshare.eu" in str(link):
                # print(link)
                try:
                    brow.open(link)
                    brow.get_current_page()
                    brow.select_form('form')
                    brow.submit_selected()
                    p = brow.get_current_page()
                    d_link = p.find(["source"])["src"]
                    r = requests.head(d_link)
                    if r.status_code != 200:
                        continue
                except Exception as e:
                    # print(e)
                    continue
                print("Downloading {} from:\n\t{}".format(title, d_link))
                download_link(output, title, done_output, d_link)
                print("Done!\n")
                return "Done"
        except Exception as e:
            #print(e)
            #print(link)
            continue
    print("\tnothing from vshare")
    return None


def __try_onlystream(soup, output, title, done_output):
    lines = soup.find_all("a", class_="watchlink")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    for link in lines:
        sublink = link["href"]
        bs64 = sublink[sublink.find("r=")+2:]
        try:
            link = base64.b64decode(bs64)
            if "onlystream.tv" in str(link):
                # print(link)
                try:
                    driver.get(str(link.decode()))
                    time.sleep(1)
                    bu = driver.find_elements_by_class_name("btn-go")
                    driver.execute_script("arguments[0].click();", bu[2])
                    time.sleep(1)
                    btns = driver.find_elements_by_class_name("btn-go")
                    d_link = btns[0].get_attribute("href")
                    # print(d_link)
                    r = requests.head(d_link)
                    if r.status_code != 200:
                        continue
                except Exception as e:
                    # print(e)
                    continue
                print("Downloading {} from:\n\t{}".format(title, d_link))
                download_link(output, title, done_output, d_link)
                print("Done!\n")
                driver.quit()
                return "Done"
        except Exception as e:
            # print(e)
            # print(link)
            continue
    driver.quit()
    print("\tnothing from onlystream")
    return None


def __try_vidtodo(soup, output, title, done_output):
    lines = soup.find_all("a", class_="watchlink")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    for link in lines:
        sublink = link["href"]
        bs64 = sublink[sublink.find("r=")+2:]
        try:
            link = base64.b64decode(bs64)
            if "vidtodo.com" in str(link):
                try:
                    driver.get(str(link.decode()))
                    time.sleep(10)
                    bu = driver.find_elements_by_class_name("vjs-big-play-button")
                    driver.execute_script("arguments[0].click();", bu[0])
                    vid = driver.find_elements_by_class_name("vjs-tech")
                    d_link = vid[0].get_attribute("src")
                    r = requests.head(d_link)
                    if r.status_code != 200:
                        continue
                except Exception as e:
                    continue
                print("Downloading {} from:\n\t{}".format(title, d_link))
                download_link(output, title, done_output, d_link)
                print("Done!\n")
                driver.quit()
                return "Done"
        except Exception as e:
            # print(e)
            # print(link)
            continue
    driver.quit()
    print("\tnothing from vidtodo")
    return None


def _download_from_epi_page(plink, output, title, done_output):
    print("searching for {}".format(title))
    page = requests.get(plink)
    soup = BeautifulSoup(page.text, 'html.parser').find("div", id="linktable")
    # print(soup.prettify())
    done = __try_vidtodo(soup, output, title, done_output) or \
           __try_onlystream(soup, output, title, done_output) or \
           __try_vidoza(soup, output, title, done_output) or \
           __try_vshare(soup, output, title, done_output)
    if not done:
        print("couldn't find anything to Download\n")


def download_link(output, title, done_output, d_link):
    FNULL = open(os.devnull, 'w')
    cmd = 'wget -q -O "{}" {} && touch "{}"'.format(output + title, d_link, done_output + title)
    print("executing: \n\t{}".format(cmd))
    subprocess.Popen(cmd, shell=True, stdout=FNULL)


def check_downloading():
    print("\nwaiting for Downloads")
    out = "running"
    count = 0
    while out:
        count += 1
        p = subprocess.Popen("ps ax | grep -i wget | grep -v grep", stdout=subprocess.PIPE, shell=True)
        out = p.stdout.read()
        sys.stdout.write('.')
        if count % 200 == 0:
            sys.stdout.write('\n')
        sys.stdout.flush()
        time.sleep(5)
    print("\nall done!")

