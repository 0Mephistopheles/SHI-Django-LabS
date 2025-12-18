import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
from DB_Management.repositories.analytics_repository import AnalyticsRepository

class SeabornVisualizationService:
    def __init__(self):
        sns.set_theme(style="whitegrid")
        self.palette = "viridis"

    def _get_base64_image(self):
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_str

    def generate_bar(self, df, x, y, color=None):
        if df.empty: return None
        plt.figure(figsize=(8, 5))
        sns.barplot(data=df, x=x, y=y, palette=color or self.palette)
        return self._get_base64_image()

    def generate_pie(self, df, values, labels):
        if df.empty: return None
        plt.figure(figsize=(6, 6))
        plt.pie(df[values], labels=df[labels], autopct='%1.1f%%', colors=sns.color_palette("pastel"))
        return self._get_base64_image()

    def generate_line(self, df, x, y):
        if df.empty: return None
        plt.figure(figsize=(10, 4))
        sns.lineplot(data=df, x=x, y=y, marker='o', color='#2ecc71', linewidth=2.5)
        plt.xticks(rotation=45)
        return self._get_base64_image()

    def generate_performance_chart(self, df, title="Аналіз продуктивності запитів"):
        if df.empty: return None
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x='workers', y='execution_time', marker='o', color='red', linewidth=2)
        plt.title(title, fontsize=14)
        plt.xlabel('Кількість потоків (Threads)')
        plt.ylabel('Загальний час виконання (секунди)')
        plt.grid(True, linestyle='--', alpha=0.7)
        return self._get_base64_image()