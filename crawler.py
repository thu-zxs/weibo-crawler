#-*- coding:utf-8 -*-
import urllib2
import json
import time
#cookie_dict ={'_T_WM':'83ae70af166c701e5e05ea8538bceef4', 'gsid_CTandWM':'4u25CpOz5rGjCdIIGoV3nlUSq2R', 'H5_INDEX':'2', 'H5_INDEX_TITLE':'thu_Zengxs', 'SSOLoginState':'1464261968', 'SUB':'_2A256Qq0ADeRxGeNM6VEU8ijNzDuIHXVZzDNIrDV6PUJbrdBeLWLbkW1LHetrqciPXv8uSN5FGVARUDfGEK9KPg..', 'SUHB':'0N21z16Zx-NbhF'}
import re
# get user info by id through json analyst
def get_user_info_by_id(uid, retry=3):
    url = 'http://m.weibo.cn/u/%s' % uid
    success = False
    attempts = 0
    #print url
    while not success:
        try:
            req = urllib2.Request(url,
                                  headers={
                                     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 ' +
                                     '(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
                                )
            response = urllib2.urlopen(req)
            data = response.read()
            begin = data.find("""[{"mod_type":""")
            end = data.find("""},'common':""")
            body = data[begin:end]
            body = json.loads(body, encoding = "gb2312")
            #assert body[1]['mod_type'] != 'mod/empty'
            assert 'id' in body[1]
            success = True
        except Exception as e:
            if attempts < retry:
                attempts += 1
                time.sleep(2)
            else:
                #print e
                return 0

    #body = json.dumps(body[0], skipkeys = True, ensure_ascii = False, encoding = "gb2312", indent = 4)
    nums = int(body[1]['mblogNum']), int(body[1]['attNum']), int(body[1]['fansNum'])
    #print body
    print nums
    return body

# Another method that also works.
def get_user_info_by_id_v2(uid, cookie_dict, retry):
    url = 'http://m.weibo.cn/users/'+uid+'/?'
    success = False
    attempts = 0
    #print url
    while not success:
        try:
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookie_dict.items())))
            req = urllib2.Request(url,
                               headers={
                                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
                                    #'Connection':'keep-alive'
                                    #'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 ' +
                                                    #'(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
                                        }
                                )
            response = opener.open(req)
            data = response.read()
            assert '昵称' in data
            success = True
        except Exception as e:
            if attempts < retry:
                attempts += 1
                time.sleep(5)
            else:
                #print e
                return 0
    body = data

    return body

