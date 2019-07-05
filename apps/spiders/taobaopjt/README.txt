1.页面宝贝链接
<body>
<div class="grid-left">

右边栏(动态分析https://tmatch.simba.taobao.com/?name=tbuad&o=j&pid=420434_1006&count=16&keyword=T%D0%F4&p4p=tbcc_p4p_c2015_8_130027_15338028185251533802825159&catid=50344007&se=84ab6f948fa9b022d20d419cd76276eb)
"URL", "TITLE", "SELL"

左边栏(静态)
"picUrl"
2.主图
<div clas="tb-booth tb-pic tb-main-pic">

3.宝贝缩略图
<div class="tb-pic tb-s50"></div>

4.宝贝标题
<h3 class="tb-main-title"></h3>

5.价格
<strong id="J_StrPrice">        静态(原价)
<strong class="tb-promo-price"> 动态显示
                    
6.分析得评论内容链接(GET) https://rate.taobao.com/feedRateList.htm?auctionNumId=568626937384&userNumId=2609164698&currentPageNum=1&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098

7.评论总结论及好差评(GET)
https://rate.taobao.com/detailCommon.htm?auctionNumId=568626937384&userNumId=2609164698&ua=098

8.分析得评论内容
date:
content: "*"

9.大家印象
https://rate.taobao.com/detailCommon.htm?auctionNumId=570650821975&userNumId=1080001706&ua=098

分析过程:
1) 进入页面
2) 获取页面宝贝链接,价格,付款人数,title
3) 进入该链接,获取主图片一张,原价格,评论数,交易成功数,人气数
4) 获取大家印象,好评,追评,中评,差评人数以及累积评论前100个评论(包括评论内容,评论时间)