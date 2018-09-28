# coding = 'utf-8'
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import collections
import dicttoxml
from xml.dom.minidom import parseString

def parse_xml():
    tree = ET.parse('./outline.xml')
    root = tree.getroot()
    titles = []
    Title = collections.namedtuple('Title', ['title', 'page', 'level'])
    for part in root.find('catalogs'):        
        titles += Title(part.attrib['title'].strip(), int(part.attrib['page']), 'part'),
        for chapter in part:
            titles += Title(chapter.attrib['title'].strip(), int(chapter.attrib['page']), 'chapter'),
            for section in chapter:
                titles += Title(section.attrib['title'].strip(), int(section.attrib['page']), 'section'),
    # print (titles)
    return titles

def parse_txt():
    content = collections.defaultdict(list)
    with open('./content.txt') as f:
        for line in f.readlines():
            lindex = line.find('<')
            rindex = line.find('>')
            if lindex == -1 or rindex == -1:
                continue
            page = line[lindex+1:rindex]
            para = line[rindex+1:].rstrip()
            if page != 'img' and page != 'pic':
                content[int(page[1:])].append(para)
    # print (content)
    return content

def process(content, titles):
    obj = {'parts': []}
    for i in range(1, len(titles)):
        cur_title = titles[i]
        last_title = titles[i-1]
        if last_title.title == '第五章 基于全生命周期评价原理的污水处理技术评价' and cur_title.title == '5.1 生命周期评价的概念与发展':
            # return because of a p number error
            return
        
        potential_paras = content[last_title.page]+content[cur_title.page] if cur_title.page != last_title.page else content[last_title.page]
        actual_paras = []
        for para in potential_paras:
            if similar(para, cur_title.title):
                break
            if len(actual_paras)>0 or similar(para, last_title.title):
                actual_paras += para,
        actual_paras = actual_paras[1:]
        print (last_title, actual_paras)


        if last_title.level == 'part':
            part = collections.OrderedDict({'title':last_title.title, 'paras':actual_paras, 'chapters':[]})
        elif last_title.level == 'chapter':
            chapter = collections.OrderedDict({'title':last_title.title, 'paras':actual_paras, 'sections':[]})
        elif last_title.level == 'section':
            section = collections.OrderedDict({'title':last_title.title, 'paras':actual_paras})
            sections

    xml = dicttoxml.dicttoxml(obj, root=False, item_func=lambda x:'para', cdata=True)
    dom = parseString(xml)
    print(dom.toprettyxml())
        

def similar(s1, s2):
    combine = set(s1 + s2)
    return abs(len(combine) - len(set(s1))) < 3 and abs(len(combine) - len(set(s2))) < 3



def main():
    process(parse_txt(), parse_xml())

if __name__ == '__main__':
    main()