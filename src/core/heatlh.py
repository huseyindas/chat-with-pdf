import requests
import redis
import psycopg2


from core.config import settings
from core.logging import logger


def health_check():
    health_status = {
        "postgresql": "unhealthy",
        "redis": "unhealthy",
        "ollama": "unhealthy"
    }

    try:
        postgres_conn = psycopg2.connect(
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_server,
            port=settings.postgres_port
        )
        cur = postgres_conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        health_status["postgresql"] = "healthy"
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")

    try:
        redis_conn = redis.Redis(
            host=settings.redis_server,
            port=settings.redis_port,
            db=0
        )
        if redis_conn.ping():
            health_status["redis"] = "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")

    try:
        response = requests.get(settings.ollama_host)
        if response.status_code == 200:
            health_status["ollama"] = "healthy"
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")

    overall_status = "healthy" if all(
        status == "healthy" for status in health_status.values()
    ) else "unhealthy"
    status_code = 200 if overall_status == "healthy" else 500

    return {
        "status_code": status_code,
        "response": {"status": overall_status, "details": health_status}
    }
