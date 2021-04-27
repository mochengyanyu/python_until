# -*- coding: utf-8 -*-
# @Time : 2021/4/27 0027 21:09
# @Author : zuozhu
# @File : pdf_to_all

# pdf格式文件的转换
import os;
import PySimpleGUI as sg;
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams,LTTextBoxHorizontal,LTImage,LTCurve,LTFigure
from pdfminer.pdfpage import PDFTextExtractionNotAllowed,PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# 保存的位置
save_dir='E:/my_doc/'
def get_parser(path):
    file = open(path,'rb');
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(file);
    # 创建一个PDF文档对象存储文档结构,提供密码初始化，没有就不用传该参数
    doc = PDFDocument(parser,password='');
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed;
    rsrcmgr = PDFResourceManager(caching=False)
    # 创建一个PDF设备对象
    laparams = LAParams()
    # 创建一个PDF页面聚合对象
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解析器对象
    interpreter = PDFPageInterpreter(rsrcmgr, device);
    # 获得文档的目录（纲要）,文档没有纲要会报错
    # PDF文档没有目录时会报：raise PDFNoOutlines  pdfminer.pdfdocument.PDFNoOutlines
    return doc,interpreter,device;

def pdf_to_word(path):
    save_file = str(path).split('/')[-1];
    save_file_name = save_file.split('.')[0];
    doc,interpreter,device = get_parser(path);
    # 判断保存的文件夹是否存在,不存在则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir);
    #检查文件是否允许文本提取
    for page in PDFPage.create_pages(doc):
        # 利用解释器的process_page()方法解析读取单独页数
        interpreter.process_page(page);
        # 获取每个页面的值(LAParams,LTTextBoxHorizontal,LTImage,LTCurve,LTFigure);
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
        layout = device.get_result();
        for item in layout:
            if isinstance(item,LTTextBoxHorizontal):
                with open(save_dir+save_file_name+'.docx','a+') as to_word_file:
                    results = item.get_text().replace(u'\xa0', u' ')
                    to_word_file.write(results);
    sg.popup('转换成功!文件保存地址:%s' % (save_dir+save_file_name+'.docx'));


def get_gui():
    radios = [sg.Radio(text='文本', group_id='RADIO1', default=True), sg.Radio(text='图片', group_id='RADIO1'),
              sg.Radio(text='表格', group_id='RADIO1')];
    file_inputs = [sg.Text('文件的路径'), sg.InputText(key='file_id',disabled=True), sg.FileBrowse('上传')];
    btns = [sg.Button('确定'), sg.Button('退出')];
    layouts = [radios, file_inputs,btns];
    my_widows = sg.Window('PFD转化', layout=layouts);
    event, value = my_widows.read();
    if event is None or event == '退出':
        exit();
    my_widows.close();
    return event,value;


if __name__ == '__main__':
    event,value = get_gui();
    file_path = value['file_id'];
    if file_path == '' or not os.path.exists(file_path):
        sg.popup('文件路径不能空或者文件名不存在');
        exit();
    if value[0]:
        pdf_to_word(file_path);
    if value[1]:
        print('转换图片');
        sg.popup("等待开发");
    if value[2]:
        print('表耳转化');
        sg.popup('等待开发')