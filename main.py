import os
import io
import time
import json
import zipfile
import streamlit as st
st.set_page_config(page_title="答案之书",page_icon="icon.png",layout="wide",menu_items={
    'Get Help': 'https://github.com/youtianyu/The-Book-of-Answers/tree/main',
    'Report a bug': 'https://github.com/youtianyu/The-Book-of-Answers/tree/main',
    'About': '  这是一个基于Python的答案之书，使用Streamlit制作! 哪些人可以使用"答案之书":只有学生，老师勿用'
})
if os.path.exists("set_rq_height.txt"):
    with open("set_rq_height.txt", "r", encoding="utf-8") as f:
        rq_height = int(f.read())
else:
    with open("set_rq_height.txt", "w", encoding="utf-8") as f:
        f.write("500")
    rq_height = 500
if os.path.exists("publicity.txt"):
    with open("publicity.txt", "r", encoding="utf-8") as f:
        additionalcode = f.read()
else:
    with open("publicity.txt", "w", encoding="utf-8") as f:
        f.write("")
    additionalcode = ""
settings = {
    "additionalcode": additionalcode,
    "long_term_file":"data/"
}
def write_stream(response):
    global total_tokens,text
    text = ""
    total_tokens = 0
    for i in response:
        v = i.choices[0].delta.content
        yield v 
        try:
            text += v
            total_tokens += i.usage.total_tokens
        except:
            pass
def stream_data(text):
    for word in list(text):
        yield word
        time.sleep(0.005)
def count_files_in_directory(directory):
    file_count = 0
    for entry in os.scandir(directory):
        if entry.is_file():
            file_count += 1
    return file_count
def get_folder_size_num(folder_path):
    total_size = 0
    total_num = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, f))
            total_num += 1
    return total_size,total_num
if not "mode" in st.session_state:
    st.session_state["mode"] = "books"
if "loder" not in st.session_state:
    with st.spinner("Loading..."):
        time.sleep(1)
    st.session_state.loder = True
    st.rerun()
if "login" not in st.session_state:
    st.session_state.login = False
if os.path.exists("is_login_free_mode.txt"):
    with open("is_login_free_mode.txt", "r", encoding="utf-8") as f:
        is_login_free_mode = f.read()
else:
    is_login_free_mode = "disable"
    open("is_login_free_mode.txt", "w", encoding="utf-8").write(is_login_free_mode)
if st.session_state.login == False:
    if is_login_free_mode == "disable":
        coll,colc,colr = st.columns([1,2,1])
        with colc:
            st.title("  ")
            st.title("        :blue[登录]")
            user = st.text_input("用户名",value="root")
            password = st.text_input("密码",type="password")
            if st.button("登录"):
                if user == st.secrets.user_password.user and password == st.secrets.user_password.password:
                    st.session_state.login = True
                    st.info("授予访问权限")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
                    time.sleep(1)
                    st.rerun()
    else:
        st.session_state.login = True
        st.rerun()
