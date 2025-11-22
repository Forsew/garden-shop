from app.database import Base, engine
from app.models.users import User
from app.models.brigades import Brigade
from app.models.collectors import Collector
from app.models.products import ProductCategory, Product
from app.models.harvest import HarvestLog

print("Создание таблиц...")
Base.metadata.create_all(bind=engine)
print("✅ Все таблицы созданы успешно!")