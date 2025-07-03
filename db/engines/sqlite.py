import sqlite3
from queue import Queue
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 内置连接池（自动管理）
engine = create_engine(
    "sqlite:///app.db",
    pool_size=10,
    max_overflow=20,
    pool_timeout=30
)
Session = sessionmaker(bind=engine)

# 使用示例
with Session() as session:
    session.execute("DELETE FROM temp_data")
    session.commit()

class SQLiteConnectionPool:
    def __init__(self, db_path, max_size=10, timeout=5):
        self.db_path = db_path
        self.timeout = timeout
        self._pool = Queue(maxsize=max_size)
        self._lock = Lock()
        # 初始化连接池
        for _ in range(max_size):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            self._pool.put(conn)

    def get_conn(self):
        """获取连接（支持超时等待）"""
        try:
            return self._pool.get(timeout=self.timeout)
        except Queue.Empty:
            raise TimeoutError("获取数据库连接超时")

    def release_conn(self, conn):
        """归还连接（非关闭）"""
        with self._lock:
            if not self._pool.full():
                self._pool.put(conn)
            else:  # 连接池已满则直接关闭
                conn.close()

    def close_all(self):
        """关闭所有连接"""
        while not self._pool.empty():
            conn = self._pool.get()
            conn.close()


class SQLiteDB:
    def __init__(self, db_path, pool_size=5):
        self.pool = SQLiteConnectionPool(db_path, max_size=pool_size)

    @contextmanager
    def _connection(self):
        """上下文管理连接（自动获取/归还）"""
        conn = self.pool.get_conn()
        try:
            yield conn
            conn.commit()  # 操作成功自动提交
        except Exception as e:
            conn.rollback()  # 异常时回滚
            raise e
        finally:
            self.pool.release_conn(conn)

    def execute(self, sql, params=()):
        """执行SQL并返回影响行数"""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.rowcount

    def fetch_all(self, sql, params=()):
        """查询所有结果"""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()


class PooledConnection:
    def __init__(self, pool):
        self.pool = pool
        self.conn = None

    def __enter__(self):
        self.conn = self.pool.get_conn()
        return self.conn

    def __exit__(self, exc_type, *_):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.pool.release_conn(self.conn)


# 使用示例
with PooledConnection(pool) as conn:
    conn.execute("UPDATE settings SET value=1")

# 使用示例
db = SQLiteDB("app.db")
# 插入数据
db.execute("INSERT INTO logs (message) VALUES (?)", ("System started",))
# 查询数据
results = db.fetch_all("SELECT * FROM logs")
print(results)

# 使用示例
pool = SQLiteConnectionPool("test.db", max_size=5)
try:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
finally:
    pool.release_conn(conn)  # 使用后归还
    pool.close_all()         # 程序退出时关闭[1,6](@ref)