# -*- coding: utf-8 -*-
import os
import shutil


class GetConf(object):
    def __init__(self):
        self.s_dir = os.getcwd()

    def list_files_to_txt(self, file, recursion):
        print("生成备份配置文件列表..")
        ext_s = ".txt"
        for root, sub_dirs, files in os.walk(self.s_dir):
            for name in files:
                for ext in ext_s:
                    if name.endswith(ext):
                        print("搜索到配置文件:" + name)
                        file.write(name + "\n")
                        break
            if not recursion:
                break

    def get_conf_dir(self):
        print("在当前文件夹下创建配置脚本存放目录....")
        try:
            os.mkdir(self.s_dir + "\\conf_dir\\")
            print("创建./conf_dir/成功！")
        except OSError:
            while True:
                print("目录已存在！是否删除目录下所有已存在文件（y/n）？")
                user_input = input("请输入：")
                if user_input == "y":
                    print("正在删除子目录及文件")
                    self.del_file(self.s_dir + "\\conf_dir\\")
                    break
                elif user_input == "n":
                    print("未删除目录，如果目录下存在与目标配置脚本相同的文件名，请识别后使用！")
                    break
                else:
                    print("输入选项有误，请重输入！")
        outfile = self.s_dir + "\\conf_dir\\file_list.txt"
        file = open(outfile, "w")
        if not file:
            print("cannot open the file %s for writing" % outfile)
        self.list_files_to_txt(file, 0)
        file.close()

    def mk_config(self):
        print("获取当前目录（请确保备份的配置文件在此根目录下且后缀名为”.txt“）")
        self.get_conf_dir()
        file_list = self.s_dir + "\\conf_dir\\file_list.txt"
        print("生成备份配置文件列表成功，文件为:" + file_list)
        with open(file_list, 'r') as f:
            lines = f.readlines()
            for line in lines:
                file_name = line.strip('\n')
                self.mk_config_file(file_name)
        f.close()
        os.system('pause')

    def mk_config_file(self, filename):
        with open(self.s_dir + "\\" + filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            with open(self.s_dir + "\\conf_dir\\" + "conf_" + filename, 'a', encoding='utf-8') as dfile:
                print("正在生成配置脚本文件：conf_" + filename + "...")
                for line in lines:
                    if line.startswith(('!', 'hostname', 'enable password', 'clock timezone', 'no ip domain-', 'vtp mode ', 'vlan ', 'interface', ' switchport', ' spanning-tree portfast', 'interface Vlan',' ip address', 'line vty 0', ' password ', 'ntp server ', 'end')):
                        dfile.write(line)
                dfile.write("write\n")
            dfile.close()
            print("完成！")

    def del_file(self, filepath):
        """
        删除某一目录下的所有文件或文件夹
        :param filepath: 路径
        :return:
        """
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


if __name__ == '__main__':
    get_conf = GetConf()
    get_conf.mk_config()

