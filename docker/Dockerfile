FROM ubuntu:latest
RUN echo "We are runing Docker !!"
RUN apt-get -qq update
RUN apt-get install -y tar
RUN apt-get install -y make
RUN apt-get install -y gcc
RUN  apt-get install -y wget

RUN wget --no-parent --reject "index.html*" --reject "*.tar" --reject ".rpm" --reject "*.pdf" --reject "*.exe"  -r\
 http://www.iozone.org/src/stable/

WORKDIR  /www.iozone.org/src/stable/
RUN echo "Hello printing cir diur"
RUN make linux-AMD64
RUN ./iozone -s24m -r64 -i 0 -i 1 -t 1 -b iozone_report.xls






