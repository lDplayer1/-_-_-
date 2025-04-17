from request import table_generator, get_official_languages
from classes.country import country, query_cities_of_country
import random
import requests

def method_1(classtype_1 = country(),reps = 5):
    global classtype
    classtype = classtype_1 ## 选择主题
    keys, opts = [],[]
    for i in range(reps):
        if not (keys or opts):
            quiz_table = table_generator(classtype)
            keys, opts = table_sort(quiz_table)
        keys,opts = generate_fill(keys,opts)

def method_2(classtype_2 = country(),reps = 5):
    global classtype
    classtype = classtype_2 ## 选择主题
    keys, opts = [],[]
    for i in range(reps):
        if len(keys)<4:
            quiz_table = table_generator(classtype)
            keys, opts = table_sort(quiz_table)
        keys,opts = generate_quiz(keys,opts)

def method_4(classtype_4 = country(),reps = 5):
    global classtype
    classtype = classtype_4 ## 选择主题
    keys, opts = [],[]
    for i in range(reps):
        if len(keys)<4:
            quiz_table = table_generator(classtype)
            keys, opts = table_sort(quiz_table)
        i_max = 5 if classtype.name == "Country" else 4
        index = random.randint(0,i_max)
        if index == 0: keys,opts = generate_quiz(keys,opts)
        elif index == 1: keys,opts = generate_fill(keys,opts)
        elif index == 2: keys,opts = generate_TrueOrFalse(keys,opts)
        elif index == 3: keys,opts = generate_question(keys,opts)
        elif index == 4: keys,opts = generate_match(keys,opts)
        else: keys,opts = generate_two_fill(keys,opts)

def table_sort(table_dict):
    results_list = [value.replace(' ','_') for value in table_dict.values()]
    keys_list = [key for key in table_dict.keys()]
    return keys_list, results_list

    
def generate_quiz(keys_list,results_list):
    keyword = random.choice(keys_list)
    rightOpt = results_list[keys_list.index(keyword)] ## 正确宾语
    results_list.remove(rightOpt)
    keys_list.remove(keyword)
    
    if classtype.name == "Country": w = "What"
    else: w = "Who"
    question = f"{w} is the {classtype.opt} of {keyword}? \n" 
    #question = f"{w} is the {classtype.opt} of 《{keyword}》? \n"

    options = [rightOpt]  # 用正确的答案初始化选项列表
    cities = []
    if classtype.name == "Country": cities = query_cities_of_country(keyword.replace(' ','_'))
    wrongResults = list(set(results_list + cities))
    wrongOpt = random.sample(wrongResults, 3)  #随机选择3个错误答案
    options.extend(wrongOpt)
    random.shuffle(options)  # 选项随机化
    
    # Transform options into A/B/C/D 
    choices = ["A", "B", "C", "D"]
    options = dict(zip(choices, options))
    options_str = "\n".join([f"{choice}. {option}" for choice, option in options.items()])
    
    print(question + options_str + "\n")
    return keys_list,results_list

def generate_fill(keys_list,results_list): ##填空题
    keyword = random.choice(keys_list)
    rightOpt = results_list[keys_list.index(keyword)] ## 正确宾语
    results_list.remove(rightOpt)
    keys_list.remove(keyword)

    question = f"The {classtype.opt} of {keyword} is {rightOpt}. \n" ##三元组
    index = random.randint(0,1) ##随机选择刨去主语or宾语
    if classtype.name == "Country" and index == 0: blank = keyword 
    else: blank = rightOpt
    print(question.replace(blank,'________'))
    return keys_list,results_list

def generate_TrueOrFalse(keys_list,results_list): ##判断题
    keyword = random.choice(keys_list)
    rightOpt = results_list[keys_list.index(keyword)] ## 正确宾语
    results_list.remove(rightOpt)
    keys_list.remove(keyword)
    cities = []
    if classtype.name == "Country": cities = query_cities_of_country(keyword.replace(' ','_'))
    wrongResults = list(set(results_list + cities))

    question = f"The {classtype.opt} of {keyword} is {rightOpt}.\t\u2610\n" ##生成真三元组
    if random.randint(0,1): ## 如果随机为1，替换为假三元组
        i = random.randint(0,1) ##随机选择替换主语or宾语
        if classtype.name == "Country" and i == 0: target, bullet = keyword, random.choice(keys_list)
        else: target, bullet = rightOpt, random.choice(wrongResults)
        question.replace(target,bullet)
    print(question)
    return keys_list,results_list

def generate_question(keys_list,results_list):
    keyword = random.choice(keys_list)
    rightOpt = results_list[keys_list.index(keyword)] ## 正确宾语
    results_list.remove(rightOpt)
    keys_list.remove(keyword)
    if classtype.name == "Country": w = "What"
    else: w = "Who"
    question = f"{w} is the {classtype.opt} of {keyword}? \n" 
    print(question)
    return keys_list,results_list

def generate_match(keys_list,results_list):
    keywords = random.sample(keys_list,4)
    rightOpts = [] 
    for keyword in keywords:
        rightOpt = results_list[keys_list.index(keyword)]
        rightOpts.append(rightOpt)
        results_list.remove(rightOpt)
        keys_list.remove(keyword)
    random.shuffle(rightOpts)
    options = dict(zip(keywords, rightOpts))
    options_str = "\n".join([f"{choice}\t{option}" for choice, option in options.items()])
    print("Match country and its Capital!\n"+options_str)
    return keys_list,results_list

