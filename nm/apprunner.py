# Copyright (C) 2016 Michał Góral.
#
# This file is part of NapiMan
#
# NapiMan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NapiMan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NapiMan. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import logging
import argparse
import re
import tempfile
import logging
import subprocess

import requests
import bs4
import guessit

from nm.util import abs_diff, nm_assert, ErrorCode, ExceptionWithCode
from nm.time import Time
from nm.datatypes import PageInfo, SubInfo, MovieInfo
from nm.printing import use_colors, underline, bold, red, purple, blue, green
from nm.version import __version__

log = logging.getLogger('NapiMan')

def prepare_parser():
    parser = argparse.ArgumentParser(description = "By-name, by-time subtitle downloader.")

    parser.add_argument("files", metavar = "FILE", nargs="+",
        type = os.path.expanduser, help="movie files to open")

    parser.add_argument("-t", "--title", metavar = "STRING", type = str, default = "",
        help = "force searching for a video with a given title")
    parser.add_argument("-s", "--season", metavar = "NUMBER", type = int, default = None,
        help = "force season number to be searched")
    parser.add_argument("-e", "--episode", metavar = "NUMBER", type = int, default = None,
        help = "force episode number to be searched")

    parser.add_argument("-m", "--manual", action = "store_true", dest = "manual_sub",
        help = "show a subtitle list to choose from")

    parser.add_argument("--no-color", action = "store_false", dest = "no_color",
        help = "don't color program output")

    parser.add_argument("--debug", action = "store_true", help = "enable debug printing")

    parser.add_argument("--version", action = "version",
            version = "%(prog)s %(version)s" % {"prog" : "%(prog)s", "version" : __version__},
            help = "print program version")

    return parser

def choose(list_, question):
    nm_assert(len(list_) > 0, "empty list")

    if len(list_) == 1:
        return list_[0]

    choice = None

    max_num = len("[%d]:" % len(list_))

    print()

    for no, item in enumerate(list_):
        needed_space = 1 + max_num - len("[%d]:" % int(no + 1))
        print("   %s[%s]: %s" % (' '.rjust(needed_space), purple(no + 1), str(item)))

    print()

    while True:
        choice = input("    %s ['q', '1-%d']: " % (question, len(list_)))

        if choice.lower() == "q":
            sys.exit(1)

        try:
            choice = int(choice)
            if choice > 0 and choice <= len(list_):
                return list_[choice - 1]
        except ValueError:
            pass

def parse_input(filename, args):
    title = os.path.basename(os.path.splitext(filename)[0])
    found_dict = guessit.guessit(title)

    title = found_dict.get("title", title)
    season = found_dict.get("season")
    episode = found_dict.get("episode")

    if args.title:
        title = args.title
    if args.season:
        season = args.season
    if args.episode:
        episode = args.episode

    return (title.strip(), season, episode)

def get_movie_pages(soup):
    ret = []

    for link in soup.find_all("a"):
        if "movieTitleCat" in link.get("class", []):
            i = PageInfo()
            i.url = link.get("href")
            i.name = link.text
            ret.append(i)

    return ret

def get_subtitles(soup):
    ret = []
    for tr in soup.find_all("tr"):
        if "Autor" in tr.get("title", ""):
            td_list = tr.find_all("td")

            if len(td_list) < 4:
                continue

            if td_list[0].a is None:
                continue

            try:
                info = SubInfo()

                info.sub_hash = td_list[0].a.get("href").strip()
                if info.sub_hash.startswith("napiprojekt:"):
                    info.sub_hash = info.sub_hash[12:]

                info.name = td_list[0].a.text.strip()
                info.time_info.fps = float(td_list[2].text.strip())
                info.time_info.length = Time(td_list[3].text.strip())
                ret.append(info)
            except Exception as e:
                log.debug(e)
                continue
    return ret

def get_movie_page_url(links, name, args):
    if (len(links) == 0):
        log.error("No movies found for a given query: '%s'" % name)
        sys.exit(1)

    page = choose(links, "Many video pages found, please choose one")
    correct_url = page.url.replace("napisy-", "napisy1,1,1-dla-")
    subpage_url = "http://www.napiprojekt.pl/%s" % correct_url

    return subpage_url

def add_season(url, season, episode):
    if season is not None:
        episode_info = "-s%02d" % season
        if episode is not None:
            episode_info = "%se%02d" % (episode_info, episode)
        return "%s%s" % (url, episode_info)
    return url

