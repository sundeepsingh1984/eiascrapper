import scrapy
from scrapy.utils.response import open_in_browser
import re
import pandas as pd

class EiaSpider(scrapy.Spider):
    
    name = 'eia'
    allowed_domains = ['eia.gov']
    start_urls = ['http://www.eia.gov/naturalgas/weekly/includes/archive.php/']

    
    def parse(self, response):
        BASE_URL="http://www.eia.gov"
        follow_links=response.xpath("(//table)[position()=1]/tbody/tr/td/a/@href").getall()
        for link in follow_links:
            url=BASE_URL+link
            yield scrapy.Request(url,self.parse_inner)

        



    
    def parse_inner(self,response):
        tables=response.xpath("(//table[@class='simpletable ngwu_tables'])[position()<7 or position()=last()]")

      
        report_link=response.xpath("//div[@class='ngwu_itn_box']//p/strong/text()").get()

        if report_link == "null" or not report_link:
            report_link=response.xpath("//div[@class='ngwu_itn_box']//h4/text()").get()

       
        data_dict={

        "report_link":self.remove_sp_chr(report_link),
        "report_url":response.request.url


        }


        START_DATE=None


        for i,table in enumerate(tables):
           
            if i  == 0:
                
                
                
                idx=table.xpath("(.//tbody)[1]/tr/td/strong/text()").getall()
                clm1=table.xpath('(.//thead//th)[position() < last() and position() != 1]//strong//text()').getall()
                clm1=[self.remove_sp_chr(clm) for clm in clm1]





                print(clm1)
               

            



           




             

                

            
            if i == 1:

                stng=table.xpath(".//tr/th/strong/text()").get()
                stng=stng.split(":")
                data_dict[stng[0]]=stng[1]
                dates=stng[1].replace("(","").replace(")","")
                dates=dates.split("-")
                data_dict["start"]=dates[0]
                data_dict["end"]= dates[1]

            
            
            
            if i==1 or i==2:    

                indices=table.xpath("(.//tr)[position()<last()  and position()>3]//td[1]/text()").getall()
                values=table.xpath("(.//tr)[position()<last()  and position()>3]//td[2]/div/text()").getall()
                
                for index,val in enumerate(values):
                    data_dict[self.remove_sp_chr(indices[index])]=self.remove_sp_chr(val)


            rigs_dict={}

             
            if i == 3:
           
                
                indices=table.xpath("(.//tr)[position()>3]//td[1]/text()").getall()
                values=table.xpath("(.//tr)[position()>3]//td[2]/div/text()").getall()
                dt=table.xpath("(.//tr)[position()=3]//td[1]/div/text()").get()
              


 
                
                for index,val in enumerate(values):
                    rigs_dict["datetime"]=dt
                    rigs_dict[self.remove_sp_chr(indices[index])]=self.remove_sp_chr(val)




            
        return rigs_dict
    def process_dates(self):
        pass           

    def remove_sp_chr(self,string):
        st=re.sub(r'[^\x00-\x7F]+','',string).strip()
        st.replace('\r', '').replace('\n', '').replace("\br","")
        st=st.encode(encoding="UTF-8").decode(encoding='UTF-8',errors='strict')
        return st


        


      
        

        
