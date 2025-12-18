import time
import concurrent.futures
from django.db import connection
from DB_Management.repositories.unit_of_work import UnitOfWork

class ConcurrencyService:
    def __init__(self):
        self.uow = UnitOfWork()

    def _single_query(self):
        connection.close() 
        return list(self.uow.analytics.get_books_count_by_author())

    def run_experiment(self, total_requests=150, max_workers_list=[1, 2, 4, 8, 16]):
        results = []
        
        for workers in max_workers_list:
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [executor.submit(self._single_query) for _ in range(total_requests)]
                concurrent.futures.wait(futures)
            
            duration = time.time() - start_time
            results.append({
                'workers': workers,
                'execution_time': duration,
                'avg_time_per_request': duration / total_requests
            })
            
        return results