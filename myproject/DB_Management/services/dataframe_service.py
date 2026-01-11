import pandas as pd
from ..repositories.analytics_repository import AnalyticsRepository


class AnalyticsDataFrameService:
    def __init__(self):
        self.repo = AnalyticsRepository()

    def _queryset_to_df(self, queryset):
        """Допоміжний метод: перетворює QuerySet у DataFrame безпечно"""
        data = list(queryset)
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)

    def get_filtered_data(self, filters: dict):
        """
        Єдине джерело правди для всіх графіків.
        Отримує дані, чистить типи (Decimal -> float) і агрегує дублікати.
        """
        # 1. Розпаковка фільтрів
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')
        min_spent = filters.get('min_spent', 0)
        min_books = filters.get('min_books', 0)
        threshold = filters.get('threshold', 100)
        author_query = filters.get('author_query', '')
        top_genres = filters.get('top_genres')  # int або None

        # --- 1. АВТОРИ ---
        authors_qs = self.repo.get_books_count_by_author(name_query=author_query, min_books=min_books)
        df_authors = self._queryset_to_df(authors_qs)

        if not df_authors.empty:
            # Створюємо повне ім'я
            df_authors['full_name'] = df_authors['firstname'] + ' ' + df_authors['lastname']

            # [FIX] Захист від пустих імен (щоб не зникли при групуванні)
            df_authors['full_name'] = df_authors['full_name'].fillna('Невідомий автор').replace('', 'Невідомий автор')

            # [FIX] Примусовий float для Plotly
            df_authors['books_count'] = pd.to_numeric(df_authors['books_count'], errors='coerce').fillna(0).astype(
                float)

            # Агрегація
            df_authors = df_authors.groupby('full_name', as_index=False)['books_count'].sum()
            df_authors = df_authors.sort_values('books_count', ascending=False)

        # --- 2. ЖАНРИ ---
        genres_qs = self.repo.get_popularity_by_genre(top_n=None)
        df_genres = self._queryset_to_df(genres_qs)

        if not df_genres.empty:
            # [FIX] Заповнюємо пусті жанри
            df_genres['genre'] = df_genres['genre'].fillna('Інше').replace('', 'Інше')

            # [FIX] Примусовий float
            df_genres['total_sold'] = pd.to_numeric(df_genres['total_sold'], errors='coerce').fillna(0).astype(float)

            # Групування
            df_genres = df_genres.groupby('genre', as_index=False)['total_sold'].sum()
            df_genres = df_genres.sort_values('total_sold', ascending=False)

            # Обрізаємо топ тільки ПІСЛЯ групування
            if top_genres:
                df_genres = df_genres.head(int(top_genres))

        # --- 3. ПРОДАЖІ ---
        sales_qs = self.repo.get_monthly_sales_dynamics(start_date, end_date)
        df_sales = self._queryset_to_df(sales_qs)

        if not df_sales.empty:
            # [FIX] Примусовий float (тут часто приходить Decimal з бази)
            df_sales['total_revenue'] = pd.to_numeric(df_sales['total_revenue'], errors='coerce').fillna(0).astype(
                float)

            # Групування по місяцях
            df_sales = df_sales.groupby('month', as_index=False)['total_revenue'].sum()
            df_sales = df_sales.sort_values('month')

            # Створення рядка для підпису осі X
            df_sales['month_str'] = df_sales['month'].dt.strftime('%Y-%m')

        # --- 4. КЛІЄНТИ ---
        cust_qs = self.repo.get_total_spent_by_customer(min_spent=min_spent)
        df_customers = self._queryset_to_df(cust_qs)

        if not df_customers.empty:
            # Формуємо ім'я та закриваємо пропуски
            df_customers['name'] = df_customers['customerid__firstname'] + ' ' + df_customers['customerid__lastname']
            df_customers['name'] = df_customers['name'].fillna('Анонім').replace('', 'Анонім')

            # [FIX] Примусовий float
            df_customers['total_spent'] = pd.to_numeric(df_customers['total_spent'], errors='coerce').fillna(0).astype(
                float)

            # Групування клієнтів
            df_customers = df_customers.groupby('name', as_index=False)['total_spent'].sum()
            df_customers = df_customers.sort_values('total_spent', ascending=False)

        # --- 5. СКЛАДИ ---
        stock_qs = self.repo.get_low_stock_warehouses(threshold)
        df_stock = self._queryset_to_df(stock_qs)

        if not df_stock.empty:
            # [FIX] Захист локації
            df_stock['location'] = df_stock['location'].fillna('Невідомий склад')

            # [FIX] Примусовий float
            df_stock['total_books'] = pd.to_numeric(df_stock['total_books'], errors='coerce').fillna(0).astype(float)

            df_stock = df_stock.groupby('location', as_index=False)['total_books'].sum()

        # --- 6. ВИДАВНИЦТВА ---
        pub_qs = self.repo.get_publisher_book_stats()
        df_pub = self._queryset_to_df(pub_qs)

        if not df_pub.empty:
            # [FIX] Захист назви
            df_pub['name'] = df_pub['name'].fillna('Без назви')

            # [FIX] Примусовий float
            df_pub['books_published'] = pd.to_numeric(df_pub['books_published'], errors='coerce').fillna(0).astype(
                float)

            df_pub = df_pub.groupby('name', as_index=False)['books_published'].sum()

        return {
            'authors': df_authors,
            'genres': df_genres,
            'sales': df_sales,
            'customers': df_customers,
            'stock': df_stock,
            'publishers': df_pub
        }

    def get_stats_kpi(self, dfs: dict):
        """Розрахунок карток статистики на основі тих самих DataFrame'ів"""
        # Використовуємо .get() з пустим DF як дефолт, щоб не падало
        sales_df = dfs.get('sales', pd.DataFrame())
        cust_df = dfs.get('customers', pd.DataFrame())
        authors_df = dfs.get('authors', pd.DataFrame())
        stock_df = dfs.get('stock', pd.DataFrame())

        # Оскільки ми вже зробили .astype(float) вище, тут розрахунки будуть точними і без помилок типів
        return {
            'avg_monthly_revenue': round(sales_df['total_revenue'].mean(), 2) if not sales_df.empty else 0,
            'median_customer_spend': round(cust_df['total_spent'].median(), 2) if not cust_df.empty else 0,
            'max_books_by_author': authors_df['books_count'].max() if not authors_df.empty else 0,
            'deficit_warehouses_count': len(stock_df)
        }