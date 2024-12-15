from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)

    auditions = relationship('Audition', back_populates='role')

class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='auditions')

    def call_back(self):
        self.hired = True


engine = create_engine('sqlite:///theater.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



class Role(Base):
    # Assuming the previous definitions

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if hired_auditions:
            return hired_auditions[0]
        else:
            return "no actor has been hired for this role"

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) > 1:
            return hired_auditions[1]
        else:
            return "no actor has been hired for understudy for this role"