def generate_two_fill(keys_list,results_list):
    keyword = random.choice(keys_list)
    rightOpt = results_list[keys_list.index(keyword)] ## 正确宾语
    results_list.remove(rightOpt)
    keys_list.remove(keyword)
    language = get_official_languages(keyword)
    question = f"________'s capital is {rightOpt} and officially speak in {language}. \n" ##三元组
    print(question)
    return keys_list,results_list

'''----------------------------------------------------------'''

API_URL = "http://localhost:11434/api/generate"

def table_sort4LLM(table_dict):
    if not table_dict:
        print("Error: table_dict is empty!")
        return None  # 避免返回错误值

    if classtype.name == "Country":
        keyword = random.choice(list(table_dict.keys()))
        wrongResults = query_cities_of_country(keyword)
        wrongKeys = list(table_dict.keys())
    else:
        wrongResults = list(table_dict.values())
        keyword = random.choice(list(table_dict.keys()))
        wrongKeys = list(table_dict.keys())

        try:
            wrongKeys.remove(keyword)
        except ValueError:
            pass

    rightOpt = table_dict.get(keyword, "Unknown")  # 确保获取到正确宾语
    if rightOpt is None:
        print(f"Error: No rightOpt found for keyword '{keyword}', setting to 'Unknown'")
        rightOpt = "Unknown"

    try:
        wrongResults.remove(rightOpt)
    except ValueError:
        pass

    return keyword, classtype.opt, rightOpt, wrongKeys, wrongResults

def generate_test_question_api(triple):
    """
    根据传入的三元组 (主语, 谓语, 宾语) 随机选择一个部分进行提问，
    并生成一道多项选择题，其中正确答案用括号标注，
    其他三个选项为相近但具有迷惑性的干扰项。
    仅返回最终测试题，不包含任何思考过程或额外说明。
    """
    question_types = [
        "Multiple Choice (MCQ)",
        "True/False",
        "Fill in the Blank",
        "Short Answer",
        "Matching",
        "Creative (Riddles, Scenario-based, Logical Reasoning)"
    ]

    # 选择一个随机题型
    selected_type = random.choice(question_types)
    
    part_names = ["主语", "谓语", "宾语"]
    idx = random.randint(0, 2)
    target_name = part_names[idx]
    correct_answer = triple[idx]

    prompt = (
    f"Generate **one** test question strictly based on the following triple:\n"
    f"- **Subject:** {triple[0]}\n"
    f"- **Predicate:** {triple[1]}\n"
    f"- **Object:** {triple[2]}\n\n"
    "### Requirements:\n"
    "- **The question must be directly related to the given triple.**\n"
    "- **It must involve all three elements of the triple.**\n"
    f"- Use the **{selected_type}** question type.\n"
    "- Ensure a **balanced mix of difficulty levels**.\n"
    "- **Do not provide answers** in the output.\n"
    "- **Avoid revealing the correct answer directly** in the question statement.\n\n"
    "### Example Questions:\n"
    "1. **MCQ:** What is the capital of China?\n"
    "   A) Shanghai  B) Guangzhou  C) Beijing  D) Shenzhen\n\n"
    "2. **True/False:** Beijing is the capital of China. (True or False?)\n\n"
    "3. **Fill in the Blank:** The capital city of China is _______.\n\n"
    "4. **Short Answer:** Which city serves as the political and administrative center of China?\n\n"
    "5. **Matching:** Match the country with its correct capital:\n"
    "   A) China - ?\n"
    "   B) France - Paris\n"
    "   C) Japan - Tokyo\n"
    "   D) Germany - Berlin\n\n"
    "6. **Riddle:** I am the heart of a nation, known for my Forbidden City. What city am I?\n\n"
    "Now generate **one** test question following these rules."
    )
    

    data = {
        #"model": "deepseek-r1:7b",
        "model": "qwen:7b",
        "prompt": prompt,
        "stream": False
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "")
    else:
        return f"请求失败: {response.status_code} {response.text}"
    


def method_5(classtype_5=country(), reps=10):
    """
    新方法：利用外部 API 根据三元组生成测试题。
    """
    global classtype
    classtype = classtype_5  # 选择主题
    print(type(classtype))
    
    quiz_table = table_generator(classtype)
    
    if not quiz_table:
        print("Error: quiz_table is empty!")
        return  # 防止后续报错
    
    for i in range(reps):
        try:
            result = table_sort4LLM(quiz_table)
            #print(f"table_sort result: {result}")  # 打印 table_sort 返回值以调试
            
            if result is None or len(result) != 5:
                print("Error: table_sort did not return expected tuple of 5 elements")
                continue  # 跳过错误数据
            
            keyword, opt, rightOpt, _, _ = result
            triple = (keyword, opt, rightOpt)
            print(triple)
            question = generate_test_question_api(triple)
            print(question)
        
        except Exception as e:
            print(f"Error in method_5 loop: {e}")

if __name__ == "__main__" :
    method_5()