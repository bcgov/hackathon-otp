FROM sqitch/sqitch

WORKDIR /schema
COPY . /schema

ENTRYPOINT [ "/bin/sqitch" ]
CMD ["deploy"]
