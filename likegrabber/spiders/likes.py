# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import urllib.parse as urlparse
from urllib.parse import parse_qs

class LikesSpider(scrapy.Spider):
    name = 'likes'


    def start_requests(self):
        return [FormRequest(
            'https://%s/index.php?form=UserLogin' % self.url,
            formdata={'loginUsername': self.user, 'loginPassword': self.password, 'useCookies': '1'}
        )]

    def parse(self, response):
        #self.logger.info(response.text)
        if authentication_failed(response):
            self.logger.error("login failed")
        else:
            self.logger.info('login successful')
            for i in range(64):
                yield response.follow('https://%s/index.php?page=MembersList&sortField=posts&sortOrder=DESC&pageNo=%d' % (self.url, i), self.parse_users)


    def parse_user(self, response):
        user_id = ''
        try:
            user_id = parse_qs(urlparse.urlparse(response.request.url).query)['userID'][0]
        except:
            pass
        if(not user_id ==''):    
            return {
                'id': user_id,
                'name': response.css('.userName > span::text').get(),
                'likes': response.xpath("//h4/text()[. = 'Danksagungen']/../../p/text()").get() 
            }

    def parse_users(self, response):
        for href in response.css('.columnUsername a::attr(href)'):
            yield response.follow(href, self.parse_user)


