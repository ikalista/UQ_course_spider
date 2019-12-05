import requests
from lxml import etree
import re

# 获取网页内容
def get_url(url, headers):
    ss = requests.Session()
    resp = ss.get(url, headers=headers)
    html = resp.text

    return html

def parse_UQ_course_list(content):#分析所有课程的界面   https://my.uq.edu.au/programs-courses/program_list.html?acad_prog=5522&year=2020
    hrefs = []  # 存放抓取的链接
    course_list = {}
    html = etree.HTML(content)
    table_list = html.xpath("//table")  # 主界面的Part ABC课程的table
    for table in table_list:
        trs = table.xpath("./tbody/tr")  # 每个table的所有tr
        for tr in trs:
            href = tr.xpath("./td[1]/a/@href")  # 取出每个课程介绍的链接
            code = tr.xpath("./td[1]/a/text()")#取出课程代码
            title = tr.xpath("./td[3]/text()")#取出课程title
            # Adding a new key value pair
            try:
                course_list.update({code[0].strip(): title[0]})
            except Exception as e:
                pass
            hrefs.append(href)

    return hrefs, course_list


def parse_UQ_course_details(content):#获取每一个units的链接
    html = etree.HTML(content)
    href = html.xpath("//table[@id='course-archived-offerings']/tbody/tr[1]/td[4]/a/@href")
    return href


def get_course_profile_url_list(part_of_hrefs):#分析每一个unit的界面
    course_profile_urls = []
    for i in part_of_hrefs:
        for href in i:
            course_url = "https://my.uq.edu.au" + href
            each_course_details_html = get_url(course_url, headers)
            course_profile_url = parse_UQ_course_details(each_course_details_html)
            course_profile_urls.append(course_profile_url)
    return course_profile_urls


def get_pre_course_of_courses(content):
    html = etree.HTML(content)
    title_code = html.xpath("//h1[@class='page__title']/text()")
    code = html.xpath("//div[@class='columns large-12']/p[10]/text()")
    pre_course_code = code[0].strip()
    return title_code, pre_course_code


url = "https://my.uq.edu.au/programs-courses/program_list.html?acad_prog=5522&year=2020"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

#main_page = get_url(url,headers)
#part_of_hrefs, course_list= parse_UQ_course_list(main_page)
#print(course_list)
#course_profile_urls = get_course_profile_url_list(part_of_hrefs)
#print(course_profile_urls)


course_details_urls_list = [['https://course-profiles.uq.edu.au/student_section_loader/section_1/99776'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/92499'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/99708'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/93799'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/93222'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/95874'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/98668'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/97940'], [], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/93738'], [], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/92563'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/97136'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/93164'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/96521'], [], [], [], [], [], [], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/99756'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/91925'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/93773'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/93174'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/94951'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/99678'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/90731'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/96532'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/95888'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/96493'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/93703'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/96597'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/95686'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/97179'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/100337'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/94343'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/100292'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/99790'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/98534'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/100401'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/92498'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/100406'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/97240'], ['https://course-profiles.uq.edu.au/student_section_loader/section_1/90706']]
course_list = {'COMP7402': 'Compilers and Interpreters ', 
               'COMP7500': 'Advanced Algorithms & Data Structures ',
               'COMP7703': 'Machine Learning ',
               'COMS4105': 'Communication Systems ',
               'COMS7200': 'Computer Networks II ',
               'COMS7507': 'Advanced topics in Security ',
               'CSSE4004': 'Distributed Computing ', 'CSSE4011': 'Advanced Embedded Systems ', 'CSSE4630': 'Principles of Program Analysis ', 'CSSE7610': 'Concurrency: Theory and Practice ', 'DECO6500': 'Advanced Human-Computer Interaction ', 'INFS7203': 'Data Mining ', 'INFS7205': 'Advanced Techniques for High Dimensional Data ', 'INFS7410': 'Information Retrieval and Web Search ', 'INFS7450': 'Social Media Analytics ', 'COMP7000': 'Special Topics in Computer Science 7A ', 'COMP7001': 'Special Topics in Computer Science 7B ', 'CSSE7080': 'Advanced Topics in Computer Systems A ', 'CSSE7081': 'Advanced Topics in Computer Systems B ', 'CSSE7090': 'Advanced Topics in Software Engineering A ', 'CSSE7091': 'Advanced Topics in Software Engineering B ', 'BISM7255': 'Business Information Systems Analysis and Design ', 'COMP7308': 'Operating Systems Architecture ', 'COMP7505': 'Algorithms & Data Structures ', 'COMP7702': 'Artificial Intelligence ', 'COMS7003': 'Information Security ', 'COMS7201': 'Computer Networks I ', 'COSC7502': 'High-Performance Computing ', 'CSSE7001': 'The Software Process ', 'CSSE7100': 'Reasoning about Programs ', 'CSSE7301': 'Embedded Systems Design & Interfacing ', 'DECO7350': 'Social & Mobile Computing ', 'INFS7202': 'Web Information Systems ', 'INFS7208': 'Cloud Computing ', 'INFS7907': 'Advanced Database Systems ', 'COMP7801': 'Computer Science Research Project ', 'COMP7802': 'Computer Science Research Project ', 'ENGG7811': 'Research Methods ', 'COMP7840': 'Computer Science Research Project ', 'COMP7860': 'Computer Science Research Project ', 'COMP7861': 'Computer Science Research Project ', 'COMP7862': 'Computer Science Research Project ', 'COMP7880': 'Computer Science Research Project ', 'COMP7881': 'Computer Science Research Project ', 'COMP7882': 'Computer Science Research Project '}
course_code_list = list(course_list.keys())

for i in course_details_urls_list:
    if i != []:
        #print(i[0])
        course_details_page = get_url(i[0],headers)
        title, pre_course_code = get_pre_course_of_courses(course_details_page)
        pre_course_code_list = re.split(' and | or | (|) ', pre_course_code)
        print(title[0])
        retA = [i for i in pre_course_code_list if i in course_code_list]
        #print(retA)
        if len(retA) > 0:
            print("Pre courses:")
        for lol in pre_course_code_list:
            try:
                print(lol, course_list[lol], "\n")
            except Exception as e:
                pass