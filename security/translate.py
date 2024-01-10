from googletrans import Translator
import pandas as pd

# Sample data (replace this with your actual data)
data = {
    'Organization': ['贵州省电子认证科技有限公司', '河南大河网数字科技有限公司', '南方新闻网', '南宁市大数据发展局', '南昌市人民政府办公厅', '首都之窗运行管理中心', '安庆市数据资源管理局',
                     '重庆市人民政府办公厅', '无锡市人民政府办公室', '福建省政务门户网站运营管理有限公司', '温州市大数据发展管理局', '湖北省大数据中心', '江苏省人民政府办公厅', '中国电信股份有限公司四川分公司',
                     '滁州市人民政府办公室', '湖南省人民政府发展研究中心', '九江市人民政府办公室', '淮南市人民政府办公室', '宿州市大数据中心'],
    'Count': [371, 82, 76, 49, 48, 47, 45, 44, 44, 44, 44, 44, 44, 43, 43, 43, 43, 42, 42]
}

# Create DataFrame
df_table = pd.DataFrame(data)

# Google Translate
translator = Translator()
df_table['Translated_Organization'] = df_table['Organization'].apply(lambda x: translator.translate(x, src='zh-cn', dest='en').text)

# Display the translated table
print(df_table[['Translated_Organization', 'Count']])
