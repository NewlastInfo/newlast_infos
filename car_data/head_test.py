#!/usr/bin/env python
# -*- coding: utf-8 -*-

def header_dict(header_str):
    import re
    parttern = '(.*?):.(.*)'
    for line in header_str.splitlines():
        line = line.replace('"', '').replace('"', '')
        print(re.sub(parttern, r'"\1":"\2",', line))


if __name__ == '__main__':
    header_request = '''

accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7
authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvMTI3LjAuMC4xOjEwMTEzXC9hcGlcL3VzZXJzXC91c2VyX2hlYWRlcl9pbmZvIiwiaWF0IjoxNjc4MzU4MTM4LCJleHAiOjE2Nzg0MjA3OTQsIm5iZiI6MTY3ODQxMzU5NCwianRpIjoiNFY5aEtaeml2NFlVOFg2WiIsInN1YiI6MTE0NDIyNCwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyIsInV1aWQiOiJweW0ySGcifQ.PmS3A0XVaYVGT3-XlXkFYFcR5ODlQMGuzrW5Gjc1yaE
content-length: 0
cookie: oequaa9VXOEvO=5mk9FoXYKr9JrCk7Gzhi6KatPcDlyF6pmk1ara2Y_1h_wkUQLWQMcGOs17as8O1WXlXDqV9nycCGJca9iCOvLMG; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1678357977; _ga=GA1.2.1659515998.1678357977; _gid=GA1.2.1484209277.1678357977; juzi_user=1144224; juzi_token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvMTI3LjAuMC4xOjEwMTEzXC9hcGlcL3VzZXJzXC91c2VyX2hlYWRlcl9pbmZvIiwiaWF0IjoxNjc4MzU4MTM4LCJleHAiOjE2Nzg0MjA3OTQsIm5iZiI6MTY3ODQxMzU5NCwianRpIjoiNFY5aEtaeml2NFlVOFg2WiIsInN1YiI6MTE0NDIyNCwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyIsInV1aWQiOiJweW0ySGcifQ.PmS3A0XVaYVGT3-XlXkFYFcR5ODlQMGuzrW5Gjc1yaE; _gat=1; enable_undefined=true; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1678413927; oequaa9VXOEvP=0KbK42CRW.LdgKe2P9Yuu49h49E5rLz2zhb0nUF8JUSHeyrX1edhDkhES14wAUI83VbuTwltIPn6EpQhdp8dtTYjONrz7FjoBXtL9msGo_RZT4zoGKwv2qvuNffhHrLVzZKJVW2rx_0GB.jUC3ZQVZibdCCvLqTWQTTlHxpFLJFmHVfzQ600dy9oje51ZsIjJHm6RN4j2fquxoo1eMoaJWYxde.aevQkcg5beHVeCITqP7gaGENXiCxWCDQZCqYkapaP0BaZ05cS0LmaJwHMyPH9lOIl20tZjccki26LZ48swWEVxlcJWDZjIsDyL612irFhQrkPRx9tMqIF2S1_IoY0fxzAE6Kfunuz2kdpQuQ
origin: https://www.itjuzi.com
referer: https://www.itjuzi.com/investevent
sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36

'''
    header_dict(header_request)

