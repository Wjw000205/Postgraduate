from pypdf import PdfReader

def pdf_read():
    # 打开 PDF 文件
    reader = PdfReader("paper_dir/downloaded-paper.pdf")

    # 获取元数据
    metadata = reader.metadata
    # print(metadata)  # 输出: {'/Title': 'Example PDF', '/Author': 'John Doe', ...}
    #
    # # 获取页面数
    # print(len(reader.pages))  # 输出页面数

    # i=0
    # # 提取第一页文本
    # while i<len(reader.pages):
    #     page = reader.pages[i]
    #     print(page.extract_text())
    #     i=i+1
    res = ""
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        res = res+page.extract_text()
    print(res)

    return res