# get posts by keyword by accessing the Weibo in-built search engine.
def get_weibo_by_keyword(keyword, page):
    if page > 1:
        url = 'http://m.weibo.cn/main/pages/index?containerid=100103type%3D1%26q%3D'+keyword+'&type=all&queryVal='+keyword+'&luicode=20000174&title='+keyword+'&page='+str(page)
    else:
        url = 'http://m.weibo.cn/main/pages/index?containerid=100103type%3D1%26q%3D'+keyword+'&type=all&queryVal='+keyword+'&luicode=20000174&title='+keyword
    #print url
    req = urllib2.Request(url,
                          headers={
                              'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 ' +
                                            '(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
                          )
    response = urllib2.urlopen(req)
    data = response.read()
    try:
        body = json.loads(data)
        weibos = body[1]['card_group'][0]['card_group']
        weibolist = [w['mblog'] for w in weibos]
        return weibolist
    except Exception as e:
        pass

# Weibo Topics is a place held by a host for users to join in the discussion of some specific topics. Host is also a weibo users.
# We called users who post under this topic the followers.
# This implements a function for grabbing the posts from a specific theme and extracting their owners' info..
def get_weibo_by_theme(container_id1, uid, cookie_dict, page = 1, retry = 3, last_since_id = None, next_since_id = None):
    #url1 = 'http://m.weibo.cn/p/index?containerid='+container_id1+'&page='+str(page)
    if page == 1:
        url1 = 'http://m.weibo.cn/page/pageJson?containerid='+container_id1+'&containerid='+container_id1+'&uid='+uid+'&page=1'
    else:
        url1 = 'http://m.weibo.cn/page/pageJson?containerid=&containerid=' + container_id1 + '&uid=' + uid +'&from=feed&luicode=10000011&lfid=10730319c366f62380fecd399270159fcc2184_-_ext_intro&v_p=11&ext=&fid='+container_id1+'&uicode=10000011&next_cursor={%22last_since_id%22:'+last_since_id+',%22res_type%22:1,%22next_since_id%22:'+next_since_id+'}&page='+str(page)
    #print url1
   # /page/pageJson?containerid=&containerid=23053010080819c366f62380fecd399270159fcc2184__timeline__mobile_info_-_pageapp%3A23055763d3d983819d66869c27ae8da86cb176&uid=5223526177&from=feed&luicode=10000011&lfid=10730319c366f62380fecd399270159fcc2184_-_ext_intro&v_p=11&ext=&fid=23053010080819c366f62380fecd399270159fcc2184__timeline__mobile_info_-_pageapp%3A23055763d3d983819d66869c27ae8da86cb176&uicode=10000011&next_cursor={%22last_since_id%22:3981637848790627,%22res_type%22:1,%22next_since_id%22:3981630722841857}&page=2
    #print url1
    success = False
    attempts = 0
    body = 0
    #print url1
    while not success:

        try:
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookie_dict.items())))
            req = urllib2.Request(url1,
                              headers={
                                  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 ' +
                                                '(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
                                  #, 'Cache-Control': 'max-age=0'
                                  }
                              )
            response = opener.open(req)
            data = response.read()
            body = json.loads(data)
            assert len(body['cards']) > 0
            success = True
        except Exception as e:
            if attempts < retry:
                attempts += 1
                time.sleep(3)
            else:
                return 0;
    weibos = body['cards'][0]['card_group']
    cursor = json.loads(body['next_cursor'])
    Last = str(cursor['last_since_id'])
    Next = str(cursor['next_since_id'])
    users = [(k['mblog']['user']['screen_name'], str(k['mblog']['user']['id']), k['mblog']['user']['gender']) for k in weibos]
    #weibos = body[1]['card_group'][0]['card_group']
    #weibolist = [w['mblog'] for w in weibos]
    #return [theme, weibos, users]
    return [users, Last, Next]


# Each topic has its own fans. A user becomes fans by clicking the 'focus' button on the topic.
# This implementation can grab those fans's info.
def get_fans_by_theme(container_id, uid, cookie_dict, page = 2, retry = 3):
    url = 'http://m.weibo.cn/p/index?containerid='+container_id+'&containerid='+container_id+'&title=粉丝&uid='+uid+'&page='+str(page)
    success = False
    attempts = 0
    #print url
    while not success:
        try:
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookie_dict.items())))
            req = urllib2.Request(url,
                                headers={
                                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
                                    #'Connection':'keep-alive'
                                    #'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 ' +
                                                    #'(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
                                        }
                                )
            response = opener.open(req)
            data = response.read()
            body = json.loads(data)
            #assert body[1]['mod_type'] != 'mod/empty'
            assert 'card_group' in body[1].keys()
            success = True
        except Exception as e:
            if attempts < retry:
                attempts += 1
                time.sleep(2)
            else:
                #print e
                return 0
    users_list = body[1]['card_group'][0]['card_group']
    users = [(k['user']['screen_name'], str(k['user']['id']), k['user']['location'][0:2], k['user']['gender']) for k in users_list]
    return [users_list, users]


# Get user's fans and follows by sepecifying its uid.
def get_focus_or_fans_by_id(uid, cookie_dict, opt, page = 1, retry = 3):
    if opt == 'focus':
        url = 'http://m.weibo.cn/page/json?containerid=100505'+uid+'_-_FOLLOWERS&page='+str(page)
    elif opt == 'fans':
        url = 'http://m.weibo.cn/page/json?containerid=100505'+uid+'_-_FANS&page='+str(page)
    success = False
    attempts = 0
    #print url
    while not success:
        try:
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookie_dict.items())))
            req = urllib2.Request(url,
                                headers={
                                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
                                    #'Connection':'keep-alive'
                                    #'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 ' +
                                                    #'(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
                                        }
                                )
            response = opener.open(req)
            data = response.read()
            body = json.loads(data)
            #assert body[1]['mod_type'] != 'mod/empty'
            #assert body['count'] != None
            success = True
        except Exception as e:
            if attempts < retry:
                attempts += 1
                time.sleep(3)
            else:
                #print e
                return [None, None]
    num = body['count']
    if num == None:
        return [None, None]
    users_list = body['cards'][0]['card_group']
    users = [str(k['user']['id']) for k in users_list]
    return [num, users]

