import os
from os.path import join
import shutil
import numpy as np
import xml.etree.ElementTree as ET

rate = 0.8
root_path       = '/opt/projects/keras-frcnn/'
xml_path        = '/opt/projects/keras-frcnn/plasticVNOI/annotations'
images_path     = '/opt/projects/keras-frcnn/plasticVNOI/images/'
annotation_path = '/opt/projects/keras-frcnn/annotate.txt'

def init_folder():
    try:
        if not os.path.exists(root_path + 'train_images'):
            os.makedirs(root_path + 'train_images')
        if not os.path.exists(root_path + 'test_images'):
            os.makedirs(root_path + 'test_images')
    except Exception as e:
        print(e)


def get_train_test_name():
    """
    Chia thư mục dữ liệu thành 2 phần train, test. Mỗi phần có chứa tên của ảnh đuôi .jpg
    :return:
    """
    files = os.listdir(images_path)
    num_train = int(len(files) * 0.8)
    return files[:num_train], files[num_train:]


def move_to_folder(folder_name, img_names):
    """
    Chuyển tập ảnh có tên trong img_names vào thư mục folder_name
    :param folder_name:
    :param img_names:
    :return:
    """
    for name in img_names:
        dir_from = images_path + name
        dir_to = join(root_path, join(folder_name, name))
        shutil.copyfile(dir_from, dir_to)


def create_annotation(img_names):
    """
    Tạo file annotate.txt chứa nhãn của từng ảnh trong thư mục train_images

    :param img_names:
    :return:
    """
    img_names = [x[:-4] for x in img_names]

    with open(annotation_path, 'w') as f:
        for name in img_names:
            parsed_xml = ET.parse(join(xml_path, name + '.xml'))
            for node in parsed_xml.getroot().iter('object'):
                line = ''
                line += 'train_images/' + name + '.jpg,'
                line += node.find('bndbox/xmin').text.split('.')[0] + ','
                line += node.find('bndbox/xmax').text.split('.')[0] + ','
                line += node.find('bndbox/ymin').text.split('.')[0] + ','
                line += node.find('bndbox/ymax').text.split('.')[0] + ','
                line += node.find('name').text + '\n'
                f.write(line)



if __name__ == '__main__':
    init_folder()
    train_names, test_names = get_train_test_name()
    move_to_folder('train_images', train_names)
    move_to_folder('test_images', test_names)
    create_annotation(train_names)

