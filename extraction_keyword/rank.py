from rake_japanese import Rake

text = """
ラーメンが大好きです。特に味噌ラーメンが好きで、週に2回は食べに行きます。
ラーメンのスープの濃厚さが決め手で、最近では新しい店を開拓しています。
"""

rake = Rake()
keywords = rake.run(text)
print("抽出されたキーワード:", keywords)
