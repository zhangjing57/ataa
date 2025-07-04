class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key= True, nullable=False, index=True, unique=False)
    cluster_info = Column(Text, nullable=True)
    status = Column(String(length=128), nullable=True)
    result = Column(String(length=128), nullable=True)
    detail = Column(Text, default=0, nullable= True)
    create_time = Column(DateTime, nullable=True)
    update_time = Column(DateTime, nullable=True)
    extra = Column(Text, default=0, nullable=True)