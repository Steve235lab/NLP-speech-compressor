# process_result_dict.py


import json


def process_result_dict(result_dict: dict) -> str:
    """对API返回的结果数据解包

    :param result_dict: json data
    :return: raw text content
    """
    content_str = ''
    for meta_dict in result_dict["cn"]["st"]["rt"][0]["ws"]:
        content_str += meta_dict["cw"][0]["w"]

    return content_str


if __name__ == '__main__':
    result = '{"seg_id":8,"cn":{"st":{"rt":[{"ws":[{"cw":[{"sc":0.00,"w":"床","wp":"n","rl":"0","wb":1,"wc":0.00,"we":20}],"wb":1,"we":20},{"cw":[{"sc":0.00,"w":"前","wp":"n","rl":"0","wb":21,"wc":0.00,"we":40}],"wb":21,"we":40},{"cw":[{"sc":0.00,"w":"明","wp":"n","rl":"0","wb":41,"wc":0.00,"we":64}],"wb":41,"we":64},{"cw":[{"sc":0.00,"w":"月光","wp":"n","rl":"0","wb":65,"wc":0.00,"we":116}],"wb":65,"we":116},{"cw":[{"sc":0.00,"w":"，","wp":"p","rl":"0","wb":121,"wc":0.00,"we":121}],"wb":121,"we":121},{"cw":[{"sc":0.00,"w":"疑","wp":"n","rl":"0","wb":121,"wc":0.00,"we":148}],"wb":121,"we":148},{"cw":[{"sc":0.00,"w":"是","wp":"n","rl":"0","wb":149,"wc":0.00,"we":164}],"wb":149,"we":164},{"cw":[{"sc":0.00,"w":"地上","wp":"n","rl":"0","wb":165,"wc":0.00,"we":208}],"wb":165,"we":208},{"cw":[{"sc":0.00,"w":"霜","wp":"n","rl":"0","wb":209,"wc":0.00,"we":244}],"wb":209,"we":244},{"cw":[{"sc":0.00,"w":"，","wp":"p","rl":"0","wb":249,"wc":0.00,"we":249}],"wb":249,"we":249},{"cw":[{"sc":0.00,"w":"举","wp":"n","rl":"0","wb":249,"wc":0.00,"we":276}],"wb":249,"we":276},{"cw":[{"sc":0.00,"w":"头","wp":"n","rl":"0","wb":277,"wc":0.00,"we":292}],"wb":277,"we":292},{"cw":[{"sc":0.00,"w":"望","wp":"n","rl":"0","wb":293,"wc":0.00,"we":308}],"wb":293,"we":308},{"cw":[{"sc":0.00,"w":"明月","wp":"n","rl":"0","wb":309,"wc":0.00,"we":360}],"wb":309,"we":360},{"cw":[{"sc":0.00,"w":"，","wp":"p","rl":"0","wb":365,"wc":0.00,"we":365}],"wb":365,"we":365},{"cw":[{"sc":0.00,"w":"低头","wp":"n","rl":"0","wb":365,"wc":0.00,"we":416}],"wb":365,"we":416},{"cw":[{"sc":0.00,"w":"思","wp":"n","rl":"0","wb":417,"wc":0.00,"we":432}],"wb":417,"we":432},{"cw":[{"sc":0.00,"w":"故乡","wp":"n","rl":"0","wb":433,"wc":0.00,"we":468}],"wb":433,"we":468},{"cw":[{"sc":0.00,"w":"。","wp":"p","rl":"0","wb":468,"wc":0.00,"we":468}],"wb":468,"we":468}]}],"bg":"0","type":"0","ed":"4770"}},"ls":true}'
    result_dict = json.loads(result)
    content_str = process_result_dict(result_dict)
    print(content_str)
