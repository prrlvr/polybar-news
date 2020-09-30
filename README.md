# polybar-news

#### Optional dependancie:
[rofi](https://github.com/davatorium/rofi)
#### Module configuration :
```
[module/news]
type = custom/script
interval = 300
format = <label>
format-foreground = #c1cdcd
exec = python ~/.config/polybar/news.py polybar
click-left = rofi -modi news:"~/.config/polybar/news.py" -show
```
