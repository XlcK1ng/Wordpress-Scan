# Lee Sin v1.0
Wordpress Vulnerability Scan

主要功能：

获取WordPress的服务器信息，主题信息，WordPress版本。
获取可能的用户名。
获取站点使用的插件，通过字典的方法。
两种方式对WordPress进行密码爆破。
对一些插件漏洞添加一些利用方式。（目前数量比较少）
连接ZoomEye，根据用户关键字和数目命令，获取相应的WordPress站点IP，批量对列表内的IP地址进行漏洞测试，生成漏洞报告(因为判定是否存在漏洞的方法写的比较简单，所以误报还是有
点多的)。

批量检测命令：python scan.py -p 2 -z –zt 5 -k ‘wordpress 3.5.1’

单一站点测试：python scan.py -u x.x.x.x -b -d ./dict/500.txt –bt 2 –sp

参数说明：

-u URL              输入单一URL
-h                  输出程序帮助
-b                  是否使用暴力破解测试
-n UNAME            指定暴力破解用户名（可以不指定）
-d PWD              指定所使用的字典
–sp                 检查安装了哪些插件
–bt BTHREADS        暴力破解线程数
–pt PTHREADS        检查插件树木的线程数
–show               显示当前可以检测的所有漏洞名称
-z                  使用钟馗之眼
-p PAGE             指定钟馗之眼页数
-k KEYWORD          指定使用关键字
–zt ZOOMEYETHREAD   指定批量测试线程数
-v                  查看当前版本

