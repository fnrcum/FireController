from hashlib import md5
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine, DateTime, update
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


config = 'mysql+pymysql://root:dreamteam@127.0.0.1/firestarter'
secret_key = 'FEF9B%399-!8EF6- 4B16-[9BD4-092B1<85D632D'


def generate_hash(password):
    return md5((md5(secret_key.encode("utf-8")).hexdigest() + md5(password.encode("utf-8")).hexdigest()).encode("utf-8")).hexdigest()


def check_hash(password, stored_hash):
    return password == stored_hash


class User(Base):

    __tablename__ = 'users'

    UserName = Column(String(100), primary_key=True)
    Roles = Column(String(100), primary_key=True)
    Password = Column(Text, unique=False)

    def __init__(self, UserName, Password, Roles):
        self.UserName = UserName
        self.Password = Password
        self.Roles = Roles

    def __repr__(self):
        return '<User: {}>'.format(self.last_name)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_user_name(self):
        return self.UserName


class Server(Base):
    """
    Create a servers table
    """

    __tablename__ = 'servers'

    Id = Column(String(36), primary_key=True)
    Name = Column(String(100))
    Description = Column(String(300))
    Params = Column(String(600))
    Config = Column(String(600))
    PathStart = Column(String(300))
    PathStop = Column(String(300))
    Status = Column(Integer)
    Map = Column(String(100))
    Players = Column(Integer)
    PlayersMax = Column(Integer)
    Version = Column(Integer)
    LastUpdate = Column(DateTime)
    LoadTime = Column(Integer)

    def __init__(self, Id, Name, Description, Params, Config, PathStart, PathStop, Status, Map, Players, PlayersMax, Version, LastUpdate, LoadTime):
        self.Id = Id
        self.Name = Name
        self.Description = Description
        self.Params = Params
        self.Config = Config
        self.PathStart = PathStart
        self.PathStop = PathStop
        self.Status = Status
        self.Map = Map
        self.Players = Players
        self.PlayersMax = PlayersMax
        self.Version = Version
        self.LastUpdate = LastUpdate
        self.LoadTime = LoadTime

    def __repr__(self):
        return '<Server: {}>'.format(self.Id)


class Activity(Base):
    """
    Create a Activity table
    """

    __tablename__ = 'activity'

    Id = Column(String(36), primary_key=True)
    LastUpdate = Column(DateTime)
    Message = Column(String(300))

    def __init__(self, Id, LastUpdate, Message):
        self.Id = Id
        self.LastUpdate = LastUpdate
        self.Message = Message

    def __repr__(self):
        return '<Activity: {}>'.format(self.name)


engine = create_engine(config, echo=True)
session = sessionmaker()
session.configure(bind=engine)
# Base.metadata.create_all(engine)
s = session()

# s.execute(update(Server).where(Server.Id == "2fab42c6-e260-473c-abfc-1725b7b3daeb").values(LoadTime=10))
# s.commit()