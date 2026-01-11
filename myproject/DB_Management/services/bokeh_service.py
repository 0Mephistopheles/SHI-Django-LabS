from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import cumsum
from bokeh.palettes import Viridis256, Turbo256, Category20c
from math import pi
import pandas as pd

class BokehVisualizationService:
    def __init__(self):
        self.plot_height = 350
        # Використовуємо responsive sizing
        self.sizing_mode = 'scale_width'

    def _get_components(self, plot) -> str:
        """Повертає HTML (script + div) для вставки в шаблон"""
        script, div = components(plot)
        return f"{script}\n{div}"

    def _empty_alert(self, text="Даних не знайдено"):
        return f"<div class='alert alert-info'>{text}</div>"

    def generate_author_bar(self, df) -> str:
        """Горизонтальний графік: Топ авторів"""
        if df.empty: return self._empty_alert()

        # [FIX] Робимо копію, щоб не змінювати оригінал
        df = df.copy()

        # 1. Генеруємо палітру кольорів
        authors = df['full_name'].tolist()
        count = len(authors)
        
        if count > 0:
            step = max(1, 256 // count)
            colors = [Viridis256[i * step % 256] for i in range(count)]
        else:
            colors = []

        # 2. [ВАЖЛИВО] Додаємо кольори як колонку в DataFrame
        df['color'] = colors[:count]

        source = ColumnDataSource(df)
        
        p = figure(y_range=authors, height=self.plot_height, title="Кількість виданих книг",
                   toolbar_location=None, tools="", sizing_mode=self.sizing_mode)
        
        # 3. Посилаємось на колонку 'color'
        p.hbar(y='full_name', right='books_count', height=0.8, source=source,
               line_color="white", fill_color='color')

        p.add_tools(HoverTool(tooltips=[("Автор", "@full_name"), ("Книг", "@books_count")]))
        p.x_range.start = 0
        
        return self._get_components(p)

    def generate_genre_pie(self, df) -> str:
        """Кругова діаграма: Жанри"""
        if df.empty: return self._empty_alert()

        df = df.copy()
        
        # Розрахунок кутів
        total = df['total_sold'].sum()
        df['angle'] = df['total_sold'] / total * 2 * pi
        
        # Розрахунок кольорів
        count = len(df)
        if count > 20:
             # Для великої кількості беремо повторювану палітру
             palette = Category20c[20] * (count // 20 + 1)
        else:
             # Для малої - Turbo256
             step = max(1, 256 // count)
             palette = [Turbo256[i*step % 256] for i in range(count)]
             
        df['color'] = palette[:count]

        source = ColumnDataSource(df)

        p = figure(height=self.plot_height, title="Популярність жанрів",
                   toolbar_location=None, tools="hover", tooltips="@genre: @total_sold", 
                   x_range=(-0.5, 1.0), sizing_mode=self.sizing_mode)

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='genre', source=source)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        return self._get_components(p)

    def generate_sales_line(self, df) -> str:
        """Лінійний графік: Динаміка"""
        if df.empty: return self._empty_alert("Немає продажів")

        source = ColumnDataSource(df)

        p = figure(title="Динаміка доходу", x_axis_type="datetime", height=self.plot_height,
                   toolbar_location=None, tools="", sizing_mode=self.sizing_mode)

        # Тут колір один для всіх точок, тому можна передавати hex-рядок
        p.line(x='month', y='total_revenue', source=source, line_width=3, color='#2ecc71', legend_label="Дохід")
        p.circle(x='month', y='total_revenue', source=source, size=8, color='#27ae60', fill_color="white")

        p.add_tools(HoverTool(tooltips=[("Дата", "@month_str"), ("Сума", "@total_revenue{0.00} грн")]))
        p.legend.location = "top_left"

        return self._get_components(p)

    def generate_customer_bar(self, df) -> str:
        """Стовпчиковий: Клієнти"""
        if df.empty: return self._empty_alert("Клієнтів не знайдено")

        source = ColumnDataSource(df)
        customers = df['name'].tolist()

        p = figure(x_range=customers, height=self.plot_height, title="Топ клієнтів",
                   toolbar_location=None, tools="", sizing_mode=self.sizing_mode)

        p.vbar(x='name', top='total_spent', width=0.7, source=source,
               line_color="white", fill_color="#3498db")

        p.add_tools(HoverTool(tooltips=[("Клієнт", "@name"), ("Витрачено", "@total_spent{0.00} грн")]))
        p.xgrid.grid_line_color = None
        p.y_range.start = 0

        return self._get_components(p)

    def generate_publisher_bar(self, df) -> str:
        """Стовпчиковий: Видавництва"""
        if df.empty: return ""

        source = ColumnDataSource(df)
        pubs = df['name'].tolist()

        p = figure(x_range=pubs, height=self.plot_height, title="Книги за видавництвами",
                   toolbar_location=None, tools="", sizing_mode=self.sizing_mode)

        p.vbar(x='name', top='books_published', width=0.7, source=source,
               line_color="white", fill_color="#9b59b6") 

        p.add_tools(HoverTool(tooltips=[("Видавництво", "@name"), ("Книг", "@books_published")]))
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = 1.0

        return self._get_components(p)

    def generate_stock_bar(self, df) -> str:
        """Стовпчиковий: Дефіцит"""
        if df.empty: return "<div class='alert alert-success'>Дефіциту немає</div>"

        source = ColumnDataSource(df)
        locs = df['location'].tolist()

        p = figure(x_range=locs, height=self.plot_height, title="Склади з дефіцитом",
                   toolbar_location=None, tools="", sizing_mode=self.sizing_mode)

        p.vbar(x='location', top='total_books', width=0.7, source=source,
               line_color="white", fill_color="#e74c3c")

        p.add_tools(HoverTool(tooltips=[("Склад", "@location"), ("Залишок", "@total_books")]))
        p.xgrid.grid_line_color = None
        p.y_range.start = 0

        return self._get_components(p)