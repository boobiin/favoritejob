import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

my_style = LS('#333366', base_style=LCS)
chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)

chart.title = 'Python Projects'
chart.x_labels = ['httpie', 'django', 'flask']

# 定义了一个plot_dicts的列表,包含了三个字典
# 分别针对项目 httpie, django, flask
# pygal根据键 value 确定条形高度， 根据 label 确定工具提示

plot_dicts = [
    {'value': 16101, 'label': 'Description of httpie'},
    {'value': 15028, 'label': 'Description of django'},
    {'value': 14798, 'label': 'Description of flask'},
]

chart.add('', plot_dicts)
chart.render_to_file('bar_descriptions.svg')