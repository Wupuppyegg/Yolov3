import os
import shutil
from xml.dom.minidom import parse

def mod(a, b):    
    c = a // b
    r = a - c * b
    return r

if __name__ == "__main__":
    print('begin process...')

    #用户参数
    the_num_of_Missile_vehicle_1 = 0
    the_num_of_w = 0
    the_path_of_Missile_vehicle_1 = ''
    the_path_of_w = ''

    #输入输出目录设置
    xml_input_path = '/home/ganyd/Projects/yolov3_label_xml_to_txt/laoge1/标记图片'
    txt_output_path = '/home/ganyd/Projects/yolov3_label_xml_to_txt/laoge1/标记图片txt'
    files = os.listdir(xml_input_path)
    file_total_nums = len(files)

    #读取names文件,记录成字典变量
    namesDict = {}
    namesId = 1
    namesFile = open("/home/ganyd/Projects/yolov3_label_xml_to_txt/classType.names")
    for line in namesFile.readlines():
        namesDict[line.strip()] = namesId
        namesId = namesId + 1
    print(namesDict)

    #遍历当前目录下所有xml文件
    for index1,file in enumerate(files):
        xml_path = xml_input_path + '/' + file
        txt_path = txt_output_path + '/' + file.replace('.xml','.txt')
        xml_out_path_err = xml_input_path.replace('laoge1','laoge2') + '/' + file
        dom = parse(xml_path) #解析xml文件
        root = dom.documentElement
        txt_f = open(txt_path,'a')

        #获取当前xml中图像的宽高size
        size_wh = root.getElementsByTagName('size')[0]
        size_w = size_wh.getElementsByTagName('width')
        size_h = size_wh.getElementsByTagName('height')
        size_w = size_wh.getElementsByTagName("width")[0]
        size_h = size_wh.getElementsByTagName("height")[0]
        imgWidth = int(size_w.childNodes[0].data)
        imgHeight = int(size_h.childNodes[0].data)

        #获取当前xml中所有object
        objects = root.getElementsByTagName('object')
        #遍历所有object
        for index2,object in enumerate(objects):
            #class name
            names = object.getElementsByTagName("name")[0]
            name = names.childNodes[0].data
            if name == 'Missile vehicle 1':
                the_num_of_Missile_vehicle_1 = the_num_of_Missile_vehicle_1 + 1
                the_path_of_Missile_vehicle_1 = the_path_of_Missile_vehicle_1 + ' ' + file
                shutil.copyfile(xml_path, xml_out_path_err)
                continue
            if name == 'w':
                the_num_of_w = the_num_of_w + 1
                the_path_of_w = the_path_of_w + ' ' + file
                continue
            #转换成类别id
            objectId = namesDict[name]

            # bndbox
            xmins = object.getElementsByTagName("xmin")[0]
            xmin = int(xmins.childNodes[0].data)
            xmaxs = object.getElementsByTagName("xmax")[0]
            xmax = int(xmaxs.childNodes[0].data)
            ymins = object.getElementsByTagName("ymin")[0]
            ymin = int(ymins.childNodes[0].data)
            ymaxs = object.getElementsByTagName("ymax")[0]
            ymax = int(ymaxs.childNodes[0].data)

            #转成中心坐标和宽高的归一化值，保存成txt
            cen_x_normalize = (xmin + xmax)/2.0/imgWidth
            cen_y_normalize = (ymin + ymax)/2.0/imgHeight
            objWidth_normalize = (xmax - xmin) / imgWidth
            objHeight_normalize = (ymax - ymin) / imgHeight
            strTmp = str(objectId) + ' ' + str(cen_x_normalize) + ' ' + str(cen_y_normalize) \
                + ' ' + str(objWidth_normalize) + ' ' + str(objHeight_normalize)
            txt_f.write(strTmp)
            if index2 != len(objects)-1:
                txt_f.write('\n')

        txt_f.close()
        if mod(index1,100) == 0:
            print(index1,'/',file_total_nums)

    print('the_num_of_Missile_vehicle_1: ',the_num_of_Missile_vehicle_1)
    print('the_num_of_w: ',the_num_of_w)
    print('the_path_of_Missile_vehicle_1:\n')
    print(the_path_of_Missile_vehicle_1)
    print('the_path_of_w:\n')
    print(the_path_of_w)

    