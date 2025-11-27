from sqlalchemy import Column, Integer, String, DateTime, Text, DECIMAL, BIGINT, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from BUDONG.api.core.database import Base
from BUDONG.api.models.enums.infra_category import InfraCategory
from BUDONG.api.models.enums.stats_type import StatsType
from BUDONG.api.models.enums.station_type import StationType
from BUDONG.api.models.enums.user_role import UserRole
from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, Float, DateTime, 
    ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from typing import List, Optional
from datetime import datetime

class Base(DeclarativeBase):
    pass

# ------------------------------------------------------------------
# 1. 사용자 및 활동 테이블 (User & Activity)
# ------------------------------------------------------------------

class User(Base):
    __tablename__ = "t_user"

    user_id = Column(Integer, primary_key=True, autoincrement=True, comment='회원 ID')
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    # 관계 설정 (User -> Reviews, Saved)
    reviews = relationship("BuildingReview", back_populates="user", cascade="all, delete-orphan")
    saved_buildings = relationship("UserSavedBuilding", back_populates="user", cascade="all, delete-orphan")


class BuildingReview(Base):
    __tablename__ = "t_building_review"

    review_id = Column(Integer, primary_key=True, autoincrement=True, comment='리뷰 ID')
    user_id = Column(Integer, ForeignKey("t_user.user_id"), nullable=False, comment='작성자 ID')
    
    # [주의] t_building의 PK는 BigInteger입니다. FK도 반드시 BigInteger여야 합니다. (DBML의 INT 수정됨)
    building_id = Column(BigInteger, ForeignKey("t_building.building_id"), nullable=False, comment='건물 ID')
    
    rating = Column(Integer, nullable=False, comment='평점 (1~5)')
    content = Column(Text)
    created_at = Column(DateTime, nullable=False, default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="reviews")
    building = relationship("Building", back_populates="reviews")


class UserSavedBuilding(Base):
    __tablename__ = "t_user_saved_building"
    __table_args__ = (
        UniqueConstraint('user_id', 'building_id', name='uq_user_building_save'),
    )

    save_id = Column(Integer, primary_key=True, autoincrement=True, comment='찜 ID')
    user_id = Column(Integer, ForeignKey("t_user.user_id"), nullable=False, comment='회원 ID')
    
    # [주의] t_building의 PK는 BigInteger입니다. FK도 BigInteger로 맞춰야 합니다.
    building_id = Column(BigInteger, ForeignKey("t_building.building_id"), nullable=False, comment='건물 ID')
    
    memo = Column(String(255), comment='간단 메모')
    created_at = Column(DateTime, nullable=False, default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="saved_buildings")
    building = relationship("Building", back_populates="saved_by_users")


# ------------------------------------------------------------------
# 2. 공공데이터 테이블 (Public Data Tables) - 관계 추가됨
# ------------------------------------------------------------------

class Building(Base):
    __tablename__ = "t_building"

    # 원본 덤프가 BigInt이므로 여기서도 BigInteger 유지
    building_id = Column(BigInteger, primary_key=True, index=True, comment="건물 ID")
    bjd_code = Column(BigInteger, ForeignKey("t_bjd_table.bjd_code"), index=True) 
    address = Column(Text)
    building_name = Column(Text)
    building_type = Column(Text)
    build_year = Column(Text)
    total_units = Column(Text)
    location = Column(Text)
    lon = Column(Float)
    lat = Column(Float)

    # 관계 설정 (역방향)
    reviews = relationship("BuildingReview", back_populates="building")
    saved_by_users = relationship("UserSavedBuilding", back_populates="building")
    real_transactions = relationship("RealTransactionPrice", back_populates="building")
    bjd = relationship("BjdTable", back_populates="buildings")


class BjdTable(Base):
    __tablename__ = "t_bjd_table"

    bjd_code = Column(BigInteger, primary_key=True, index=True)
    bjd_name = Column(Text)
    bjd_eng = Column(Text)

    # 관계 설정
    buildings = relationship("Building", back_populates="bjd")
    jcg_mappings = relationship("JcgBjdTable", back_populates="bjd")


class RealTransactionPrice(Base):
    __tablename__ = "t_real_transaction_price"

    tx_id = Column(BigInteger, primary_key=True, index=True)
    building_id = Column(BigInteger, ForeignKey("t_building.building_id"), index=True)
    transaction_date = Column(Text)
    price = Column(BigInteger)
    area_sqm = Column(Float)
    floor = Column(Float)

    # 관계 설정
    building = relationship("Building", back_populates="real_transactions")


class JcgBjdTable(Base):
    __tablename__ = "t_jcg_bjd_table"

    region_name_full = Column(Text)
    ja_chi_gu_code = Column(BigInteger, primary_key=True) # 복합키 중 하나라고 가정
    bjd_code = Column(BigInteger, ForeignKey("t_bjd_table.bjd_code"), primary_key=True) # 복합키

    # 관계 설정
    bjd = relationship("BjdTable", back_populates="jcg_mappings")


# ------------------------------------------------------------------
# 3. 기타 통계/정보 테이블 (관게가 명확치 않아 독립적으로 유지)
# ------------------------------------------------------------------

class CrimeCCTV(Base):
    __tablename__ = "t_crime_CCTV"
    jcg_name = Column(Text, primary_key=True)
    crime_num = Column(BigInteger)
    cctv_num = Column(BigInteger)
    dangerous_rating = Column(BigInteger)
    CCTV_security_rating = Column(BigInteger)

class Noise(Base):
    __tablename__ = "t_noise"
    address = Column(Text, primary_key=True) # 임시 PK
    noise_max = Column(BigInteger)
    noise_avg = Column(BigInteger)
    noise_min = Column(BigInteger)
    lat = Column(Float)
    lon = Column(Float)

class Park(Base):
    __tablename__ = "t_park"
    park_name = Column(Text, primary_key=True)
    park_introduce = Column(Text)
    park_size = Column(Text)
    region = Column(Text)
    address = Column(Text)
    management = Column(Text)
    lon = Column(Float)
    lat = Column(Float)

class PoliceStationInfo(Base):
    __tablename__ = "t_police_station_info"
    polic_station_name = Column(Text, primary_key=True)
    address = Column(Text)
    bjd_name = Column(Text)

class PublicTransportByAdminDong(Base):
    __tablename__ = "t_public_transport_by_admin_dong"
    hjd_id = Column(BigInteger, primary_key=True, index=True)
    passenger_num = Column(BigInteger)
    complexity_rating = Column(BigInteger)

class School(Base):
    __tablename__ = "t_school"
    school_name = Column(Text, primary_key=True)
    build_year = Column(BigInteger)
    ja_chi_gu = Column(Text)
    school_level = Column(Text)
    category = Column(Text)
    address = Column(Text)
    lon = Column(Float)
    lat = Column(Float)

class Station(Base):
    __tablename__ = "t_station"
    station_id = Column(BigInteger, primary_key=True, index=True)
    line = Column(BigInteger)
    station_name = Column(Text)
    lat = Column(Float)
    lon = Column(Float)