from sqlalchemy import (JSON, Column, Float, ForeignKey, Integer, OneToOne,
                        String)

from src.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    driver = Column(Integer, OneToOne("drivers.id"), nullable=False)


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    car_mark = Column(String, nullable=False)
    car_plate_number = Column(String, nullable=False)


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=False)
    description = Column(String, nullable=False)


class RoleMatrix(Base):
    __tablename__ = "roles_permissions"

    id = Column(Integer, primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey(
        "permissions.id"), nullable=False)
