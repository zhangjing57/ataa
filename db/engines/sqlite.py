import threading
from config import CONF
from oslo_db.sqlalchemy import session
from sqlalchemy.pool import NullPool  # 禁用连接池复用
from sqlalchemy import event  # 用于启用 WAL 模式

DATABASE_URL = CONF.DEFAULT.sqlite_path

_LOCK = threading.Lock()
_FACADE = None


def _create_facade_lazily():
    global _FACADE
    with _LOCK:
        if _FACADE is None:
            # 关键配置：禁用连接池 + 线程安全 + WAL 模式
            engine_kwargs = {
                "poolclass": NullPool,  # 禁用连接池复用 [1,5](@ref)
                "connect_args": {"check_same_thread": False},  # 允许多线程访问 [7](@ref)
                "executemany_mode": "batch"  # 批量操作优化
            }
            _FACADE = session.EngineFacade(
                DATABASE_URL,
                engine_kwargs=engine_kwargs
            )

            # 启用 WAL 模式提升并发读性能 [3](@ref)
            engine = _FACADE.get_engine()

            @event.listens_for(engine, "connect")
            def set_sqlite_pragma(dbapi_conn, _):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.execute("PRAGMA cache_size=-10000;")  # 10MB 缓存
                cursor.close()
        return _FACADE


def get_engine():
    return _create_facade_lazily().get_engine()


def get_session(**kwargs):
    return _create_facade_lazily().get_session(**kwargs)