"""
##################################################################################
为迁移站点，创建转向链接页面。
为每个已有的站点html文件生成一个页面；将生成的文件上传到你的就网站。
关于在页面文件生成时或者之后再脚本中执行上传的访问，请参考本书稍后
关于fptlib部分。
##################################################################################
"""
import os

servename = 'learning-python.com'      # 站点迁移的目的地
homedir = 'books'                      # 站点根目录
sitefiledir = r'C:\temp\public_html'   # 站点文件在本地的路径
uploaddir = r'C:\temp\isp-forward'     # 准备存放转向链接文件的目录
templatename = 'template.html'         # 待生成的页面的模板

try:
    os.mkdir(uploaddir)                # 如有需要则创建上传目录
except OSError:
    pass

template = open(templatename).read()   # 载入或导入模板文件
sitefiles = os.listdir(sitefiledir)    # 文件名， 前面不带目录

count = 0
for filename in sitefiles:
    if filename.endswith('.html') or filename.endswith('.htm'):
        fwdname = os.path.join(uploaddir, filename)
        print('creating', filename, 'as', fwdname)
        filetext = template.replace('$server$', servename)  # 插入文本
        filetext = template.replace('$home$', homedir)      # 然后写入
        filetext = template.replace('$file$', filename)     # 文件不同
        open(fwdname, 'w').write(filetext)
        count += 1

print('Last file =>\n', filetext, sep='')
print('Done:', count, 'forward files created.')