def get_movie_data(filename):
    command = ['mplayer',
        '-really-quiet', '-vo', 'null', '-ao', 'null', '-frames', '0', '-identify', filename]
    out = subprocess.check_output(command, stderr = subprocess.DEVNULL)

    ret = MovieInfo()
    ret.path = filename
    ret.time_info.fps = float(re.search(r'ID_VIDEO_FPS=([\w/.]+)\s?', str(out)).group(1))
    ret.time_info.length = Time(
        seconds = float(re.search(r'ID_LENGTH=([\w/.]+)\s?', str(out)).group(1)))
    return ret

def napi_f(z):
    idx = [ 0xe, 0x3,  0x6, 0x8, 0x2 ]
    mul = [   2,   2,    5,   4,   3 ]
    add = [   0, 0xd, 0x10, 0xb, 0x5 ]

    b = []
    for i in range(len(idx)):
        a = add[i]
        m = mul[i]
        i = idx[i]

        t = a + int(z[i], 16)
        v = int(z[t:t+2], 16)
        b.append( ("%x" % (v*m))[-1] )

    return ''.join(b)

def download(sub, movie_data):
    url= "http://napiprojekt.pl/unit_napisy/dl.php"

    data = {
        "f" : sub.sub_hash, "t" : napi_f(sub.sub_hash),
        "l" : "PL",
        "v" : "other",
        "kolejka" : "false",
        "nick" : "", "pass" : "",
        "napios" : os.name
    }

    sub_out_path = None
    with tempfile.NamedTemporaryFile() as f:
        resp = requests.get(url, data)
        f.write(resp.content)
        sub_out_path = "%s.txt" % os.path.splitext(movie_data.path)[0]
        cmd = ["7z", "x", "-y", "-so", "-piBlm8NTigvru0Jr0", f.name]

        decompressed = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)

        with open(sub_out_path, 'wb') as out_file:
            out_file.write(decompressed)

    return sub_out_path

def get_soup(url, post_data = None):
    if post_data is not None:
        resp = requests.post(url, post_data)
    else:
        resp = requests.get(url)
    return bs4.BeautifulSoup(resp.text, "html.parser")

def main():
    if not sys.stdout.isatty():
        log.critical("NapiMan is interactive program. Don't use it in scripts, pipes etc.")
        return ErrorCode.BAD_INPUT

    opt_parser = prepare_parser()
    args = opt_parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

    use_colors(args.no_color)

    selected_movies = {}

    for filename in args.files:
        if not os.path.exists(filename):
            log.error("%s doesn't exist. Skipping." % red(filename))
            continue

        print("  * Processing '%s'" % filename)

        try:
            name, season, episode = parse_input(filename, args)
            movie_data = get_movie_data(filename)

            queries_key = "%s-%s" % (name, season)

            movie_url = selected_movies.get(name)

            if (movie_url is None):
                movie_search_post = {
                    "queryString" : name,
                    "queryKind" : "0",
                    "queryYear" : "",
                    "associate" : ""
                }

                print("  * Search query: %s, season: %s, episode: %s"  %
                    (bold(name), season, episode))

                catalog_url = "http://www.napiprojekt.pl/ajax/search_catalog.php"
                soup = get_soup(catalog_url, movie_search_post)
                links = get_movie_pages(soup)
                movie_url = get_movie_page_url(links, name, args)
                selected_movies[name] = movie_url

            print("  * Video: %s" % movie_data)

            url = add_season(movie_url, season, episode)
            soup = get_soup(url)
            subs = get_subtitles(soup)

            if (len(subs) == 0):
                print("  * %s" % bold(red("No subtitles found!")))
                continue
            else:
                subs.sort(key=lambda k, md=movie_data: abs_diff(k.time_info, md.time_info))

                if args.manual_sub:
                    sub = choose(subs, "Many subtitles found, please choose one")
                else:
                    sub = subs[0]
                    print("  * Best subtitle: %s" % sub)

                downloaded_path = download(sub, movie_data)
                print("  * Downloaded subtitles: %s" % downloaded_path)
            print("")

        except ExceptionWithCode as e:
            if e.description() is not None:
                log.critical(str(e))
            return e.error_code()
        except Exception as e:
            log.error("Exception occured during processing of file %s. Skipping." % filename)
            log.debug(e)

    return ErrorCode.NO_ERROR
