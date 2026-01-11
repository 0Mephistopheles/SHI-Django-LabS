import plotly.graph_objs as go
import plotly.offline as opy

class PlotlyVisualizationService:
    def __init__(self):
        self.template = "plotly_white"

    def _get_html_div(self, fig) -> str:
        """Допоміжний метод для генерації HTML div"""
        return opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False)

    def generate_author_bar(self, df) -> str:
        """Горизонтальний графік: Топ авторів за кількістю книг"""
        if df.empty:
            return "<div class='alert alert-info'>Даних не знайдено</div>"

        fig = go.Figure(data=[go.Bar(
            x=df['books_count'].tolist(),
            y=df['full_name'].tolist(),
            orientation='h',
            marker=dict(
                color=df['books_count'].tolist(),
                colorscale='Viridis',
                showscale=True
            ),
            hovertemplate='<b>%{y}</b><br>Книг: %{x}<extra></extra>'
        )])

        fig.update_layout(
            title="Кількість виданих книг",
            template=self.template,
            yaxis=dict(autorange="reversed")  # Щоб топ був зверху
        )
        return self._get_html_div(fig)

    def generate_genre_pie(self, df) -> str:
        """Кругова діаграма: Популярність жанрів"""
        if df.empty:
            return "<div class='alert alert-info'>Даних не знайдено</div>"

        fig = go.Figure(data=[go.Pie(
            labels=df['genre'].tolist(),
            values=df['total_sold'].tolist(),
            hole=0.3,
            hovertemplate='<b>%{label}</b><br>Продано: %{value}<br>Частка: %{percent}<extra></extra>'
        )])

        fig.update_layout(
            title="Популярність жанрів",
            template=self.template
        )
        return self._get_html_div(fig)

    def generate_sales_line(self, df) -> str:
        """Лінійний графік: Динаміка доходу"""
        if df.empty:
            return "<div class='alert alert-info'>Немає продажів</div>"

        fig = go.Figure(data=[go.Scatter(
            x=df['month'].tolist(),
            y=df['total_revenue'].tolist(),
            mode='lines+markers',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=8),
            hovertemplate='Місяць: %{x}<br>Дохід: %{y} грн<extra></extra>'
        )])

        fig.update_layout(
            title="Динаміка доходу",
            template=self.template
        )
        return self._get_html_div(fig)

    def generate_customer_bar(self, df) -> str:
        """Стовпчиковий графік: Топ клієнтів"""
        if df.empty:
            return "<div class='alert alert-info'>Клієнтів не знайдено</div>"

        fig = go.Figure(data=[go.Bar(
            x=df['name'].tolist(),
            y=df['total_spent'].tolist(),
            marker=dict(color='#3498db'), # Синій колір
            hovertemplate='<b>%{x}</b><br>Витрачено: %{y} грн<extra></extra>'
        )])

        fig.update_layout(
            title="Топ клієнтів",
            template=self.template
        )
        return self._get_html_div(fig)

    def generate_publisher_bar(self, df) -> str:
        """Стовпчиковий графік: Книги за видавництвами"""
        if df.empty:
            return ""

        fig = go.Figure(data=[go.Bar(
            x=df['name'].tolist(),
            y=df['books_published'].tolist(),
            marker=dict(color='#9b59b6'), # Фіолетовий колір
            hovertemplate='<b>%{x}</b><br>Книг: %{y}<extra></extra>'
        )])

        fig.update_layout(
            title="Книги за видавництвами",
            template=self.template
        )
        return self._get_html_div(fig)

    def generate_stock_bar(self, df) -> str:
        """Стовпчиковий графік: Склади з дефіцитом"""
        if df.empty:
            return "<div class='alert alert-success'>Дефіциту немає</div>"

        fig = go.Figure(data=[go.Bar(
            x=df['location'].tolist(),
            y=df['total_books'].tolist(),
            marker=dict(color='#e74c3c'),  # Червоний колір (warning)
            hovertemplate='<b>%{x}</b><br>Залишок: %{y}<extra></extra>'
        )])

        fig.update_layout(
            title="Склади з дефіцитом",
            template=self.template
        )
        return self._get_html_div(fig)

    def generate_concurrency_chart(self, results) -> str:
        """Лінійний графік: Залежність часу виконання від кількості потоків"""
        if not results:
            return "<div class='alert alert-info'>Дані відсутні</div>"

        # Розпаковуємо дані для графіку
        workers = [r['workers'] for r in results]
        times = [r['execution_time'] for r in results]

        # Формуємо текст для наведення курсору (hover)
        hover_text = [
            f"Потоків: {r['workers']}<br>Загальний час: {r['execution_time']:.3f}с<br>Сер. час/запит: {r['avg_time_per_request']:.4f}с"
            for r in results
        ]

        fig = go.Figure()

        # Лінія загального часу виконання
        fig.add_trace(go.Scatter(
            x=workers,
            y=times,
            mode='lines+markers',
            name='Час виконання',
            line=dict(color='#e74c3c', width=3, shape='spline'),  # Червоний колір для "стрес-тесту"
            marker=dict(size=10, color='#c0392b'),
            text=hover_text,
            hoverinfo='text'
        ))

        fig.update_layout(
            title="Ефективність багатопоточності (Stress Test)",
            xaxis_title="Кількість потоків (Workers)",
            yaxis_title="Загальний час виконання (сек)",
            template=self.template,
            xaxis=dict(
                tickmode='array',
                tickvals=workers,  # Показувати тільки ті значення, які ми тестували
                showgrid=True
            ),
            hovermode="x unified"
        )
        return self._get_html_div(fig)