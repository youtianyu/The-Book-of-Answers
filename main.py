import os
import time
import json
import random
import streamlit as st
st.set_page_config(page_title="答案之书",page_icon=":blue_book:",layout="wide",menu_items={
    'Get Help': 'https://github.com/',
    'Report a bug': 'https://github.com/',
    'About': '  这是一个基于Python的答案之书，使用Streamlit制作\n文献提供者:作业帮\n程序制作者:我、python和streamlit的开发者\n哪些人可以使用程序:只有学生，老师勿用'
})
def stream_data(text):
    for word in list(text):
        yield word
        time.sleep(0.005)
if "loder" not in st.session_state:
    with st.spinner("Loading..."):
        time.sleep(1)
    st.session_state.loder = True
    st.rerun()
if "login" not in st.session_state:
    st.session_state.login = False
if st.session_state.login == False:
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
    st.sidebar.title("  ")
    data = json.load(open("data.json","r",encoding="utf-8"))
    st.title(":blue[答案之书] :blue_book:")
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
                                            mode = st.selectbox("    ",["流光","12px","14px","16px","18px","20px","22px","24px","26px","28px","30px","32px","34px","36px","38px","40px"])
                                        if abs(0-(mtrl_num-1))>1:
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
                                                    st.image(i,caption=f"第{mtrl_ls_dir.index(i)+1}章",use_column_width=True)
                                                elif i.endswith(".txt"):
                                                    with open(i,"r",encoding="utf-8") as f:
                                                        with st.container(height=max(1000//(abs(u_mtrl_range[0]-u_mtrl_range[1])+1),500),border=True):
                                                            dh_data = f.read()
                                                            if "\n" in dh_data:
                                                                for i3 in dh_data.split("\n"):
                                                                    if mode == "流光":
                                                                        st.write_stream(stream_data(i3))
                                                                    else:
                                                                        st.markdown(f"<p style='font-size:{mode};'>{i3}</p>", unsafe_allow_html=True)
                                                            else:
                                                                if mode == "流光":
                                                                    st.write_stream(stream_data(f.read()))
                                                                else:
                                                                    st.markdown(f"<p style='font-size:{mode};'>{f.read()}</p>", unsafe_allow_html=True)
                                                        st.caption(f"{mtrl_name} 第{i2+1}章")
                                                else:
                                                    st.warning("未知文件类型")
                                                dbs.append(i)
                                        import io
                                        import zipfile
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

