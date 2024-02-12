from jinja2 import Template

name = 'Fedor'
tm = Template("Hello {{ name }}")
msg = tm.render(name=name)
print(msg)