elif st.session_state['mode'] == "books":
    st.sidebar.title(":blue[答案之书] :blue_book:")
    r_mode = st.sidebar.radio("功能:",[":red[查找答案]",":orange[AI求解]",":green[更多信息]",":blue[设置]"])
    if r_mode == ":red[查找答案]":
        st.title(":red[答案之书]")
        data = json.load(open("data.json","r",encoding="utf-8"))
        st.caption("在**右侧**选择您的练习册，然后点击 _“下载”_ 按钮，下载字典。")
        st.divider()
        if not os.path.exists("data.json"):
            st.error("数据文件不存在")
        else:
            if data == {}:
                st.error("数据为空")
            else:
                subject = st.sidebar.selectbox("练习册:",list(data.keys()))
                if subject in data:
                    if data[subject] != {}:
                        sub_class = st.sidebar.selectbox("类:",list(data[subject].keys()))
                        if data[subject][sub_class] != {}:
                            sub_material = st.sidebar.selectbox("模块:",list(data[subject][sub_class].keys()))
                            if data[subject][sub_class][sub_material] != {}:
                                mtrl_data = data[subject][sub_class][sub_material]
                                mtrl_name = mtrl_data["name"]
                                mtrl_date = mtrl_data["date"]
                                mtrl_dir = mtrl_data["dir"]
                                if os.path.exists(mtrl_dir):
                                    mtrl_ls_dir = os.listdir(mtrl_dir)
                                    mtrl_num = len(mtrl_ls_dir)
                                    if mtrl_num != 0:
                                        st.caption(f"名称: **{mtrl_name}**")
                                        st.caption(f"添加日期: **{mtrl_date}**")
                                        st.caption(f"文件地址: **{mtrl_dir}**")
                                        with st.expander("配置",expanded=True,icon="⚙️"):
                                            coll5,colr5,_ = st.columns([1,4,10])
                                            with coll5:
                                                st.write("  ")
                                                st.write("  ")
                                                st.write("字体:")
                                            with colr5:                                    
                                                mode = st.selectbox("    ",["流","12px","14px","16px","18px","20px","22px","24px","26px","28px","30px","32px","34px","36px","38px","40px"])
                                            if abs(0-(mtrl_num-1))>0:
                                                u_mtrl_range = st.slider("选择一个范围:",0,mtrl_num-1,[0,0])
                                            else:
                                                u_mtrl_range = (0,0)
                                        mtrl_ls_dir = sorted(mtrl_ls_dir)
                                        mtrl_ls_dir = [mtrl_dir + os.sep + i for i in mtrl_ls_dir]
                                        if u_mtrl_range[0] == 0 and u_mtrl_range[1] > 5:
                                            st.warning("只能选择5章答案")
                                        else:
                                            with st.spinner("正在加载..."):
                                                dbs = []
                                                for i2 in range(u_mtrl_range[0],u_mtrl_range[1]+1):
                                                    i = mtrl_ls_dir[i2]
                                                    if i.endswith(".png") or i.endswith(".jpg") or i.endswith(".jpeg"):
                                                        st.image(i,caption=f"第{mtrl_ls_dir.index(i)+1}章  "+str(i),use_column_width=True)
                                                    elif i.endswith(".txt"):
                                                        with open(i,"r",encoding="utf-8") as f:
                                                            with st.container(height=max(1000//(abs(u_mtrl_range[0]-u_mtrl_range[1])+1),rq_height),border=True):
                                                                dh_data = f.read()
                                                                if "\n" in dh_data:
                                                                    for i3 in dh_data.split("\n"):
                                                                        if mode == "流":
                                                                            st.write_stream(stream_data(i3))
                                                                        else:
                                                                            st.markdown(f"<p style='font-size:{mode};'>{i3}</p>", unsafe_allow_html=True)
                                                                else:
                                                                    if mode == "流":
                                                                        st.write_stream(stream_data(f.read()))
                                                                    else:
                                                                        st.markdown(f"<p style='font-size:{mode};'>{f.read()}</p>", unsafe_allow_html=True)
                                                            st.caption(f"{mtrl_name} 第{i2+1}章  "+str(i))
                                                    elif i.endswith(".py"):
                                                        show_code = False
                                                        with open(i,"r",encoding="utf-8") as f:
                                                            with st.container(height=max(1000//(abs(u_mtrl_range[0]-u_mtrl_range[1])+1),rq_height),border=True):
                                                                py_data = f.read()
                                                                with st.spinner("正在运行控件..."):
                                                                    try:
                                                                        exec(py_data,globals())
                                                                        show_code = True
                                                                    except:
                                                                        st.error("控件运行失败")
                                                                        st.code(py_data,language="python")
                                                                        show_code = False
                                                            with st.expander("源"):
                                                                st.code(py_data,language="python")
                                                            st.caption(f"{mtrl_name} 第{i2+1}章  "+str(i))
                                                                
                                                    else:
                                                        st.warning("未知文件类型")
                                                    dbs.append(i)
                                            buffer = io.BytesIO()
                                            with zipfile.ZipFile(buffer, 'w') as zipf:
                                                for file in dbs:
                                                    # 将文件添加到ZIP文件中
                                                    zipf.write(file)
                                            buffer.seek(0)
                                            zip_bytes = buffer.read()
                                            st.sidebar.download_button(f"下载选中的{len(dbs)}个答案",data=zip_bytes,file_name=f"{mtrl_name}.zip",mime="application/zip")
                                    else:
                                        st.warning("暂无练习册")
                                else:
                                    st.warning("暂无练习册")
                            else:
                                st.warning("暂无练习册")
                        else:
                            st.warning("暂无练习册")
                    else:
                        st.warning("暂无练习册")
                else:
                    st.warning("暂无练习册")
        if st.sidebar.button("进入文件管理器"):
            st.session_state["mode"] = "manager"
            st.rerun()
        try:
            exec(settings["additionalcode"],globals())
        except:
            pass
    elif r_mode == ":orange[AI求解]":
        with st.sidebar:
            openai_api_key = st.text_input("请输入您的 API Key", key="chatbot_api_key", type="password")
        if "zhipuAI_api_key" in st.secrets:
            if openai_api_key in st.secrets.zhipuAI_api_key:
                openai_api_key = st.secrets.zhipuAI_api_key[openai_api_key]
        st.title(":orange[ChatGPT/GLM]")
        st.caption("Streamlit 聊天机器人")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "您好，我是人工智能助手。我的任务是针对用户的问题和要求提供适当的答复和支持。我可以回答各种领域的问题，包括但不限于科学、技术、历史、文化、娱乐等。如果您有任何问题，请随时向我提问。"}]
        with st.container(height=rq_height,border=False):
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])
        total_tokens = 0
        text = ""
        if os.path.exists("set_model_name.json"):
            with open("set_model_name.json", "r", encoding="utf-8") as f:
                model_name_s = json.load(f)
        else:
            model_name_s = {"openai":"gpt-4","zhipuai":"glm-4-Flash"}
            with open("set_model_name.json", "w", encoding="utf-8") as f:
                json.dump(model_name_s, f)
        if os.path.exists("set_openai_base_url.json"):
            with open("set_openai_base_url.json", "r", encoding="utf-8") as f:
                openai_base_url = json.load(f)
        else:
            openai_base_url = {"openai_base_url":0}
            with open("set_openai_base_url.json", "w", encoding="utf-8") as f:
                json.dump(openai_base_url, f)
        with st.sidebar.expander("设置"):
            if os.path.exists("set_tokens.txt"):
                with open("set_tokens.txt", "r", encoding="utf-8") as f:
                    s_tokens = int(f.read())
            else:
                with open("set_tokens.txt", "w", encoding="utf-8") as f:
                    f.write("1024")
                s_tokens = 1024
            if os.path.exists("set_ai_oset.txt"):
                with open("set_ai_oset.txt", "r", encoding="utf-8") as f:
                    ai_oset = json.load(f)
            else:
                with open("set_ai_oset.txt", "w", encoding="utf-8") as f:
                    f.write(json.dumps({"temperature":0.95,"top_p":0.8,"max_tokens":min(1024,s_tokens)}))
                ai_oset = {"temperature":0.95,"top_p":0.8,"max_tokens":min(1024,s_tokens)}
            temperature = st.number_input("温度", min_value=0.0, max_value=1.5, value=ai_oset["temperature"], step=0.01)
            top_p = st.number_input("Top P", min_value=0.0, max_value=1.0, value=ai_oset["top_p"], step=0.01)
            max_tokens = st.number_input("最大令牌数", min_value=50, max_value=s_tokens, value=min(ai_oset["max_tokens"], s_tokens), step=1)
        if st.sidebar.button("清空记录"):
            st.session_state.messages = []
        if prompt := st.chat_input():
            if not openai_api_key:
                st.info("请添加您的 OpenAI API 密钥以继续。")
            else:
                if "sk-" in openai_api_key:
                    from openai import OpenAI as ai_module
                else:
                    from zhipuai import ZhipuAI as ai_module
                # 创建对象
                if "sk-" in openai_api_key:
                    model_name = model_name_s["openai"]
                else:
                    model_name = model_name_s["zhipuai"]
                if openai_base_url["openai_base_url"] != 0:
                    ai = ai_module(api_key=openai_api_key, base_url=openai_base_url["openai_base_url"])
                else:
                    ai = ai_module(api_key=openai_api_key)
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                response = ai.chat.completions.create(model=model_name, messages=st.session_state.messages,stream=True, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
                total_tokens = 0
                text = ""
                with st.spinner("正在生成回复中..."):
                    st.chat_message("assistant").write_stream(write_stream(response))
                total_tokens = total_tokens
                msg = text
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.caption(f"总使用令牌数：{total_tokens}")
                try:
                    if os.path.exists("ai_use_count.json"):
                        with open("ai_use_count.json", "r", encoding="utf-8") as f:
                            ai_use_count = json.load(f)
                    else:
                        ai_use_count = {"use_count":0, "total_tokens":0}
                    ai_use_count["use_count"] = ai_use_count["use_count"] + 1
                    ai_use_count["total_tokens"] = ai_use_count["total_tokens"] + total_tokens
                    with open("ai_use_count.json", "w", encoding="utf-8") as f:
                        json.dump(ai_use_count, f)
                except:
                    if os.path.exists("ai_use_count.json"):
                        with open("ai_use_count.json", "r", encoding="utf-8") as f:
                            ai_use_count = json.load(f)
                    else:
                        ai_use_count = {"use_count":0, "total_tokens":0}
                    json.dump(ai_use_count, f)
        try:
            exec(settings["additionalcode"],globals())
        except:
            pass
    elif r_mode == ":green[更多信息]":
        if os.path.exists("others.txt"):
            others_data = open("others.txt", "r", encoding="utf-8").read()
        else:
            open("others.txt", "w", encoding="utf-8").write("st.info('暂无信息, 请自行添加')")
            others_data = "st.info('暂无信息, 请自行添加')"
        exec(others_data,globals())
        try:
            exec(settings["additionalcode"],globals())
        except:
            pass
    elif r_mode == ":blue[设置]":
        st.title(":blue[设置]")
        if st.sidebar.text_input("2FA-密钥", key="2FA_key", type="password") == st.secrets["2FA"]["2FA_key"]:
            if st.sidebar.button("退出"):
                if "login" in st.session_state:
                    del st.session_state.login
                if "loder" in st.session_state:
                    del st.session_state.loder
                if "messages" in st.session_state:
                    del st.session_state["messages"]
                st.rerun()
            tab0,tab1,tab2,tab3,tab4,tab6,tab5 = st.tabs(["登录","数据大小","Ai设置","更多信息","容器","公示","刷新"])
            with tab0:
                if os.path.exists("is_login_free_mode.txt"):
                    with open("is_login_free_mode.txt", "r", encoding="utf-8") as f:
                        is_login_free_mode = f.read()
                else:
                    is_login_free_mode = "disable"
                    open("is_login_free_mode.txt", "w", encoding="utf-8").write(is_login_free_mode)
                is_login_free_mode = st.selectbox("免登录模式",["disable","enable"],index=["disable","enable"].index(is_login_free_mode))
                with open("is_login_free_mode.txt", "w", encoding="utf-8") as f:
                    f.write(is_login_free_mode)
                st.info("已保存")

            with tab1:
                size,num = get_folder_size_num("data")
                st.write("数据大小为",size/1000,"千字节")
                st.write("数据文件数为",num,"个")
            with tab2:
                with st.expander("模型设置"):
                    if os.path.exists("set_model_name.json"):
                        with open("set_model_name.json", "r", encoding="utf-8") as f:
                            model_name = json.load(f)
                    else:
                        model_name = {"openai":"gpt-4","zhipuai":"glm-4-Flash"}
                        with open("set_model_name.json", "w", encoding="utf-8") as f:
                            json.dump(model_name, f)
                    openai_model =  st.text_input("openai模型", value=model_name["openai"])
                    if os.path.exists("set_openai_base_url.json"):
                        with open("set_openai_base_url.json", "r", encoding="utf-8") as f:
                            openai_base_url = json.load(f)
                    else:
                        openai_base_url = {"openai_base_url":0}
                        with open("set_openai_base_url.json", "w", encoding="utf-8") as f:
                            json.dump(openai_base_url, f)
                    if st.checkbox("添加base_url",value=(openai_base_url["openai_base_url"]!=0 and openai_base_url["openai_base_url"]!="0")):
                        openai_base_url["openai_base_url"] = st.text_input("openai_base_url", value="" if openai_base_url["openai_base_url"]==0 else openai_base_url["openai_base_url"])
                    else:
                        openai_base_url["openai_base_url"] = 0

                    zhipuai_model =  st.text_input("zhipuai模型", value=model_name["zhipuai"])
                    model_name = {"openai":openai_model,"zhipuai":zhipuai_model}
                    with open("set_model_name.json", "w", encoding="utf-8") as f:
                        json.dump(model_name, f)
                    with open("set_openai_base_url.json", "w", encoding="utf-8") as f:
                        json.dump(openai_base_url, f)
                    st.info("已保存")

                with st.expander("ai使用次数"):
                    if os.path.exists("ai_use_count.json"):
                        with open("ai_use_count.json", "r", encoding="utf-8") as f:
                            ai_use_count = json.load(f)
                    else:
                        ai_use_count = {"use_count":0, "total_tokens":0}
                    st.write("ai使用次数为",ai_use_count["use_count"],"次")
                    st.write("ai使用总令牌数为",ai_use_count["total_tokens"],"个")
                    if st.button("重置"):
                        ai_use_count = {"use_count":0, "total_tokens":0}
                        with open("ai_use_count.json", "w", encoding="utf-8") as f:
                            json.dump(ai_use_count, f)
                with st.expander("设置最大令牌数"):
                    if os.path.exists("set_tokens.txt"):
                        with open("set_tokens.txt", "r", encoding="utf-8") as f:
                            tokens = int(f.read())
                    else:
                        with open("set_tokens.txt", "w", encoding="utf-8") as f:
                            f.write("1024")
                        tokens = 1024
                    max_tokens = st.number_input("最大令牌数", min_value=50, max_value=8192, value=tokens, step=1)
                    with open("set_tokens.txt", "w", encoding="utf-8") as f:
                        f.write(str(max_tokens))
                    st.info("已保存")
                with st.expander("默认设置"):
                    if os.path.exists("set_ai_oset.txt"):
                        with open("set_ai_oset.txt", "r", encoding="utf-8") as f:
                            ai_oset = json.load(f)
                    else:
                        with open("set_ai_oset.txt", "w", encoding="utf-8") as f:
                            f.write(json.dumps({"temperature":0.95,"top_p":0.8,"max_tokens":min(1024,max_tokens)}))
                        ai_oset = {"temperature":0.95,"top_p":0.8,"max_tokens":min(1024,max_tokens)}
                    oset_temperature = st.number_input("temperature", min_value=0.0, max_value=1.5, value=ai_oset["temperature"], step=0.01)
                    oset_top_p = st.number_input("top_p", min_value=0.0, max_value=1.0, value=ai_oset["top_p"], step=0.01)
                    oset_max_tokens = st.number_input("max_tokens", min_value=50, max_value=8192, value=min(ai_oset["max_tokens"],max_tokens), step=1)
                    with open("set_ai_oset.txt", "w", encoding="utf-8") as f:
                        f.write(json.dumps({"temperature":oset_temperature,"top_p":oset_top_p,"max_tokens":oset_max_tokens}))
                    st.info("已保存")
            with tab3:
                if os.path.exists("others.txt"):
                    others_data = open("others.txt", "r", encoding="utf-8").read()
                else:
                    open("others.txt", "w", encoding="utf-8").write("st.info('暂无信息, 请自行添加')")
                    others_data = "st.info('暂无信息, 请自行添加')"
                others_data = st.text_area("      ", others_data,key="change_others_data")
                open("others.txt", "w", encoding="utf-8").write(others_data)
                st.info("已保存")
            with tab4:
                if os.path.exists("set_rq_height.txt"):
                    with open("set_rq_height.txt", "r", encoding="utf-8") as f:
                        rq_height = int(f.read())
                else:
                    with open("set_rq_height.txt", "w", encoding="utf-8") as f:
                        f.write("500")
                    rq_height = 500
                rq_height = st.number_input("容器高度", min_value=0, max_value=1400, value=rq_height, step=1)
                with open("set_rq_height.txt", "w", encoding="utf-8") as f:
                    f.write(str(rq_height))
                st.info("已保存")
            with tab6:
                if os.path.exists("publicity.txt"):
                    publicity_data = open("publicity.txt", "r", encoding="utf-8").read()
                else:
                    open("publicity.txt", "w", encoding="utf-8").write("")
                    publicity_data = ""
                publicity_data = st.text_area("      ", value = publicity_data,key="change_publicity_data")
                open("publicity.txt", "w", encoding="utf-8").write(publicity_data)
                st.info("已保存")
            with tab5:
                if st.button("刷新"):
                    st.rerun()
        else:
            if st.sidebar.button("退出"):
                if "login" in st.session_state:
                    del st.session_state.login
                if "loder" in st.session_state:
                    del st.session_state.loder
                if "messages" in st.session_state:
                    del st.session_state["messages"]
                st.rerun()
            st.warning("请输入正确的2FA密钥")
    
elif st.session_state["mode"] == "manager":
    import shutil
    datadir = settings["long_term_file"]
    if not "is_write" in st.session_state:
        st.session_state["is_write"] = False
    if "2FA" in st.secrets:
        if "2FA_key" in st.secrets["2FA"]:
            settings["password"] = st.secrets["2FA"]["2FA_key"]
    if st.session_state["is_write"] == False:
        try:
            if "password" in settings:
                # 验证身份
                password = st.sidebar.text_input("密码:", type="password")
                if not password == "":
                    if settings["password"] == password:
                        st.sidebar.info("授予写入权限")
                        st.session_state["is_write"] = True
                    else:
                        st.sidebar.warning("密码无效")
                else:
                    st.sidebar.success("请输入密码")
            else:
                st.sidebar.warning("未设置密码")
        except:
            st.rerun()
    def get_folder_structure(root_folder):
        # 初始化结果字典
        result = {}
        path = root_folder
        listdir = os.listdir(root_folder)
        for f in listdir:
            if os.path.isdir(os.path.join(path, f)):
                result[f] = get_folder_structure(os.path.join(path, f))
                # 递归调用

            else:
                result[f] = None
                # 文件路径
        return result
    def select_file(data_tree,path=".",n=0):
        list_data_tree = list(data_tree.keys())
        list_data_tree.insert(0,".")
        selected_file = st.sidebar.selectbox(" ", list_data_tree,key="file_select_"+str(n))
        if selected_file == ".":
            return path
        elif data_tree[selected_file] == None:
            return path+os.sep+selected_file
        elif data_tree[selected_file] == {}:
            return path+os.sep+selected_file
        else:
            return select_file(data_tree[selected_file],path+os.sep+selected_file,n=n+1)
    def is_dir(path,data_tree):
        path = path.split(os.sep)
        path.pop(0)
        last = ""
        while len(path)>0:
            if not path[0] == None:
                if path[0] in list(data_tree.keys()):
                    data_tree = data_tree[path[0]]
                    last = path[0]
                    path.pop(0)
                else:
                    return False
            else:
                return False
        if data_tree == None:
            return False
        else:
            return True
    data_dir = datadir
    if st.session_state["is_write"]:
        try:
            st.title(":blue[文件管理器🗂️]")
            st.caption("管理员模式")
            data_tree = get_folder_structure(data_dir)
            select_file_or_dir = select_file(data_tree)
            select_file_or_dir_abs = select_file_or_dir.replace(".",data_dir,1)
            if is_dir(select_file_or_dir,data_tree):
                if select_file_or_dir != ".":
                    st.info(select_file_or_dir.replace(os.sep," > "))
                    file_upload_tab,new_dir_tab,delete_file_tab,rename_dir_tab = st.tabs(["上传文件","新建文件夹","删除文件夹","重命名文件夹"])
                    with file_upload_tab:
                        is_overwrite = st.checkbox("覆盖已有文件",key="is_overwrite")
                        upload_file = st.file_uploader("上传文件",key="upload_file",accept_multiple_files=True)
                        if upload_file:
                            if st.button("上传",key="upload_file_button"):
                                with st.spinner("上传中..."):
                                    for file in upload_file:
                                        if is_overwrite:
                                            with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                f.write(file.read())
                                            st.success(file.name+ " 上传成功")
                                        else:
                                            if os.path.exists(select_file_or_dir_abs+os.sep+file.name):
                                                st.warning(file.name+ " 已存在")
                                            else:
                                                with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                    f.write(file.read())
                                                st.success(file.name+ " 上传成功")
                                upload_file = None
                                st.info("上传完成")
                                st.rerun()
                            else:
                                st.success("请点击上传按钮以上传文件")
                        else:
                            st.success("请选择文件")
                    with new_dir_tab:
                        new_dir_name = st.text_input("请输入文件夹名称",key="new_dir_name")
                        if new_dir_name != "":
                            new_dir = st.button("新建文件夹",key="new_folder")
                            if new_dir:
                                not_in_name = ["\\","/",">","<",":","*","?","\"","|"]
                                can_be_name = True
                                for i in not_in_name:
                                    if i in new_dir_name:
                                        can_be_name = False
                                if can_be_name:
                                    if os.path.exists(select_file_or_dir_abs+os.sep+new_dir_name):
                                        st.warning("文件夹已存在, 新建文件夹失败")
                                    else:
                                        os.mkdir(select_file_or_dir_abs+os.sep+new_dir_name)
                                        st.info("新建文件夹成功")
                                        st.rerun()
                                else:
                                    st.warning("文件夹名称不合法")
                                new_dir = False
                            else:
                                st.success("请点击新建文件夹按钮以新建文件夹")
                        else:
                            st.success("请输入文件夹名称")
                    with delete_file_tab:
                        delete_file = st.button("删除文件夹",key="delete_dir")
                        if delete_file:
                            if os.path.isdir(select_file_or_dir_abs):
                                shutil.rmtree(select_file_or_dir_abs)
                                st.info("删除文件夹成功")
                                st.rerun()
                            else:
                                st.warning("删除文件夹失败")
                            delete_file = False
                    with rename_dir_tab:
                        new_dir_name = st.text_input("请输入更名后的文件夹名称",key="rename_dir_name")
                        if new_dir_name != "":
                            rename_dir = st.button("重命名文件夹",key="rename_folder")
                            if rename_dir:
                                not_in_name = ["\\","/",">","<",":","*","?","\"","|"]
                                if os.path.isdir(select_file_or_dir_abs):
                                    can_be_name = True
                                    for i in not_in_name:
                                        if i in new_dir_name:
                                            can_be_name = False
                                    if can_be_name:
                                        renamed = (os.sep).join(select_file_or_dir_abs.split(os.sep)[:-1])+os.sep+new_dir_name
                                        print(renamed)
                                        if os.path.exists(renamed):
                                            st.warning("文件夹已存在")
                                        else:
                                            os.rename(select_file_or_dir_abs,renamed)
                                            st.info("重命名文件夹成功")
                                            st.rerun()
                                    else:
                                        st.warning("文件夹名称不合法")
                                else:
                                    st.warning("重命名文件夹失败")
                                rename_dir = False
                            else:
                                st.success("请点击重命名文件夹按钮以重命名文件夹")
                        else:
                            st.success("请输入文件夹名称")
                else:
                    st.info(select_file_or_dir.replace(os.sep," > "))
                    file_upload_tab,new_dir_tab = st.tabs(["上传文件","新建文件夹"])
                    with file_upload_tab:
                        is_overwrite = st.checkbox("覆盖已有文件",key="is_overwrite")
                        upload_file = st.file_uploader("上传文件",key="upload_file",accept_multiple_files=True)
                        if upload_file:
                            if st.button("上传",key="upload_file_button"):
                                with st.spinner("上传中..."):
                                    for file in upload_file:
                                        if is_overwrite:
                                            with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                f.write(file.read())
                                            st.success(file.name+ " 上传成功")
                                        else:
                                            if os.path.exists(select_file_or_dir_abs+os.sep+file.name):
                                                st.warning(file.name+ " 已存在")
                                            else:
                                                with open(select_file_or_dir_abs+os.sep+file.name,"wb") as f:
                                                    f.write(file.read())
                                                st.success(file.name+ " 上传成功")
                                upload_file = None
                                st.info("上传完成")
                                st.rerun()
                            else:
                                st.success("请点击上传按钮以上传文件")
                        else:
                            st.success("请选择文件")
                    with new_dir_tab:
                        new_dir_name = st.text_input("请输入文件夹名称",key="new_dir_name")
                        if new_dir_name != "":
                            new_dir = st.button("新建文件夹",key="new_folder")
                            if new_dir:
                                not_in_name = ["\\","/",">","<",":","*","?","\"","|"]
                                can_be_name = True
                                for i in not_in_name:
                                    if i in new_dir_name:
                                        can_be_name = False
                                if can_be_name:
                                    if os.path.exists(select_file_or_dir_abs+os.sep+new_dir_name):
                                        st.warning("文件夹已存在, 新建文件夹失败")
                                    else:
                                        os.mkdir(select_file_or_dir_abs+os.sep+new_dir_name)
                                        st.info("新建文件夹成功")
                                        st.rerun()
                                else:
                                    st.warning("文件夹名称不合法")
                                new_dir = False
                            else:
                                st.success("请点击新建文件夹按钮以新建文件夹")
                        else:
                            st.success("请输入文件夹名称")
            else:
                st.info(select_file_or_dir.replace(os.sep," > "))
                with st.expander("查看文件"):
                    if st.checkbox("显示文件内容",key="show_file_content"):
                        # 如果文件大小小于100M，则显示文件内容
                        if os.path.getsize(select_file_or_dir_abs) < 100*1024*1024:
                            if select_file_or_dir_abs.endswith(".txt"):
                                with open(select_file_or_dir_abs,"r",encoding="utf-8") as f:
                                    st.text(f.read())
                            elif select_file_or_dir_abs.endswith(".jpg"):
                                st.image(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".png"):
                                st.image(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".gif"):
                                st.image(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".mp4"):
                                st.video(select_file_or_dir_abs)
                            elif select_file_or_dir_abs.endswith(".mp3"):
                                st.audio(select_file_or_dir_abs,format="audio/mp3")
                            elif select_file_or_dir_abs.endswith(".wav"):
                                st.audio(select_file_or_dir_abs,format="audio/wav")
                            else:
                                st.warning("无法显示文件内容")
                        else:
                            st.warning("文件过大，无法显示文件内容")
                download,rename_dir_tab,delete_file_tab = st.tabs(["下载文件","重命名文件","删除文件"])
                with download:
                    if st.checkbox("创建下载链接",key="download_link"):
                        with open(select_file_or_dir_abs,"rb") as f:
                            st.download_button(label="下载文件",data=f,file_name=select_file_or_dir.split(os.sep)[-1])
                with delete_file_tab:
                    delete_file = st.button("删除文件",key="delete_file")
                    if delete_file:
                        if os.path.isfile(select_file_or_dir_abs):
                            with st.spinner("删除中..."):
                                os.remove(select_file_or_dir_abs)
                                st.success("删除成功")
                                st.rerun()
                        else:
                            st.warning("无法删除文件")
                with rename_dir_tab:
                    new_dir_name = st.text_input("请输入更名后的文件名称",key="rename_dir_name")
                    if new_dir_name != "":
                        rename_dir = st.button("重命名文件",key="rename_folder")
                        if rename_dir:
                            not_in_name = ["\\","/",">","<",":","*","?","\"","|"]
                            can_be_name = True
                            for i in not_in_name:
                                if i in new_dir_name:
                                    can_be_name = False
                            if can_be_name:
                                renamed = (os.sep).join(select_file_or_dir_abs.split(os.sep)[:-1])+os.sep+new_dir_name
                                print(renamed)
                                if os.path.exists(renamed):
                                    st.warning("文件已存在")
                                else:
                                    os.rename(select_file_or_dir_abs,renamed)
                                    st.info("重命名文件成功")
                                    st.rerun()
                            else:
                                st.warning("文件名称不合法")
                            rename_dir = False
                        else:
                            st.success("请点击重命名文件按钮以重命名文件")
                    else:
                        st.success("请输入文件名称")
        except:
            st.error("发现未知错误")
    else:

        # 没有写入权限，无法修改文件，无法上传文件和重命名、删除文件
        st.title(":blue[文件管理器🗂️]")
        data_tree = get_folder_structure(data_dir)
        select_file_or_dir = select_file(data_tree)
        select_file_or_dir_abs = select_file_or_dir.replace(".",data_dir,1)
        if is_dir(select_file_or_dir,data_tree):
            if select_file_or_dir != ".":
                st.info(select_file_or_dir.replace(os.sep," > "))
                st.info("这是一个文件夹，请在侧边栏选择一个文件进行操作")
                st.info("如需要更多权限，请在侧边栏输入管理员密码")
            else:
                st.info(select_file_or_dir.replace(os.sep," > "))
                st.info("这是根目录，请在侧边栏选择一个文件进行操作")
                st.info("如需要更多权限，请在侧边栏输入管理员密码")
        else:
            st.info(select_file_or_dir.replace(os.sep," > "))
            with st.expander("查看文件"):
                if st.checkbox("显示文件内容",key="show_file_content"):
                    # 如果文件大小小于100M，则显示文件内容
                    if os.path.getsize(select_file_or_dir_abs) < 100*1024*1024:
                        if select_file_or_dir_abs.endswith(".txt"):
                            with open(select_file_or_dir_abs,"r",encoding="utf-8") as f:
                                st.text(f.read())
                        elif select_file_or_dir_abs.endswith(".jpg"):
                            st.image(select_file_or_dir_abs)
                        elif select_file_or_dir_abs.endswith(".jpeg"):
                            st.image(select_file_or_dir_abs)
                        elif select_file_or_dir_abs.endswith(".png"):
                            st.image(select_file_or_dir_abs)
                        elif select_file_or_dir_abs.endswith(".gif"):
                            st.image(select_file_or_dir_abs)
                        elif select_file_or_dir_abs.endswith(".mp4"):
                            st.video(select_file_or_dir_abs)
                        elif select_file_or_dir_abs.endswith(".mp3"):
                            st.audio(select_file_or_dir_abs,format="audio/mp3")
                        elif select_file_or_dir_abs.endswith(".wav"):
                            st.audio(select_file_or_dir_abs,format="audio/wav")
                        else:
                            st.warning("无法显示文件内容")
                    else:
                        st.warning("文件过大，无法显示文件内容")
            download, = st.tabs(["下载文件"])
            with download:
                if st.checkbox("创建下载链接",key="download_link_2"):
                    with open(select_file_or_dir_abs,"rb") as f:
                        st.download_button(label="下载文件",data=f.read(),file_name=select_file_or_dir.split(os.sep)[-1])
    if st.sidebar.button("退出文件管理器"):
        st.session_state["mode"] = "books"
        st.rerun()
    try:
        exec(settings["additionalcode"],globals())
    except:
        pass
