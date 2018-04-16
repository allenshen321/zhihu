# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # user_name
    following_count = scrapy.Field() # 2418 关注的人数
    headline = scrapy.Field() # 一句话简介
    url_token = scrapy.Field() # 用户唯一ID
    favorited_count = scrapy.Field() # 收藏量
    follower_count = scrapy.Field()  # 被多少人关注
    employments_job = scrapy.Field()  # 职业
    employments_company = scrapy.Field()  # 所在公司
    following_topic_count = scrapy.Field()  # 关注的话题数
    description = scrapy.Field()  # 个人简介
    business = scrapy.Field()  # 所在行业
    answer_count = scrapy.Field()  # 回答数量
    articles_count = scrapy.Field()  # 文章数量
    question_count = scrapy.Field()  # 提问数量
    locations = scrapy.Field()  # 居住地
    included_answers_count = scrapy.Field()  # 知乎收录回答数量
    logs_count = scrapy.Field()  # 参与公共编辑数量
    thanked_count = scrapy.Field()  # 被感觉次数
    gender = scrapy.Field()  # 性别 1是男，0是女
    educations_major = scrapy.Field()  # 教育专业
    educations_school = scrapy.Field()  # 学校