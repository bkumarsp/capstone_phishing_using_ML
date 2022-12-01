
from gophish import Gophish
from gophish.models import *
import urllib3



def launchGophish(emailTo='bhuvantejreddy45@gmail.com', firstname="bhuvan", lastname='tej', emailSubject="Automatic phishing attack", emailBody="An empty email"):
   
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print("Email: ",emailTo)

    api_key = '95291cb4f749651769852cc54590ee1385c535fb4f517354eac5cc61c4425eb1'
    api = Gophish(api_key, host='https://127.0.0.1:3333/', verify=False)
   
    # for campaign in api.campaigns.get():
    #     print(campaign.name)

    targets = [
        User(first_name=firstname, last_name=lastname, email=emailTo),
    ]

    group = Group(name='capstone_review_3', targets=targets)
    group1 = api.groups.post(group)


    # #to create the sending Profiles
    # # smtp = SMTP(name='demo1')
    # # smtp.host = "localhost:25"
    # # smtp.from_address = "Vyshak R <srvyshak@gmail.com>"
    # # smtp.interface_type = "SMTP"
    # # smtp.ignore_cert_errors = True
    # # smtp = api.smtp.post(smtp)
    # # print (smtp.id)

    Domains = {
        'hacker-rank': {'groups': [Group(name='capstone_review_3')], 'page': Page(name='Hackerrank'), 'template': Template(name='Hackerrank_invite'), 'smtp': SMTP(name='Facebook'), 'urls': 'http://127.0.0.1:8000/cloned/facebook'},
    }

    # groups = [Group(name='capstone_review_3')]
    # page = Page(name='Instagram')
    # template = Template(name='Facebook')
    # smtp = SMTP(name='Facebook')

    # urls = 'http://test123.iminyour.network'

    # campaign = Campaign(
    #     name='capstone_review_3 demo',
    #     groups=groups, 
    #     page=page,
    #     template=template, 
    #     smtp=smtp, 
    #     url=urls
    # )

    campaign = Campaign(
        name='capstone_review_3 phishing',
        groups=Domains['hacker-rank']['groups'], 
        page=Domains['hacker-rank']['page'],
        template=Domains['hacker-rank']['template'], 
        smtp=Domains['hacker-rank']['smtp'], 
        url=Domains['hacker-rank']['urls']
    )

    campaign = api.campaigns.post(campaign)
    # api.groups.delete(group)
    # x=campaign.id
    # print (x)

    # api.campaigns.complete(x)


    # summaries = api.campaigns.summary(8)
    # print(summaries.stats.as_dict())
