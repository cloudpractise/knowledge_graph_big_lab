# -*- coding: utf-8 -*-

"""
BRAT ANN TO TXT(BOS) @wangshi
"""
import codecs
import os

tag_dic = {
    "加快折旧": "Accelerated Depreciation",
    "意外与健康福利": "Accident and Health Benefits",
    "应收账款": "Accounts Receivable (AR)",
    "具增值作用的收购项目": "Accretive Acquisition"
    "活跃债券投资者": "Active Bond Crowd",
    "活动收入": "Active Income",
    "积极投资": "Active Investing",
    "积极管理": "Active Management"
    # for more details, please check the fin_dict
}

# 转换成可训练的格式，最后以"END O"结尾


def from_ann2dic(r_ann_path, r_txt_path, w_path):
    q_dic = {}
    print("开始读取文件:%s" % r_ann_path)
    with codecs.open(r_ann_path, "r", encoding="utf-8") as f:
        line = f.readline()
        line = line.strip("\n\r")
        while line != "":
            line_arr = line.split()
            print(line_arr)
            cls = tag_dic[line_arr[1]]
            start_index = int(line_arr[2])
            end_index = int(line_arr[3])
            length = end_index - start_index
            for r in range(length):
                if r == 0:
                    q_dic[start_index] = ("B-%s" % cls)
                else:
                    q_dic[start_index + r] = ("I-%s" % cls)
            line = f.readline()
            line = line.strip("\n\r")

    print("开始读取文件:%s" % r_txt_path)
    with codecs.open(r_txt_path, "r", encoding="utf-8") as f:
        content_str = f.read()
        # content_str = content_str.replace("\n", "").replace("\r", "").replace("//////", "\n")
    print("开始写入文本%s" % w_path)
    with codecs.open(w_path, "w", encoding="utf-8") as w:
        for i, str in enumerate(content_str):
            if str is " " or str == "" or str == "\n" or str == "\r":
                print("===============")
            elif str == "/":
                if i == len(content_str) - len("//////") + 1:  # 表示到达末尾
                    # w.write("\n")
                    break
                # 连续六个字符首尾都是/,则表示换一行
                elif content_str[i + len("//////") - 1] == "/" and content_str[i + len("//////") - 2] == "/" and \
                        content_str[i + len("//////") - 3] == "/" and content_str[i + len("//////") - 4] == "/" and \
                        content_str[i + len("//////") - 5] == "/":
                    w.write("\n")
                    i += len("//////")
            else:
                if i in q_dic:
                    tag = q_dic[i]
                else:
                    tag = "O"  # 大写字母O
                w.write('%s %s\n' % (str, tag))
        w.write('%s\n' % "END O")


# 去除空行
def drop_null_row(r_path, w_path):
    q_list = []
    with codecs.open(r_path, "r", encoding="utf-8") as f:
        line = f.readline()
        line = line.strip("\n\r")
        while line != "END O":
            if line != "":
                q_list.append(line)
            line = f.readline()
            line = line.strip("\n\r")
    with codecs.open(w_path, "w", encoding="utf-8") as w:
        for i, line in enumerate(q_list):
            w.write('%s\n' % line)


# 生成train.txt、dev.txt、test.txt
# 除8，9-new.txt分别用于dev和test外,剩下的合并成train.txt
def rw0(data_root_dir, w_path):
    if os.path.exists(w_path):
        os.remove(w_path)
    for file in os.listdir(data_root_dir):
        path = os.path.join(data_root_dir, file)
        if file.endswith("8-new.txt"):
            # 重命名为dev.txt
            os.rename(path, os.path.join(data_root_dir, "dev.txt"))
            continue
        if file.endswith("9-new.txt"):
            # 重命名为test.txt
            os.rename(path, os.path.join(data_root_dir, "test.txt"))
            continue
        q_list = []
        print("开始读取文件:%s" % file)
        with codecs.open(path, "r", encoding="utf-8") as f:
            line = f.readline()
            line = line.strip("\n\r")
            while line != "END O":
                q_list.append(line)
                line = f.readline()
                line = line.strip("\n\r")
        print("开始写入文本%s" % w_path)
        with codecs.open(w_path, "a", encoding="utf-8") as f:
            for item in q_list:
                if item.__contains__('\ufeff1'):
                    print("===============")
                f.write('%s\n' % item)


if __name__ == '__main__':
    # ann and txt folder before converting to BOS featured txt
    data_dir = '/Users/thyme/Documents/Development/kg/raw_data/pilot_data/'
    for file in os.listdir(data_dir):
        if file.find(".") == -1:
            continue
        file_name = file[0:file.find(".")]
        r_ann_path = os.path.join(data_dir, "%s.ann" % file_name)
        r_txt_path = os.path.join(data_dir, "%s.txt" % file_name)
        w_path = "%s/new/%s-new.txt" % (data_dir, file_name)
        from_ann2dic(r_ann_path, r_txt_path, w_path)
    # 生成train.txt、dev.txt、test.txt
    rw0("%s/new" % data_dir, "%s/new/train.txt" % data_dir)
