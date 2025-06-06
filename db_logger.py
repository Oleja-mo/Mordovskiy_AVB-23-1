import psycopg2
from psycopg2 import sql
from datetime import datetime
import sys

class DBLogger:
    def __init__(self):
        self.conn = None
        try:
            print("Инициализация подключения к БД...")
            self.conn = psycopg2.connect(
                dbname='alarm_clock',
                user='postgres',
                password='111',
                host='localhost'
            )
        except Exception as e:
            print(f"Ошибка инициализации логгера: {e}", file=sys.stderr)
            raise

    def log_event(self, event_type, **kwargs):
        try:
            with self.conn.cursor() as cursor:
                query = sql.SQL("""
                    INSERT INTO alarm_logs (
                        timestamp, event_type,
                        current_time_value, alarm_time_value,
                        button_pressed,
                        alarm_state, recording_alarm
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """)
                cursor.execute(query, (
                    datetime.now(),
                    event_type,
                    kwargs.get('current_time_value'),
                    kwargs.get('alarm_time_value'),
                    kwargs.get('button_pressed'),
                    kwargs.get('alarm_state'),
                    kwargs.get('recording_alarm')
                ))
                self.conn.commit()
        except Exception as e:
            print(f"Ошибка логирования: {e}", file=sys.stderr)
            self.conn.rollback()


    def __del__(self):
        if self.conn:
            self.conn.close()