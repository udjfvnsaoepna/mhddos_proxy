FROM python:3.10-alpine as builder
RUN apk update && apk add --update git gcc libc-dev libffi-dev
RUN git clone https://github.com/porthole-ascend-cinnamon/mhddos_proxy.git
WORKDIR mhddos_proxy
RUN git clone https://github.com/MHProDev/MHDDoS.git
RUN pip3 install --target=/mhddos_proxy/dependencies -r MHDDoS/requirements.txt

FROM python:3.10-alpine
WORKDIR mhddos_proxy
COPY --from=builder	/mhddos_proxy .
ENV PYTHONPATH="${PYTHONPATH}:/mhddos_proxy/dependencies"

ENTRYPOINT ["python3", "./runner.py"]
