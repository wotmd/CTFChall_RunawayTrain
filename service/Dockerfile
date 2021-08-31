from ubuntu:18.04

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y xinetd python3-minimal python3-pip

ENV PROB runtrain
RUN useradd -m $PROB
WORKDIR /home/$PROB


ADD ./runtrain.xinetd /etc/xinetd.d/runtrain
ADD ./server.sh /home/$PROB/
ADD ./src/* /home/$PROB/
RUN chmod +x /home/$PROB/runtrain
RUN chmod +x /home/$PROB/server.sh
RUN chmod +x /home/$PROB/server.sh
RUN echo "runtrain 31337/tcp" >> /etc/services

EXPOSE 31337
CMD ["xinetd","-dontfork"]
