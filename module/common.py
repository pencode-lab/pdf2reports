# -*- coding: utf-8 -*-
"""
Common functions used in all modules.

Created on 2021.08.04 

@author: stone 
"""


import xml.etree.ElementTree as ET
import json
import struct
import numpy as np


def read_xml(fname):
    """
    Read an XML file <fname> which can be later parsed with parse_pages. Uses Python's xml.etree.ElementTree.
    Return a tuple with (XML tree object, tree root element)
    """
    tree = ET.parse(fname)
    root = tree.getroot()

    return tree, root


def create_text_dict(t,value=None):
    """
    From an XML element <t>, create a text box dict structure and return it.
    <text top="69" left="684" width="26" height="12" font="1">2020</text>
    """
    t_top = int(float(t.attrib['top']))
    t_left = int(float(t.attrib['left']))
    t_width = int(float(t.attrib['width']))
    t_height = int(float(t.attrib['height']))
    t_value = value.strip() 

    text = {
        'top': t_top,
        'left':t_left,
        'width': t_width,
        'height':t_height,
        'value': t_value,
        'xmlnode': t
    }

    return text


def parse_text_box(root,start_word,stop_word=None, min_row_space=16):
    """
    Parses an XML structure in pdf2xml format to extract the text boxes.
    <root> is the XML tree root

    <text top="67" left="518" width="162" height="14" font="0">江苏洋河酒厂股份有限公司</text>
    <text top="69" left="684" width="26" height="12" font="1">2020</text>
    <text top="67" left="713" width="94" height="14" font="0">年年度报告全文</text>
    <text top="69" left="808" width="3" height="12" font="1"> </text>

    Return an text list.
    """
  
    
    start =False
    stop = False

    text_list=[]
    _last_row=[]

    for t in root.iter("text"):
        value = t.text
        text=None

        if not value:
            continue

        if value:
            if value.find(start_word)>= 0:
                start =True
            if start and value.find(stop_word) >= 0:
                stop =True

        if start:
            text = create_text_dict(t,value)
            text_list.append(text) 

        if stop :
            if( len(_last_row)>0):
                last_text = _last_row[-1]
                #Make sure  save  all text in the same row 
                if last_text.get('top')== text.get('top'):
                    row_space = 0
                elif last_text.get('top') <= text.get('top'):
                    row_space =text.get('top') - (last_text.get('top') + last_text.get('height'))
                else:
                    row_space =last_text.get('top') - (text.get('top') + text.get('height'))

                if abs(row_space) > min_row_space:#is't in same row
                        del text_list[-1]
                        break
            _last_row.append(text)
        

    return text_list,min_row_space





def compose_rows(text_list, min_row_space=16):

    '''
    from parse_text_box() get text list
    this function compose rows
    '''
    iter_texts=iter(text_list)

    _row=[]
    rows_list =[]

    while True :
        try:
            #same rows do in a while()
            prv_text=None
            while True:
                text=next(iter_texts)
                if prv_text:

                    #Make sure  save  all text in the same row
                    if prv_text.get('top')== text.get('top'):
                        row_space = 0
                    elif prv_text.get('top') <= text.get('top'):
                        row_space =text.get('top') - (prv_text.get('top') + prv_text.get('height'))
                    else:
                        row_space =prv_text.get('top') - (text.get('top') + text.get('height'))

                    if abs(row_space) > min_row_space:#is't in same row
                        #save row and start new row
                        rows_list.append(_row.copy())
                        prv_text=None
                        _row.clear()

                _row.append(text)
                prv_text = text
        except StopIteration:
            rows_list.append(_row.copy())
            break
        #end try
    #end while

    return rows_list
    #return np.array(rows_list)



def compose_col(rows_list, min_col_space=60):

    '''
    from compose_rows get rows list
    this function compose columns 
    '''
    return_lists =[]

    #row like : [text1,text2,tex3...]
    for row in rows_list: #get per row

        iter_texts = iter(row)
        prv_text = None
        value_list=[]
        _tmp_row=[]
        while True:#loop for col in a row 
            try:
                text = next(iter_texts)
                if prv_text:
                    #print("text.left:=",text.get('left'),'--------prv_text.left+width=',(prv_text.get('left')+prv_text.get('width')))
                    if (text.get('left') - (prv_text.get('left')+prv_text.get('width'))) > min_col_space:#is't in same col 
                        _tmp_row.append("".join(value_list))
                        value_list.clear()
                value_list.append(text.get('value'))
                prv_text = text
            except StopIteration:
                _tmp_row.append("".join(value_list))
                return_lists.append(_tmp_row.copy())
                break


    return return_lists




