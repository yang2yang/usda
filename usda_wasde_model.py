from sqlalchemy import Column, String, Date, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class UsdaWasdeCorn(Base):
    __tablename__ = 'usda_wasde_corn'

    PublicationDate = Column(Date, primary_key=True)
    MarketingYear = Column(String, primary_key=True)
    Stage = Column(String)
    AreaPlanted = Column(Float)
    AreaHarvested = Column(Float)
    Yield = Column(Float)
    AreaPlanted = Column(Float)
    BeginningStocks = Column(Float)
    Production = Column(Float)
    Imports = Column(Float)
    TotalSupply = Column(Float)
    FeedandResidual = Column(Float)
    FoodSeedIndustrial = Column(Float)
    EthanolByProducts = Column(Float)
    TotalDomestic = Column(Float)
    Exports = Column(Float)
    TotalUse = Column(Float)
    EndingStocks = Column(Float)
    AvgFarmPriceLow = Column(Float)
    AvgFarmPriceHigh = Column(Float)


class usdaWasdeSoybean(Base):
    __tablename__ = "usda_wasde_soybean"

    PublicationDate = Column(Date, primary_key=True)
    MarketingYear = Column(String, primary_key=True)
    Stage = Column(String)
    AreaPlanted = Column(Float)
    AreaHarvested = Column(Float)
    Yield = Column(Float)
    BeginningStocks = Column(Float)
    Production = Column(Float)
    Imports = Column(Float)
    TotalSupply = Column(Float)
    Crushings = Column(Float)
    Exports = Column(Float)
    Seed = Column(Float)
    Residual = Column(Float)
    TotalUse = Column(Float)
    EndingStocks = Column(Float)
    AvgFarmPriceLow = Column(Float)
    AvgFarmPriceHigh = Column(Float)


class usdaWasdeSoybeanMeal(Base):
    __tablename__ = "usda_wasde_soybeanmeal"

    PublicationDate = Column(Date, primary_key=True)
    MarketingYear = Column(String, primary_key=True)
    Stage = Column(String)
    BeginningStocks = Column(Float)
    Production = Column(Float)
    Imports = Column(Float)
    TotalSupply = Column(Float)
    DomesticDisappearance = Column(Float)
    Exports = Column(Float)
    TotalUse = Column(Float)
    EndingStocks = Column(Float)
    AvgPriceLow = Column(Float)
    AvgPriceHigh = Column(Float)


class usdaWasdeSoybeanNoil(Base):
    __tablename__ = "usda_wasde_soybeanoil"

    PublicationDate = Column(Date, primary_key=True)
    MarketingYear = Column(String, primary_key=True)
    Stage = Column(String)
    BeginningStocks = Column(Float)
    Production = Column(Float)
    Imports = Column(Float)
    TotalSupply = Column(Float)
    DomesticDisappearance = Column(Float)
    Biodiesel = Column(Float)
    FoodFeedIndustrial = Column(Float)
    Exports = Column(Float)
    TotalUse = Column(Float)
    EndingStocks = Column(Float)
    AvgPriceLow = Column(Float)
    AvgPriceHigh = Column(Float)


class usdaWasdeWorldCorn(Base):
    __tablename__ = "usda_wasde_world_corn"

    PublicationDate = Column(Date, primary_key=True)
    MarketingYear = Column(String, primary_key=True)
    Stage = Column(String)
    Country = Column(String, primary_key=True)
    BeginningStocks = Column(Float)
    Production = Column(Float)
    Imports = Column(Float)
    DomesticCrush = Column(Float)
    TotalDomestic = Column(Float)
    Exports = Column(Float)
    EndingStocks = Column(Float)


class usdaWasdeWorldSoybean(Base):
    __tablename__ = "usda_wasde_world_soybean"

    PublicationDate = Column(Date, primary_key=True)
    MarketingYear = Column(String, primary_key=True)
    Stage = Column(String)
    Country = Column(String, primary_key=True)
    BeginningStocks = Column(Float)
    Production = Column(Float)
    Imports = Column(Float)
    DomesticFeed = Column(Float)
    TotalDomestic = Column(Float)
    Exports = Column(Float)
    EndingStocks = Column(Float)


engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)


Session = sessionmaker(bind=engine)
session = Session()