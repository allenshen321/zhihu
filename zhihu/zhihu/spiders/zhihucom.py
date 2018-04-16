# -*- coding: utf-8 -*-


import scrapy
import json
import jsonpath

from ..items import ZhihuItem
from requests import Request


class ZhihucomSpider(scrapy.Spider):
    name = 'zhihucom'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    def start_requests(self):
        user_url_token = 'excited-vczh'
        offset = 0
        url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
        yield scrapy.Request(url,
                             meta={'cookiejar': 1,
                                   'user_url_token': user_url_token,
                                   'offset': offset},
                             callback=self.start_parse
                             )

    def start_parse(self, response):
        user_url_token = response.meta['user_url_token']
        # 解析用户关注信息，提取所有关注用户的url_token
        followees_user_json = json.loads(response.text)
        followees_user_num = jsonpath.jsonpath(followees_user_json, '$..totals')  # 关注总数
        # 循环取遍所有的关注者的url_token
        offset = -20
        while offset < (int(followees_user_num[0]) - 20):
            offset += 20
            # 用户的关注者信息链接
            followees_user_url = 'https://www.zhihu.com/api/v4/members/' + user_url_token + '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(
                offset) + '&limit=20'
            yield scrapy.Request(followees_user_url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.get_user_url_token)

    # 获得用户关注人的url_token
    def get_user_url_token(self, response):
        # 获取关注用户url_token 列表
        followees_user_json = json.loads(response.text)
        user_url_tokens = list(set(jsonpath.jsonpath(followees_user_json, '$..url_token')))
        # 将用户关注的人的在进行提取关注人的url_token,从首页提取关注总人数
        for user_url_token in user_url_tokens:
            offset = 0
            followees_user_url = 'https://www.zhihu.com/api/v4/members/' + user_url_token + '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(
                offset) + '&limit=20'
            yield scrapy.Request(followees_user_url,
                                 meta={'cookiejar': response.meta['cookiejar'],
                                       'user_url_token': user_url_token},
                                 callback=self.start_parse
                                 )

            # 构造用户详细信息url
            user_info_url = "https://www.zhihu.com/api/v4/members/" + user_url_token + '?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cincluded_answers_count%2Cincluded_articles_count%2Cincluded_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cis_org_createpin_white_user%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
            # 调用 user_info_parse函数进行提取用户详细信息
            yield scrapy.Request(user_info_url,
                                 callback=self.user_info_parse,
                                 meta={'cookiejar': response.meta['cookiejar']}
                                 )

    def get_user_info_url(self, response):
        url_token = ''
        # 轮子哥详细资料链接
        user_info_url = "https://www.zhihu.com/api/v4/members/" + url_token + '?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cincluded_answers_count%2Cincluded_articles_count%2Cincluded_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cis_org_createpin_white_user%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

        yield scrapy.Request(user_info_url,
                             meta={'cookiejar': response.meta['cookiejar']},
                             callback=self.user_info_parse,
                             )

    def user_info_parse(self, response):
        user_info_json = json.loads(response.text)
        if 'business' not in user_info_json.keys():
            business = None
        else:
            business = user_info_json.get('business').get('name')
        # 判断educations是否为空，如果空则返回空
        educations_major = ''
        educations_school = ''
        try:
            for educations in user_info_json['educations']:
                if educations.get('major') != None:
                    educations_major += (educations['major']['name'] + ',')
                if educations.get('school') != None:
                    educations_school += (educations['school']['name'] + ',')
        except Exception as e:
            print(e)
        # employments 判断
        employments_job = ''
        employments_company = ''
        for employments in user_info_json['employments']:
            if employments != None:
                if employments.get('job') != None:
                    employments_job = employments.get('job').get('name')
                if employments.get('company') != None:
                    employments_company = employments.get('company').get('name')
        # 对地点进行判断，防止有空的情况
        locations = ''
        for location in user_info_json['locations']:
            if location != None:
                locations += location.get('name') + ','

        user_info_item = ZhihuItem(
            name=user_info_json['name'],
            educations_major=educations_major,
            educations_school=educations_school,
            following_count=user_info_json['following_count'],
            headline=user_info_json['headline'],
            url_token=user_info_json['url_token'],
            favorited_count=user_info_json['favorited_count'],
            follower_count=user_info_json['follower_count'],
            employments_job=employments_job,
            employments_company=employments_company,
            following_topic_count=user_info_json['following_topic_count'],
            description=user_info_json['description'],
            business=business,
            answer_count=user_info_json['answer_count'],
            articles_count=user_info_json['articles_count'],
            question_count=user_info_json['question_count'],
            locations=locations,
            included_answers_count=user_info_json['included_answers_count'],
            logs_count=user_info_json['logs_count'],
            thanked_count=user_info_json['thanked_count'],
            gender=user_info_json['gender']
        )
        yield user_info_item
