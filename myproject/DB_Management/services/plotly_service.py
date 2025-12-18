import plotly.express as px
import plotly.offline as opy
import pandas as pd


class PlotlyVisualizationService:

    def __init__(self):
        # Використовуємо сучасну світлу тему для всіх графіків
        self.template = "plotly_white"

    def _get_html_div(self, fig) -> str:
        return opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)

    def generate_author_bar(self, df: pd.DataFrame) -> str:
        """1. Кількість книг за авторами (Bar Chart)"""
        if df.empty: return ""

        # Об'єднуємо ім'я та прізвище для осі Y
        df['full_name'] = df['firstname'] + ' ' + df['lastname']

        fig = px.bar(
            df, x='books_count', y='full_name', orientation='h',
            title="Кількість виданих книг за авторами",
            labels={'books_count': 'Кількість книг', 'full_name': 'Автор'},
            template=self.template,
            color='books_count',
            color_continuous_scale='Viridis'
        )
        return self._get_html_div(fig)

    def generate_genre_pie(self, df: pd.DataFrame) -> str:
        """2. Популярність жанрів (Pie Chart)"""
        if df.empty: return ""

        fig = px.pie(
            df, values='total_sold', names='genre',
            title="Частка продажів за жанрами",
            template=self.template,
            hole=0.3  # Робимо діаграму "кільцевою" (Donut chart)
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return self._get_html_div(fig)

    def generate_sales_line(self, df: pd.DataFrame) -> str:
        """3. Динаміка прибутку (Line Chart)"""
        if df.empty: return ""

        fig = px.line(
            df, x='month', y='total_revenue',
            title="Динаміка доходу по місяцях",
            labels={'month': 'Місяць', 'total_revenue': 'Сума (грн)'},
            markers=True,
            template=self.template
        )
        fig.update_traces(line_color='#2ecc71', line_width=3)
        return self._get_html_div(fig)

    def generate_customer_bar(self, df: pd.DataFrame) -> str:
        """4. Топ клієнтів (Bar Chart)"""
        if df.empty: return ""

        df['name'] = df['customerid__firstname'] + ' ' + df['customerid__lastname']
        fig = px.bar(
            df, x='name', y='total_spent',
            title="Топ клієнтів за сумою покупок",
            labels={'name': 'Клієнт', 'total_spent': 'Витрачено (грн)'},
            template=self.template,
            color='total_spent',
            color_continuous_scale='Bluered'
        )
        return self._get_html_div(fig)

    def generate_publisher_bar(self, df: pd.DataFrame) -> str:
        """5. Статистика видавництв (Bar Chart)"""
        if df.empty: return ""

        fig = px.bar(
            df, x='name', y='books_published',
            title="Кількість книг у базі за видавництвами",
            labels={'name': 'Видавництво', 'books_published': 'Кількість книг'},
            template=self.template
        )
        return self._get_html_div(fig)

    def generate_stock_bar(self, df: pd.DataFrame) -> str:
        """6. Дефіцит на складах (Bar Chart)"""
        if df.empty: return ""

        fig = px.bar(
            df, x='location', y='total_books',
            title="Склади з критичним залишком (< 100 од.)",
            labels={'location': 'Локація складу', 'total_books': 'Всього книг'},
            template=self.template
        )
        # Виділяємо червоним для привернення уваги
        fig.update_traces(marker_color='#e74c3c')
        return self._get_html_div(fig)