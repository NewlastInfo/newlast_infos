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

accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7
cache-control: max-age=0
cookie: oequaa9VXOEvO=5mk9FoXYKr9JrCk7Gzhi6KatPcDlyF6pmk1ara2Y_1h_wkUQLWQMcGOs17as8O1WXlXDqV9nycCGJca9iCOvLMG; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1678357977; _ga=GA1.2.1659515998.1678357977; _gid=GA1.2.1484209277.1678357977; juzi_user=1144224; juzi_token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvMTI3LjAuMC4xOjEwMTEzXC9hcGlcL3VzZXJzXC91c2VyX2hlYWRlcl9pbmZvIiwiaWF0IjoxNjc4MzU4MTM4LCJleHAiOjE2Nzg0MjA3OTQsIm5iZiI6MTY3ODQxMzU5NCwianRpIjoiNFY5aEtaeml2NFlVOFg2WiIsInN1YiI6MTE0NDIyNCwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyIsInV1aWQiOiJweW0ySGcifQ.PmS3A0XVaYVGT3-XlXkFYFcR5ODlQMGuzrW5Gjc1yaE; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1678414771; oequaa9VXOEvP=DjD3Pm3zk0ANe7.tjKYN.mtGJI2YGGng.DuZZiMirHSEcmKZF5o80aU8t0SpcY1pS1AF4Bi7Wf_swKE2s_F2IXFgelFnjzOyQF6yWdUjXp2SZTU6oVVPlAG_9eUuzc__QnFs_njfnhwmh_Luf_aTnOAru.laqMmQxWEwXVJ8YQum7iQAX0y.uApL7Cxa0h5LCytttzHN71vNHyUZqTL2ayDUztttXcsNKhclKqEnmhhb6Ozdw1EpAwEH7cub2zn7dEaxfZUVbCPUKn2jeB7ZiZag3DMyrRT2VwaZbP39aLjRcgsWJ.BSMpMGX.W0HGzf717nb0rDdlJ_7fNJrbCNIRkCNoGuWcDPSEILZoTbnnACgoQsqhAV3GGMf.klb7H99x7_VoTZIcnq42eL8Uzcvq
sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36


'''
    header_dict(header_request)
