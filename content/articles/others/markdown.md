Slug: markdown
Tags: markdown

[TOC]

## 前言

关于markdown的基础知识本文就不赘述了，网上随便一搜就有，本文下面主要讲了一些值得一提的知识点。

## 添加脚注

```text
这里显示如何插入脚注[^1]


[^1]: 这是一个脚注。
```

具体效果如下所示：

这里显示如何插入脚注[^1]

## 插入描述列表
```text
sqrt
: 开平方根函数，sqrt(x)。

sin
: 正弦函数，类似的还有cos，tan等，sin(x)。
```

sqrt
: 开平方根函数，sqrt(x)。

sin
: 正弦函数，类似的还有cos，tan等，sin(x)。



## github flavored markdown

gfm的官方文档在 [这里](https://help.github.com/articles/github-flavored-markdown/) 。github flavored markdown 也就是github的markdown方言，其主要区别有:

1. 下划线直接为下划线。

2. URL 直接输入，比如 <http://www.google.com> ，其将直接转化成为链接。这个只是一个新功能支持，原来的链接插入方式一样有效。

3. 删除线 用:
```text
    ~~删除线~~
```
属于添加的新特性。

4. 当然最有名的就是代码块的染色支持了。
```text
 ```elisp
(+ 1 1)
​```
```

其中语言列表可以参看 [这里](https://github.com/github/linguist/blob/master/lib/linguist/languages.yml) 。




[^1]: 这是一个脚注。