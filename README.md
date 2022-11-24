
## Install
pip3 install jinja2 pandas openpyxl

## Usage:
```
python3 generator.py --input ~/Downloads/test.xlsx --sheet="Trait List_FULL" --level=debug --dest output --attr="Colour Hints" --attr="Element"
```

## input excel文件格式
```
 必要字段:
   Title TokenId Description Image(或ImagePrefix 和 ImageSuffix,这时根据公式Image = ImagePrefix + TokenId + ImageSuffix 可得Image)
   Title 和 TokenId可以拼成name字段,格式为 Title #TokenId
 可选字段:
   AnimationURL WebImage WebAnimationURL ExternalLink Attributes
   AnimationURL WebImage WebAnimationURL不存在时使用Image(或ImagePrefix + TokenId + ImageSuffix)字段
   Attributes字段是一个json字符串(比如: {"k1":"v1","k2":"v2"}),用来生成attributes
   另外生成attributes还可以通过命令参数--attr来指定excel文件中的列名，比如--attr="Element",这时会在metadata中attributes添加了key为Element值为其对应的excel单元格中的数据的属性
   Attributes 字段 和 命令行参数--attr一同决定了attributes所有属性，两者叠加

```