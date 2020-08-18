from aip import AipFace
import os
import pymongo

# """ 你的 APPID AK SK """
APP_ID = '10322297'
API_KEY = 'RIrmS6cUDfSUjtsvhCN195yt'
SECRET_KEY = 'DKMiu1p9ozCo0MOGB4ju4GBqdBjNMx8y '

aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
def get_file_content(filePath):
    print(filePath)
    with open(filePath, 'rb') as fp:
        return fp.read()


# 定义参数变量
options = {
    'max_face_num': 1,
    'face_fields': "age,beauty,expression,faceshape",
}

# 调用人脸属性识别接口

def picture_score():
    pic_list = os.listdir("./pic")
    # ["result"][0]["age"] ["result"][0]["beauty"]
    # result = aipFace.detect(get_file_content('pic/0c24c1133_1_avatar_p.jpg'), options)
    # print(result)
    # print(result["result"][0]["age"])
    # print(result["result"][0]["beauty"])
    client = pymongo.MongoClient(host="10.36.132.181", port=27017)
    jiayuan = client.jiayuan
    pic_score = jiayuan.pic_score
    num = 0
    for pic in pic_list:
        if num > 800:
            print("fuck")
            break
        pic_dic = {}
        pic_path = "pic/" + pic
        result = aipFace.detect(get_file_content(pic_path), options)
        print(result)
        age = result["result"][0]["age"]
        beauty = result["result"][0]["beauty"]
        pic_dic["name"] = pic
        pic_dic["age"] = age
        pic_dic["beauty"] = beauty
        pic_score.insert(pic_dic)
        print(pic_dic)


def pic_similarity():
    client = pymongo.MongoClient(host="10.36.132.181", port=27017)
    jiayuan = client.jiayuan
    pic_similar_dili = jiayuan.pic_similar_dili

    pic_list = os.listdir("./pic")
    dili_path = "dilireba.jpg"

    compare_list = [dili_path]

    for i in pic_list:
        compare_list.append(i)

    result = aipFace.match([get_file_content("./pic/" + compare_list[i]) for i in range(len(compare_list)) if i < 100])
    print(result)
    similar = []

    for item in result["result"]:
        if item["index_i"] == '0':
            print(item["score"]) # 遍历与其余照片的相似度得分
            similar.append(item["score"])

    for i in range(len(similar)):
        sim_dict = {}
        sim_dict["name"] = pic_list[i]
        sim_dict["similarity"] = similar[i]
        print(sim_dict)
        pic_similar_dili.insert(sim_dict)


if __name__ == '__main__':
    pass
    pic_similarity()


    # result = aipFace.match([
    #     get_file_content('pic/dilireba.jpg'),
    #     get_file_content('pic/0c24c1133_1_avatar_p.jpg'),
    #     get_file_content('pic/0c24c1133_1_avatar_p.jpg'),
    #     get_file_content('pic/0d42e2cf0_3_avatar_p.jpg'),
    # ])
    #
    #
    # # result["result"]
    # for item in result["result"]:
    #     if item["index_i"] == '0':
    #         print(item["score"]) # 遍历与其余照片的相似度得分
    #
    # # picture_score()
    # # result = aipFace.detect(get_file_content('pic/dilireba.jpg'), options)
    # print(result)