import redis


def conn_redis():

    return redis.Redis()


def push_url(r,pages,start_url,spider_key):
    '''push url to redis server'''

    r.lpush(spider_key,start_url)
    for i in range(2,pages):
        req_url = f'https://www.amazon.com/s?k=tesla+accessories&page={i} \
            &crid=90RZC7XATMXS&qid=1626309688&sprefix=\
            tesla+accessories%2Caps%2C438&ref=sr_pg_{i}'
        r.lpush(spider_key,req_url)

    print(f'{i} page is pushed inside')

if  __name__ == '__main__':
    start_url = 'https://www.amazon.com/s?k=tesla+accessories&crid=' \
                '90RZC7XATMXS&sprefix=tesla+accessories%2Caps%2C438&ref' \
                '=nb_sb_ss_ts-doa-p_1_17'
    spider_key = 'tesla:start_urls'
    pages = 7
    r = conn_redis()
    push_url(r,pages,start_url,spider_key)
