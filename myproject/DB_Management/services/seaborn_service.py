import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import matplotlib

# Встановлюємо бекенд 'Agg', щоб графіки генерувалися без вікон GUI (важливо для сервера)
matplotlib.use('Agg')


class SeabornVisualizationService:
    def __init__(self):
        self.style = "whitegrid"
        sns.set_style(self.style)

    def _get_image(self) -> str:
        """Допоміжний метод: конвертує графік у base64 рядок"""
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()  # Обов'язково закриваємо, щоб звільнити пам'ять

        graphic = base64.b64encode(image_png)
        return graphic.decode('utf-8')

    def generate_author_chart(self, df) -> str:
        if df.empty: return None
        plt.figure(figsize=(10, 6))
        sns.barplot(x='books_count', y='full_name', data=df, palette='viridis')
        plt.title('Топ авторів')
        plt.xlabel('Кількість книг')
        plt.ylabel('Автор')
        return self._get_image()

    def generate_genre_chart(self, df) -> str:
        if df.empty: return None
        plt.figure(figsize=(8, 8))
        # Використовуємо values та index, бо df згрупований
        plt.pie(df['total_sold'], labels=df['genre'], autopct='%1.1f%%', startangle=140)
        plt.title('Популярність жанрів')
        return self._get_image()

    def generate_sales_chart(self, df) -> str:
        if df.empty: return None
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='month_str', y='total_revenue', data=df, marker='o', linewidth=2.5, color='#2ecc71')
        plt.title('Динаміка продажів')
        plt.xlabel('Місяць')
        plt.ylabel('Дохід (грн)')
        plt.xticks(rotation=45)
        return self._get_image()

    def generate_customer_chart(self, df) -> str:
        if df.empty: return None
        plt.figure(figsize=(10, 6))
        sns.barplot(x='total_spent', y='name', data=df.head(10), palette='Blues_d')
        plt.title('Топ клієнтів')
        plt.xlabel('Витрачено (грн)')
        plt.ylabel('Клієнт')
        return self._get_image()

    def generate_stock_chart(self, df) -> str:
        if df.empty: return None
        plt.figure(figsize=(10, 6))
        sns.barplot(x='total_books', y='location', data=df, palette='Reds_d')
        plt.title('Склади з дефіцитом')
        plt.xlabel('Залишок книг')
        plt.ylabel('Склад')
        return self._get_image()


    def generate_publisher_chart(self, df) -> str:
        if df.empty: return None
        plt.figure(figsize=(10, 6))
        # Беремо топ-15, щоб графік не був перевантажений
        sns.barplot(x='books_published', y='name', data=df.head(15), palette='magma')
        plt.title('Книги за видавництвами')
        plt.xlabel('Кількість виданих книг')
        plt.ylabel('Видавництво')
        return self._get_image()